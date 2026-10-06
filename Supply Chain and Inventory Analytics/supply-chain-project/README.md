# Supply Chain & Inventory Analytics

An end-to-end analytics project on the DataCo Smart Supply Chain dataset: raw CSV, cleaned and modelled with Python and MySQL, and presented in a three-page Power BI dashboard.

**Pipeline:** Kaggle CSV -> Python (pandas) -> MySQL (star schema + views) -> Power BI

## Business questions
1. How are sales and profit performing across markets and departments?
2. How often are orders delivered late, and what drives it?
3. Which products drive most of the revenue (ABC analysis)?

## Tech stack
- **Python 3.12**: pandas, SQLAlchemy, PyMySQL (cleaning, feature engineering, loading)
- **MySQL 8**: star schema, keys and indexes, analytical views (CTEs, window functions)
- **Power BI Desktop**: data model, DAX measures, interactive dashboard

## Dataset
DataCo Smart Supply Chain data from Kaggle: 180,519 order lines, 65,752 orders, 118 products, 20,652 customers, January 2015 to January 2018.
The CSV is not included in this repository because of its size. Download `DataCoSupplyChainDataset.csv` from Kaggle and place it in `data/`.

## Data model
Star schema with one fact table and four dimensions.

| Table | Description |
|---|---|
| `fact_orders` | One row per order line: sales, profit, quantity, discount, shipping days, `is_late` flag, delay in days |
| `dim_customer` | Customer name, segment, city, state, country |
| `dim_product` | Product, category, price |
| `dim_department` | Department |
| `dim_date` | Calendar table (year, quarter, month, weekday) |

Views used for analysis: `vw_monthly_sales` (monthly trend with month-over-month growth), `vw_delivery_performance` (late rate by market, region and shipping mode) and `vw_product_abc` (ABC classification using a running revenue share).

Personal data columns (email, password, street, zip code) are dropped during loading.

## Project structure
```
supply-chain-project/
├── data/                   # place the Kaggle CSV here (not committed)
├── docs/                   # insights.md, dashboard screenshots
├── notebooks/              # exploratory analysis
├── powerbi/                # supply-chain.pbix
├── sql/
│   ├── 01_keys_indexes.sql
│   └── 02_views.sql
├── load_dataco.py          # clean + build star schema + load to MySQL
└── check_totals.py         # reconciles pandas totals against MySQL
```

## How to run
1. Install the requirements: `pip install pandas sqlalchemy pymysql`
2. Create the database in MySQL: `CREATE DATABASE supply_chain;`
3. Place the CSV in `data/` and run `python load_dataco.py`. It prompts for your MySQL password, so no credentials are stored in the code.
4. Run `sql/01_keys_indexes.sql`, then `sql/02_views.sql`, in MySQL Workbench.
5. Open `powerbi/supply-chain.pbix` in Power BI Desktop and refresh. Enter the MySQL credentials if prompted (server `localhost`, database `supply_chain`).

Validation: total sales of 36,784,735.01 and total profit of 3,966,902.97 match between pandas and MySQL.

## Dashboard
**Page 1: Executive Overview.** KPI cards, monthly sales and profit trend, sales by market and department.
![Executive Overview](docs/page1_executive_overview.png)

**Page 2: Delivery Performance.** On-time and late rates, late rate by shipping mode and region, delivery status, market-by-mode heat map.
![Delivery Performance](docs/page2_delivery_performance.png)

**Page 3: Product Analysis.** ABC classification, top 10 products, revenue vs profit, sales by category.
![Product Analysis](docs/page3_product_analysis.png)

## Key findings
- Sales of **$36.8M** and profit of **$4.0M** (10.8% margin) across 65,752 orders; average order value $559.
- Fan Shop is the largest department at about 46% of sales.
- Only **42.7%** of order lines are delivered on time. **Shipping mode drives lateness, not geography**: First Class is 100% late, Second Class about 80%, Same Day about 48% and Standard Class about 40%, while every market sits near 57%.
- **7 of 118 products (about 6%) generate about 77% of revenue**; 95 products make up only about 5%.

Full write-up, recommendations and data caveats: [docs/insights.md](docs/insights.md).

## Limitations
- The dataset contains orders but no stock-level table, so inventory conclusions are demand-based proxies (sales velocity and ABC class), not actual stock levels.
- "Late" means actual shipping days exceed scheduled days. The dataset's own `delivery_status` field uses a different definition (54.82% "Late delivery").
- Sales per order fall sharply from late 2017 while order counts hold up, so the final months should be read with caution.

## Author
Siddhant Singh, [GitHub](https://github.com/your-username)
