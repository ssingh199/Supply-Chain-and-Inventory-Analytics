import re
import getpass
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = "data/DataCoSupplyChainDataset.csv"
DB_USER = "root"
DB_HOST = "localhost"
DB_NAME = "supply_chain"

password = getpass.getpass("MySQL password: ")
DB_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(password)}@{DB_HOST}:3306/{DB_NAME}"

# ---------- 1. Read + normalise column names ----------
df = pd.read_csv(CSV_PATH, encoding="latin-1")


def snake(c):
    return re.sub(r"[^0-9a-zA-Z]+", "_", c.strip()).strip("_").lower()


df.columns = [snake(c) for c in df.columns]
print("Rows:", len(df), "| Columns:", len(df.columns))

# ---------- 2. Drop PII / useless columns ----------
drop_cols = [
    "customer_email", "customer_password", "customer_street",
    "customer_zipcode", "product_description", "product_image", "order_zipcode",
]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

# ---------- 3. Types + derived metrics ----------
df["order_date"] = pd.to_datetime(
    df["order_date_dateorders"], format="%m/%d/%Y %H:%M", errors="coerce"
)
df["shipping_date"] = pd.to_datetime(
    df["shipping_date_dateorders"], format="%m/%d/%Y %H:%M", errors="coerce"
)
df["shipping_delay_days"] = (
    df["days_for_shipping_real"] - df["days_for_shipment_scheduled"]
)
df["is_late"] = (df["shipping_delay_days"] > 0).astype(int)

df = df.drop_duplicates(subset="order_item_id")
print("Null dates:", df[["order_date", "shipping_date"]].isna().sum().to_dict())

# ---------- 4. Build star schema ----------
dim_customer = (
    df[["customer_id", "customer_fname", "customer_lname", "customer_segment",
        "customer_city", "customer_state", "customer_country"]]
    .drop_duplicates("customer_id")
)

dim_product = (
    df[["product_card_id", "product_name", "product_category_id", "category_name",
        "product_price", "product_status"]]
    .drop_duplicates("product_card_id")
)

dim_department = df[["department_id", "department_name"]].drop_duplicates("department_id")

dates = pd.date_range(df["order_date"].min().normalize(),
                      df["order_date"].max().normalize(), freq="D")
dim_date = pd.DataFrame({"date": dates})
dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["date"].dt.year
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.month_name()
dim_date["day_of_week"] = dim_date["date"].dt.day_name()

fact_cols = [
    "order_item_id", "order_id", "order_date", "shipping_date", "customer_id",
    "product_card_id", "department_id", "shipping_mode", "delivery_status",
    "late_delivery_risk", "days_for_shipping_real", "days_for_shipment_scheduled",
    "shipping_delay_days", "is_late", "order_status", "type", "market",
    "order_region", "order_country", "order_state", "order_city",
    "order_item_quantity", "order_item_product_price", "order_item_discount",
    "order_item_discount_rate", "sales", "order_item_total",
    "order_item_profit_ratio", "order_profit_per_order",
]
fact_orders = df[[c for c in fact_cols if c in df.columns]].copy()
fact_orders["date_key"] = fact_orders["order_date"].dt.strftime("%Y%m%d").astype("Int64")

# ---------- 5. Load into MySQL ----------
engine = create_engine(DB_URL)
tables = {
    "dim_customer": dim_customer,
    "dim_product": dim_product,
    "dim_department": dim_department,
    "dim_date": dim_date,
    "fact_orders": fact_orders,
}
for name, frame in tables.items():
    frame.to_sql(name, engine, if_exists="replace", index=False,
                 chunksize=5000, method="multi")
    print(f"Loaded {name}: {len(frame):,} rows")

print("Done.")