"""
A cleaner module that prepare data for analysis
"""

import pandas as pd

class Cleaner:
    def __init__(self):
        pass

    def _standarize_columns(self, df):
        df = df.copy()
        new_cols = []
        for column in df.columns:
            clean_name = column.strip().lower()
            new_cols.append(clean_name)
        
        df.columns = new_cols
        return df
    
    def clean_sales(self, df_sales):
        df = self._standarize_columns(df_sales)

        df["month"] = pd.to_datetime(df["date"], errors="coerce")
        df["units"] = pd.to_numeric(df["units"], errors="coerce")

        df["units"] = df["units"].fillna(0)
        df = df[df["units"] >= 0]
        df = df[df["month"].notna()]

        df = df.reset_index(drop=True)

        return df

    def clean_jdg(self, df_jdg):
        df = self._standarize_columns(df_jdg)

        df["month"] = pd.to_datetime(df["miesiac"], errors="coerce")

        df["own_channel_active"] = (
            df["jdg"]
            .fillna("active") # NaN = active
            .str.lower()
            .str.strip()
            .map({
                "active": 1,
                "zawieszona": 0
            })
        )

        if df["own_channel_active"].isna().any():
            unknown = df[df["own_channel_active"].isna()]["jdg"].unique()
            raise ValueError(f"Unknown JDG values: {unknown}")

        df = df[["month", "own_channel_active"]]

        return df
    
    def enrich_sales_with_own_activity(self, df_sales, df_own_activity):
        merged = df_sales.merge(
            df_own_activity[["month", "own_channel_active"]],
            on="month",
            how="left"
        )
        return merged
