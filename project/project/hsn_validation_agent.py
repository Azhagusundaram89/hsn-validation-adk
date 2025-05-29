from google.adk.agents import Agent
from project.hsn_data_loader import HSNDataLoader
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyBxKaoDozH-kiE0Z6dHNKuukJGe2gnz3mM"))

for model in genai.list_models():
    print(model.name)

loader = HSNDataLoader('HSN_SAC (3).xlsx')

def validate_single_code(hsn_code: str) -> dict:
    return loader.validate_hsn_code(hsn_code)

def validate_multiple_codes(hsn_codes: str) -> dict:
    codes = [c.strip() for c in hsn_codes.split(",")]
    results = [loader.validate_hsn_code(code) for code in codes]
    return {"results": results}

def hierarchical_validate(hsn_code: str) -> dict:
    return loader.hierarchical_check(hsn_code)

root_agent = Agent(
    name="hsn_code_validator",
    model="gemini-1.5-flash-latest",  # ✅ Correct model name for API key
    description="Agent to validate HSN codes against a master dataset.",
    instruction="Validate HSN codes and return their descriptions or appropriate error messages.",
    tools=[validate_single_code, validate_multiple_codes, hierarchical_validate],
)
