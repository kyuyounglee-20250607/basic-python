import pandas as pd
url = 'https://raw.githubusercontent.com/kyuyounglee-20250607/basic-python/refs/heads/main/day09_regression/clean_sales_data.csv'
df = pd.read_csv(url)
print(df)