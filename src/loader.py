"""
A loader class that loads CSV files with rebust error handling and basic validation

Expected input file(CSV):
- amazon_sales.csv  [columns: Date, Title, ASIN, Marketplace, Units]
"""

import os
import pandas as pd

class DataFileNotFoundError(Exception):
    pass

class InvalidSchemaError(Exception):
    pass

class Loader:
    """
    Usage:
        loader = Loader(data_dir="../data")
        df_sales loader.load_sales()
    """
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.path_amazon_sales = os.path.join(self.data_dir, "amazon_sales.csv")
    
    def _ensure_exist(self, path):
        print("CWD:", os.getcwd())
        # print("DATA DIR:", self.data_dir)
        # print("FULL PATH:", self.path)
        
        # if os.path.exists(self.data_dir):
        #     print("FILES:", os.listdir(self.data_dir))
        # else:
        #     print("DATA DIR DOES NOT EXIST")
        print("ensure exist", os.path.exists(path))

        if not os.path.exists(path):
            raise DataFileNotFoundError(f"Expected file not found: {path}")
    
    def _read_csv(self, path):
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            raise DataFileNotFoundError(f"File not found: {path}")
        except pd.errors.EmptyDataError:
            raise InvalidSchemaError(f"File is empty or has no rows: {path}")
        except pd.errors.ParserError as e:
            raise InvalidSchemaError(f"CSV parse error in: {path} -> {e}")
    
    def _validate_columns(self, df, required_cols, file_label):
        missing = []
        for column in required_cols:
            if column not in df.columns:
                missing.append(column)
        if missing:
            raise InvalidSchemaError(
                f"Missing required columns in {file_label}: {missing}.\n"
                f"Found columns: {list(df.columns)}"
            )
        
    def load_sales(self):
        self._ensure_exist(self.path_amazon_sales)
        df = self._read_csv(self.path_amazon_sales)
        self._validate_columns(df, ["Date", "Title", "ASIN", "Marketplace", "Units"], "amazon_sales.csv")
        print("load_sales")
        return df

