import pandas as pd
df = pd.read_csv('city_gas_month.csv')
print(df)
df.to_csv("clean_sales_data.csv", index=False, encoding='utf-8')