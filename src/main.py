"""
Expected input file(CSV):
- amazon_sales.csv  [columns: Date, Title, ASIN, Marketplace, Units]
- own_channel_activity.csv  [columns: Miesiac, JDG]
"""

from loader import Loader
from cleaner import Cleaner
from analyzer import AggregationAnalyzer, CannibalizationAnalyzer, KPIAnalyzer
import visualizer as viz
import os

# 1. LOAD
loader = Loader(data_dir="data")
try:
    amazon_sales, own_activity = loader.load_all()
except Exception as e:
    print("Data loading error: ", e)
    raise SystemExit(1)

# 2. CLEAN
cleaner = Cleaner()

sales_raw = cleaner.clean_sales(amazon_sales)
jdg = cleaner.clean_jdg(own_activity)

sales_detailed = cleaner.enrich_sales_with_own_activity_raw(sales_raw, jdg)
sales_ts = cleaner.enrich_sales_with_own_activity(sales_raw, jdg)

# 3. ANALYSIS
kpi_analyzer = KPIAnalyzer(sales_ts, sales_detailed)
agg_analyzer = AggregationAnalyzer(sales_detailed)
cannibal_analyzer = CannibalizationAnalyzer(sales_ts)

kpis = kpi_analyzer.kpis()

by_product = agg_analyzer.by_product()
by_region = agg_analyzer.by_region()

by_month = agg_analyzer.by_month()
seasonality = agg_analyzer.seasonality()

rolling_trend = cannibal_analyzer.rolling_trend()
jdg_timeseries = cannibal_analyzer.jdg_time_series()

impact = cannibal_analyzer.impact_summary()

# 4. VISUALIZATION
os.makedirs("reports/figures", exist_ok=True)

out = viz.save_dashboard(
    df_by_product=by_product,
    df_by_region=by_region,
    df_by_month=rolling_trend,
    df_own_impact=jdg_timeseries,
    df_seasonality=seasonality,
    kpis=kpis,
    n_top=3,
    out_dir="reports/figures",
    filename="dashboard.png"
)

# 5. OUTPUT
print("\n=== JDG IMPACT ===")
print(impact)

print("\nDashboard saved to:", out)
