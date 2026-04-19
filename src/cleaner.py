import pandas as pd

class Cleaner:

    def _standarize_columns(self, df):
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    def clean_sales(self, df_sales):
        df = self._standarize_columns(df_sales)

        df["month"] = pd.to_datetime(df["date"], errors="coerce")
        df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0)

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
            .map({"active": 1, "zawieszona": 0})
        )

        df["own_channel_active"] = df["own_channel_active"].ffill().fillna(1)
        df["is_active"] = df["own_channel_active"] == 1

        return df[["month", "own_channel_active", "is_active"]]

    def enrich_sales_with_own_activity(self, df_sales, df_jdg):
        monthly = (
            df_sales.groupby("month", as_index=False)
            .agg(units=("units", "sum"))
        )

        merged = df_jdg.merge(monthly, on="month", how="left")

        merged["units"] = merged["units"].fillna(0)
        merged["own_channel_active"] = merged["own_channel_active"].ffill().fillna(1)

        # 🔥 META: full JDG timeline
        total_jdg_months = len(df_jdg)

        # 🔥 META: Amazon start
        first_amazon_month = monthly["month"].min()

        # 🔥 FILTER: analysis scope
        merged = merged[merged["month"] >= first_amazon_month]

        # 🔥 META: overlap
        overlap_months = len(merged)

        # 🔥 attach metadata
        merged.attrs["meta"] = {
            "jdg_total_months": total_jdg_months,
            "amazon_start_month": first_amazon_month,
            "overlap_months": overlap_months
        }

        return merged.reset_index(drop=True)

    def enrich_sales_with_own_activity_raw(self, df_sales, df_jdg):
        """
        Raw (detailed) merge — still filtered to Amazon period for consistency
        """

        merged = df_sales.merge(df_jdg, on="month", how="left")

        merged["own_channel_active"] = merged["own_channel_active"].ffill().fillna(1)

        # 🔧 FIX: keep only months where Amazon exists
        first_amazon_month = df_sales["month"].min()
        merged = merged[merged["month"] >= first_amazon_month]

        return merged.reset_index(drop=True)
