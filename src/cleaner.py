"""
A cleaner module that prepare data for analysis
"""

import pandas as pd

class Cleaner:
    def __init__(self):
        pass

    def _standarize_columns(self, df):
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    
    def clean_sales(self, df_sales):
        df = self._standarize_columns(df_sales)

        df["month"] = pd.to_datetime(df["date"], errors="coerce")
        df["units"] = pd.to_numeric(df["units"], errors="coerce")

        df["units"] = df["units"].fillna(0)
        df = df[df["units"] >= 0]
        df = df[df["month"].notna()]

        return df.reset_index(drop=True)

    def clean_jdg(self, df_jdg):
        df = self._standarize_columns(df_jdg)

        df["month"] = pd.to_datetime(df["miesiac"], errors="coerce")

        df["own_channel_active"] = (
            df["jdg"]
            .fillna("active")
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

        df["is_active"] = df["own_channel_active"] == 1

        return df[["month", "own_channel_active", "is_active"]]

    def enrich_sales_with_own_activity(self, df_sales, df_own_activity):
        merged = df_own_activity.merge(
            df_sales,
            on="month",
            how="left"
        )

        merged["units"] = merged["units"].fillna(0)

        merged["own_channel_active"] = merged["own_channel_active"].fillna(1)
        merged["is_active"] = merged["is_active"].fillna(True)

        return merged
