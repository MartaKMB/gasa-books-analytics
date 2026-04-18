"""
Business logic for aggregations and KPIs
"""

from config.products import ASIN_TO_BOOK
from config.status import STATUS_MAP
from config.regions import MARKETPLACE_TO_REGION


class BaseAnalyzer:
    def __init__(self, df):
        self.df = df.copy()

        required = [
            "month", "title", "asin",
            "marketplace", "units", "own_channel_active"
        ]

        missing = [c for c in required if c not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        self.df = self.df[self.df["month"].notna()].copy()

        self._add_book_label()
        self._add_region()
        self._add_status()

    def _add_book_label(self):
        self.df["book"] = self.df["asin"].map(ASIN_TO_BOOK)

    def _add_region(self):
        region = (
            self.df["marketplace"]
            .str.split(".").str[-1]
            .str.upper()
        )
        self.df["region"] = region.replace(MARKETPLACE_TO_REGION)

    def _add_status(self):
        self.df["channel_status"] = self.df["own_channel_active"].map(STATUS_MAP)

# KPI ANALYZER
class KPIAnalyzer(BaseAnalyzer):

    def kpis(self):
        cannibal = CannibalizationAnalyzer(self.df).impact_summary()

        activity_stats = self.activity_split_from_df()

        return {
            "total_units": int(self.df["units"].sum()),
            "distinct_products": int(self.df["asin"].nunique()),
            "distinct_regions": int(self.df["region"].nunique()),
            "cannibalization_impact": cannibal["insight"],
            "channel_substitution_effect": self._status_impact(),
            "channel_substitution_effect_normalized": self._status_impact_normalized(),
            "amazon_active_months": self._amazon_active_months(),
            "amazon_coverage": self._amazon_coverage(),
        }

    def activity_split_from_df(self):
        df = self.df.drop_duplicates("month")

        return {
            "active_months": int((df["own_channel_active"] == 1).sum()),
            "suspended_months": int((df["own_channel_active"] == 0).sum()),
            "total_months": int(df["month"].nunique())
        }

    def _amazon_coverage(self):
        df = self.df.copy()

        monthly = df.groupby("month", as_index=False).agg(units=("units", "sum"))

        active_months = (monthly["units"] > 0).sum()
        total_months = len(monthly)

        if total_months == 0:
            return 0.0

        return float(active_months / total_months)

    def _status_impact(self):
        df = self.df.copy()

        monthly = (
            df.groupby(["month", "own_channel_active"], as_index=False)
            .agg(units=("units", "sum"))
        )

        active = monthly[monthly["own_channel_active"] == 1]["units"].mean()
        suspended = monthly[monthly["own_channel_active"] == 0]["units"].mean()

        if active == 0:
            return 0.0

        return float((suspended - active) / active)

    def _status_impact_normalized(self):
        df = self.df.copy()
        df["quarter"] = df["month"].dt.quarter

        monthly = (
            df.groupby(["month", "own_channel_active", "quarter"], as_index=False)
            .agg(units=("units", "sum"))
        )

        by_q = (
            monthly.groupby(["own_channel_active", "quarter"], as_index=False)
            .agg(avg_units=("units", "mean"))
        )

        active = by_q[by_q["own_channel_active"] == 1]["avg_units"].mean()
        suspended = by_q[by_q["own_channel_active"] == 0]["avg_units"].mean()

        if active == 0:
            return 0.0

        return float((suspended - active) / active)
    
    def _amazon_active_months(self):
        df = self.df.copy()

        monthly = (
            df.groupby("month", as_index=False)
            .agg(units=("units", "sum"))
        )

        return int((monthly["units"] > 0).sum())


# AGGREGATIONS
class AggregationAnalyzer(BaseAnalyzer):

    def by_product(self):
        return (
            self.df.groupby("book", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def by_region(self):
        return (
            self.df.groupby("region", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )

    def by_month(self):
        return self._amazon_monthly().sort_values("month")
    
    def _amazon_monthly(self):
        return (
            self.df.groupby("month", as_index=False)
                .agg(total_units=("units", "sum"))
            )

    def seasonality(self):
        df = self._amazon_monthly()

        df["quarter"] = df["month"].dt.quarter

        return (
            df.groupby("quarter", as_index=False)
                .agg(avg_units=("total_units", "mean"))
                .sort_values("quarter")
        )


# CANNIBALIZATION / EFFECT ANALYSIS
class CannibalizationAnalyzer(BaseAnalyzer):

    def _amazon_start(self):
        df = self.df.copy()
        df = df[df["units"] > 0]
        return df["month"].min()

    def impact_summary(self):
        df = self.df.copy()

        monthly = (
            df.groupby(["month", "own_channel_active"], as_index=False)
            .agg(units=("units", "sum"))
        )

        stats = (
            monthly.groupby("own_channel_active")
            .agg(
                total_units=("units", "sum"),
                months=("month", "nunique")
            )
            .reset_index()
        )

        stats["avg_per_month"] = stats["total_units"] / stats["months"]

        active = stats[stats["own_channel_active"] == 1]["avg_per_month"].values
        suspended = stats[stats["own_channel_active"] == 0]["avg_per_month"].values

        if len(active) == 0 or len(suspended) == 0:
            return {
                "ratio": 1.0,
                "impact_index": 100,
                "insight": "Insufficient data"
            }

        active = active[0]
        suspended = suspended[0]

        ratio = suspended / active if active != 0 else 0

        return {
            "active_avg": float(active),
            "suspended_avg": float(suspended),
            "ratio": float(ratio),
            "impact_index": float(ratio * 100),

            "insight": (
                "No JDG impact on Amazon sales"
                if ratio >= 1 else
                "Possible cannibalization effect"
            )
        }

    def sales_by_channel_status(self):
        return (
            self.df.groupby("channel_status", as_index=False)
            .agg(total_units=("units", "sum"))
            .sort_values("total_units", ascending=False)
        )
