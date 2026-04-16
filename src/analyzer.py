"""
Business logic for aggregations and KPIs
"""

class SalesAnalyzer:
    def __init__(self, df_sales):
        self.df = df_sales.copy() # defensive copy
        
        required = ["date", "title", "asin", "marketplace", "units"]
        missing = []
        for c in required:
            if c not in self.df.columns:
                missing.append(c)
        
        if missing:
            raise ValueError(f"SalesAnalyzer: missing required columns {missing}")
        
        self.df = self.df[self.df["date"].notna()]

        self._add_shorttitle()
        self._add_region()

    def _add_shorttitle(self):
        asin_map = {
            8394291341: "dla psów",
            8394291333: "dla kotów",
            8394291368: "for dogs"
        }
        self.df["shorttitle"] = self.df["asin"].map(asin_map)
    
    def _add_region(self):
        self.df["region"] = (
            self.df["marketplace"]
            .str.split(".").str[-1]
            .str.upper()
            .replace({"COM": "US"})  # exception for Amazon.com
        )
    
    def kpis(self):
        out = {}
        out["total_units"] = int(self.df["units"].sum())
        out["distinct_products"] = int(self.df["asin"].nunique())
        out["distinct_regions"] = int(self.df["region"].nunique())
        return out

    def by_product(self):
        agg = (
            self.df.groupby("shorttitle", as_index=False)
               .agg(units_sum=("units", "sum"))
               .sort_values("units_sum", ascending=False)
        )
        return agg
    
    def by_region(self):
        agg = (
            self.df.groupby("region", as_index=False)
               .agg(units_sum=("units", "sum"))
               .sort_values("units_sum", ascending=False)
        )
        return agg
    
    def by_month(self):
        self.df["month"] = self.df["date"].dt.to_period("M").dt.to_timestamp()
        agg = (
            self.df.groupby("month", as_index=False)
               .agg(units_sum=("units", "sum"))
               .sort_values("month")
        )
        return agg
    
    def by_quarter(self):
        # sales seasonality
        self.df["quarter"] = self.df["date"].dt.quarter

        agg = (
            self.df.groupby("quarter", as_index=False)
            .agg(units_sum=("units", "sum"))
            .sort_values("units_sum", ascending=False)
        )
        return agg
