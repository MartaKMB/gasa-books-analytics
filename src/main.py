from loader import Loader
from cleaner import Cleaner
from analyzer import SalesAnalyzer
import visualizer as viz
import os

# 1) Load
loader = Loader(data_dir="data")

try:
    amazon_sales, own_sales = loader.load_all()
except Exception as e:
    print("Data loading error: ", e)
    raise SystemExit(1)

# 2) Clean
cleaner = Cleaner()
sales = cleaner.clean_sales(amazon_sales)
own_sales = cleaner.clean_jdg(own_sales)
sales_enriched = cleaner.enrich_sales_with_own_activity(sales, own_sales)

# 3) Analyze
analyzer = SalesAnalyzer(sales_enriched)
kpis = analyzer.kpis()
by_prod = analyzer.by_product()
by_reg = analyzer.by_region()
by_month = analyzer.by_month()
check_impact = analyzer.amazon_vs_jdg()
seasonality = analyzer.seasonality_check()

# 4) Visualyze
os.makedirs("reports/figures", exist_ok=True)

out = viz.save_dashboard(
    df_by_product=by_prod,
    df_by_region=by_reg,
    df_by_month=by_month,
    df_impact=check_impact,
    df_seasonality=seasonality,
    kpis=kpis,
    n_top=3,
    out_dir="reports/figures",
    filename="dashboard.png"
)
