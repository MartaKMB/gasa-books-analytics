from loader import Loader
# from cleaner import Cleaner
# from analyzer import SalesAnalyzer
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
