import pandas as pd

df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding="latin-1")
print("Total sales:", round(df["Sales"].sum(), 2))
print("Total profit:", round(df["Order Profit Per Order"].sum(), 2))
