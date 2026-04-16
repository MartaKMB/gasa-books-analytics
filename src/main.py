from loader import Loader
from cleaner import Cleaner
from analyzer import SalesAnalyzer
# import visualizer as viz
import os

# 1) Load
print(os.getcwd())
loader = Loader(data_dir="data")

try:
    amazon_sales = loader.load_sales()
except Exception as e:
    print("Data loading error: ", e)
    raise SystemExit(1)

# 2) Clean
cleaner = Cleaner()
sales = cleaner.clean_sales(amazon_sales)

# 3) Analyze
analyzer = SalesAnalyzer(sales)
kpis = analyzer.kpis()
by_prod = analyzer.by_product()
by_reg = analyzer.by_region()
by_month = analyzer.by_month()
by_month = analyzer.by_quarter()
