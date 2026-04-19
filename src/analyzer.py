import pandas as pd
from config.products import ASIN_TO_BOOK


class AggregationAnalyzer:

    def __init__(self, df):
        self.df = df.copy()

    def by_product(self):
        df = self.df.copy()

        df["book"] = df["asin"].map(ASIN_TO_BOOK)
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
        """
        🔥 IMPROVED:
        Uses share of yearly sales instead of raw averages.
        This makes quarters comparable across years.
        """

        df = self.by_month()

        df["year"] = df["month"].dt.year
        df["quarter"] = df["month"].dt.quarter

        # 🔧 FIX: yearly total per year
        df["year_total"] = df.groupby("year")["units"].transform("sum")

        # 🔧 FIX: share of each month in its year
        df["share"] = df["units"] / df["year_total"]

        # 🔧 aggregate to quarter level
        result = (
            df.groupby("quarter", as_index=False)
            .agg(avg_share=("share", "mean"))
        )

        return result


class CannibalizationAnalyzer:

    def __init__(self, df):
        self.df = df.sort_values("month")

    def rolling_trend(self, window=3):
        df = self.df.copy()

        # 🔧 FIX: avoid NaNs at start
        df["rolling_units"] = df["units"].rolling(window, min_periods=1).mean()

        return df

    def jdg_time_series(self):
        df = self.df.copy()

        # 🔧 FIX: consistent rolling
        df["rolling_3m"] = df["units"].rolling(3, min_periods=1).mean()

        return df

    def impact_summary(self):
        df = self.df.copy()

        stats = df.groupby("own_channel_active")["units"].mean()

        return {
            "active_avg": float(stats.get(1, 0)),
            "suspended_avg": float(stats.get(0, 0))
        }

    def detect_event_month(self):
        """
        🔥 NEW:
        Detect REAL transition from active → suspended
        """

        df = self.df.copy()
        df["prev"] = df["own_channel_active"].shift(1)

        events = df[
            (df["own_channel_active"] == 0) &
            (df["prev"] == 1)
        ]

        if events.empty:
            return None

        return events["month"].iloc[0]

    def event_analysis(self, window=6):
        """
        🔥 IMPROVED:
        Uses detected event instead of arbitrary month
        """

        df = self.df.copy()

        event_month = self.detect_event_month()

        if event_month is None:
            return {
                "error": "No valid JDG suspension event detected"
            }

        before = df[df["month"] < event_month].tail(window)
        after = df[df["month"] >= event_month].head(window)

        return {
            "event_month": event_month,
            "before_avg": before["units"].mean(),
            "after_avg": after["units"].mean(),
            "delta": after["units"].mean() - before["units"].mean()
        }


class KPIAnalyzer:

    def __init__(self, df_ts, df_detailed):
        self.df_ts = df_ts.copy()
        self.df_detailed = df_detailed.copy()

    def kpis(self):
        total_units = int(self.df_ts["units"].sum())

        books = self.df_detailed["asin"].map(ASIN_TO_BOOK)
        distinct_products = int(books.nunique())

        regions = (
            self.df_detailed["marketplace"]
            .str.split(".").str[-1]
            .str.upper()
        )
        distinct_regions = int(regions.nunique())

        monthly = self.df_ts.copy()

        # 🔥 META from cleaner
        meta = self.df_ts.attrs.get("meta", {})

        jdg_total_months = meta.get("jdg_total_months", len(monthly))
        overlap_months = meta.get("overlap_months", len(monthly))

        # 🔹 analysis scope
        active_months = int((monthly["own_channel_active"] == 1).sum())
        suspended_months = int((monthly["own_channel_active"] == 0).sum())

        # 🔹 Amazon presence (not sales!)
        amazon_months = len(monthly)

        grouped = monthly.groupby("own_channel_active")["units"].mean()

        active_avg = grouped.get(1, 0)
        suspended_avg = grouped.get(0, 0)

        if active_avg == 0:
            cannibalization_pct = 0
            label = "Insufficient data"
        else:
            cannibalization_pct = (suspended_avg - active_avg) / active_avg

            if abs(cannibalization_pct) < 0.10:
                label = "No clear difference"
            elif cannibalization_pct < 0:
                label = "Lower Amazon sales observed\nduring JDG suspension (not causal)"
            else:
                label = "Higher Amazon sales observed\nduring JDG suspension (not causal)"

        return {
            "total_units": total_units,
            "distinct_products": distinct_products,
            "distinct_regions": distinct_regions,

            # 🔥 DATA CONTEXT
            "jdg_total_months": jdg_total_months,
            "amazon_observed_months": amazon_months,
            "overlap_months": overlap_months,

            # 🔥 ANALYSIS SPLIT
            "active_months": active_months,
            "suspended_months": suspended_months,

            # 🔥 RESULT
            "cannibalization_impact": label,
            "cannibalization_pct": cannibalization_pct
        }
