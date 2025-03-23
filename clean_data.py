import pandas as pd

df = pd.read_csv('ebay_tech_deals.csv',  dtype=str)

df["price"] = df["price"].str.replace(r'[$,]', '', regex=True).str.strip()
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df["original price"] = df["original price"].apply(lambda x: x.split("|")[0] if "|" in str(x) else x)
df["original price"] = df["original price"].str.replace(r'[$,]', '', regex=True).str.strip()
df["original price"] = pd.to_numeric(df["original price"], errors="coerce")

df["discount_percentage"] = ((1 - df["price"] / df["original price"]) * 100).round(2)
df.to_csv('cleaned_ebay_deals.csv', index=False)