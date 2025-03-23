import pandas as pd

# Load the dataset
df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

# Clean price and original price columns by removing currency symbols and commas
def clean_price(value):
    if isinstance(value, str):
        return value.replace("US $", "").replace(",", "").strip()
    return value


df["price"] = df["price"].apply(clean_price)
df["original price"] = df["original price"].apply(clean_price)


df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["original price"] = pd.to_numeric(df["original price"], errors="coerce")


df["original price"] = df["original price"].fillna(df["price"])


print(df[["price", "original price"]].isna().sum())


# df = df.dropna(subset=["price", "original price"])
# df = df[df["original price"] != 0]


df["discount_percentage"] = (1 - (df["price"] / df["original price"])) * 100


df["discount_percentage"] = df["discount_percentage"].round(2)


df.to_csv("cleaned_ebay_deals.csv", index=False)


print(df[["price", "original price", "discount_percentage"]].head(20))
