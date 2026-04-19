import os
import pandas as pd

class DataFileNotFoundError(Exception):
    pass

class InvalidSchemaError(Exception):
    pass

class Loader:

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.path_amazon_sales = os.path.join(self.data_dir, "amazon_sales.csv")
        self.path_own_channel_sales = os.path.join(self.data_dir, "own_channel_activity.csv")
    
    def _ensure_exist(self, path):
        if not os.path.exists(path):
            raise DataFileNotFoundError(f"Expected file not found: {path}")
    
    def _read_csv(self, path):
        return pd.read_csv(path)
    
    def _validate_columns(self, df, required_cols, file_label):
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise InvalidSchemaError(f"Missing columns in {file_label}: {missing}")
    
    def load_sales(self):
        self._ensure_exist(self.path_amazon_sales)
        df = self._read_csv(self.path_amazon_sales)
        self._validate_columns(df, ["Date", "Title", "ASIN", "Marketplace", "Units"], "amazon_sales.csv")
        return df
    
    def load_own_channel_activity(self):
        self._ensure_exist(self.path_own_channel_sales)
        df = self._read_csv(self.path_own_channel_sales)
        self._validate_columns(df, ["Miesiac", "JDG"], "own_channel_activity.csv")
        return df
    
    def load_all(self):
        return self.load_sales(), self.load_own_channel_activity()
