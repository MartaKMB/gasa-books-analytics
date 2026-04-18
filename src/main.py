from loader import Loader
from cleaner import Cleaner
from analyzer import KPIAnalyzer, AggregationAnalyzer, CannibalizationAnalyzer
import visualizer as viz
import os

# 1) Load
loader = Loader(data_dir="data")

try:
    amazon_sales, own_activity = loader.load_all()
except Exception as e:
    print("Data loading error: ", e)
    raise SystemExit(1)

# 2) Clean
cleaner = Cleaner()
sales = cleaner.clean_sales(amazon_sales)
own_activity = cleaner.clean_jdg(own_activity)
sales_enriched = cleaner.enrich_sales_with_own_activity(sales, own_activity)

# 3) Analyze
kpi_analyzer = KPIAnalyzer(sales_enriched)
agg_analyzer = AggregationAnalyzer(sales_enriched)
cannibal_analyzer = CannibalizationAnalyzer(sales_enriched)

kpis = kpi_analyzer.kpis()
activity_stats = kpi_analyzer.activity_split(own_activity)
kpis.update(activity_stats)

by_prod = agg_analyzer.by_product()
by_reg = agg_analyzer.by_region()
by_month = agg_analyzer.by_month()
seasonality_impact = agg_analyzer.seasonality()
own_activity_impact = cannibal_analyzer.sales_by_channel_status()

# 4) Visualyze
os.makedirs("reports/figures", exist_ok=True)

out = viz.save_dashboard(
    df_by_product=by_prod,
    df_by_region=by_reg,
    df_by_month=by_month,
    df_own_impact=own_activity_impact,
    df_seasonality=seasonality_impact,
    kpis=kpis,
    n_top=3,
    out_dir="reports/figures",
    filename="dashboard.png"
)
