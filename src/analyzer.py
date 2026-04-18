import pandas as pd
from config.products import ASIN_TO_BOOK

class AggregationAnalyzer:

    def __init__(self, df):
        self.df = df.copy()

    def by_product(self):
        df = self.df.copy()

        df["book"] = df["asin"].map(ASIN_TO_BOOK)

        # fallback jeśli coś nie ma mapowania
        df["book"] = df["book"].fillna("unknown")

        return (
            df.groupby("book", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def by_region(self):
        df = self.df.copy()

        df["region"] = df["marketplace"].str.split(".").str[-1].str.upper()

        return (
            df.groupby("region", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def by_month(self):
        return (
            self.df.groupby("month", as_index=False)
            .agg(units=("units", "sum"))
            .sort_values("month")
        )

    def seasonality(self):

        df = self.by_month()

        df["year"] = df["month"].dt.year
        df["quarter"] = df["month"].dt.quarter

        yearly_avg = df.groupby("year")["units"].sum().mean()

        q = (
            df.groupby(["year", "quarter"], as_index=False)
            .agg(units=("units", "sum"))
        )

        result = (
            q.groupby("quarter", as_index=False)
            .agg(avg_units=("units", "mean"))
        )

        result["share_of_year"] = result["avg_units"] / yearly_avg

        return result


class CannibalizationAnalyzer:

    def __init__(self, df):
        self.df = df.sort_values("month")

    def rolling_trend(self, window=3):
        df = self.df.copy()
        df["rolling_units"] = df["units"].rolling(window).mean()
        return df

    def jdg_time_series(self):
        df = self.df.copy()
        df["rolling_3m"] = df["units"].rolling(3).mean()
        return df

    def impact_summary(self):

        df = self.df.copy()

        stats = df.groupby("own_channel_active")["units"].mean()

        return {
            "active_avg": float(stats.get(1, 0)),
            "suspended_avg": float(stats.get(0, 0))
        }

    def event_analysis(self, event_month, window=6):

        df = self.df.copy()

        before = df[df["month"] < event_month].tail(window)
        after = df[df["month"] >= event_month].head(window)

        return {
            "before_avg": before["units"].mean(),
            "after_avg": after["units"].mean(),
            "delta": after["units"].mean() - before["units"].mean()
        }


class KPIAnalyzer:

    def __init__(self, df_ts, df_detailed):
        self.df_ts = df_ts.copy()
        self.df_detailed = df_detailed.copy()

    def kpis(self):

        # =========================
        # CORE
        # =========================
        total_units = int(self.df_ts["units"].sum())

        # =========================
        # PRODUCTS / REGIONS
        # =========================
        books = self.df_detailed["asin"].map(ASIN_TO_BOOK)
        distinct_products = int(books.nunique())

        regions = (
            self.df_detailed["marketplace"]
            .str.split(".").str[-1]
            .str.upper()
        )
        distinct_regions = int(regions.nunique())

        # =========================
        # JDG ACTIVITY
        # =========================
        monthly = self.df_ts.copy()

        active_months = int((monthly["own_channel_active"] == 1).sum())
        suspended_months = int((monthly["own_channel_active"] == 0).sum())

        # =========================
        # AMAZON COVERAGE
        # =========================
        amazon_active_months = int((monthly["units"] > 0).sum())
        total_months = len(monthly)

        amazon_coverage = (
            amazon_active_months / total_months
            if total_months > 0 else 0
        )

        # =========================
        # CANNIBALIZATION (prosty sygnał)
        # =========================
        grouped = monthly.groupby("own_channel_active")["units"].mean()

        active_avg = grouped.get(1, 0)
        suspended_avg = grouped.get(0, 0)

        if active_avg == 0:
            cannibalization_impact = "Insufficient data"
        else:
            ratio = suspended_avg / active_avg

            cannibalization_impact = (
                "No JDG impact on Amazon sales"
                if ratio >= 1 else
                "Possible cannibalization effect"
            )

        # =========================
        # FINAL DICT
        # =========================
        return {
            "total_units": total_units,
            "distinct_products": distinct_products,
            "distinct_regions": distinct_regions,
            "active_months": active_months,
            "suspended_months": suspended_months,
            "amazon_active_months": amazon_active_months,
            "amazon_coverage": amazon_coverage,
            "cannibalization_impact": cannibalization_impact
        }
