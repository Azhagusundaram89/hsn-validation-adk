import pandas as pd


class HSNDataLoader:
    def __init__(self, file_path='HSN_SAC (3).xlsx'):
        self.file_path = file_path
        try:
            # Load Excel file and clean it like the standalone logic
            self.hsn_df = pd.read_excel(self.file_path, dtype=str).fillna("")
            self.hsn_df.columns = self.hsn_df.columns.str.strip()

            print("🔍 Available columns:", self.hsn_df.columns.tolist())

            # Identify and rename HSN code column
            possible_hsn_cols = ["hsncode", "hsn code", "hsn", "code", "hsn/sac", "hsn_sac"]
            self.hsn_col = self._find_and_rename_column(possible_hsn_cols, "HSNCode")

            # Identify and rename Description column
            possible_desc_cols = ["description", "desc", "product description", "item desc", "description of goods"]
            self.desc_col = self._find_and_rename_column(possible_desc_cols, "Description")

            # Strip and clean values
            self.hsn_df["HSNCode"] = self.hsn_df["HSNCode"].astype(str).str.strip()
            self.hsn_df["Description"] = self.hsn_df["Description"].astype(str).str.strip()

            # Cache valid code lengths
            self.valid_lengths = set(self.hsn_df["HSNCode"].str.len())

            print("✅ HSN data loaded successfully!")
            print(f"🧾 Total codes: {len(self.hsn_df)}")

        except Exception as e:
            raise RuntimeError(f"❌ Failed to load HSN Excel file: {str(e)}")

    def _find_and_rename_column(self, candidates, new_name):
        for col in self.hsn_df.columns:
            if col.strip().lower() in candidates:
                self.hsn_df.rename(columns={col: new_name}, inplace=True)
                return new_name
        raise ValueError(f"No valid column found for: {new_name}")

    def validate_hsn_code(self, code: str) -> dict:
        code = code.strip()
        row = self.hsn_df[self.hsn_df["HSNCode"] == code]
        if not row.empty:
            return {
                "hsn_code": code,
                "description": row.iloc[0]["Description"],
                "valid": True
            }
        return {
            "hsn_code": code,
            "description": None,
            "valid": False,
            "message": "HSN code not found."
        }

    def hierarchical_check(self, code: str) -> dict:
        code = code.strip()
        for length in sorted(self.valid_lengths, reverse=True):
            partial_code = code[:length]
            row = self.hsn_df[self.hsn_df["HSNCode"] == partial_code]
            if not row.empty:
                return {
                    "hsn_code": partial_code,
                    "description": row.iloc[0]["Description"],
                    "matched_length": length,
                    "valid": True
                }
        return {
            "hsn_code": code,
            "description": None,
            "valid": False,
            "message": "No hierarchical match found."
        }
