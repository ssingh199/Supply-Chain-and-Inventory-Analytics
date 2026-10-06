# Supply Chain & Inventory Analytics: Key Insights

Dataset: DataCo Smart Supply Chain (Kaggle). Pipeline: CSV -> Python (pandas) -> MySQL (star schema) -> Power BI.
Coverage: January 2015 to January 2018, 180,519 order lines, 65,752 orders, 118 products, 20,652 customers.

## 1. Business overview
- Total sales: **$36.78M**. Total profit: **$3.97M**. Profit margin: **10.8%**.
- Average order value: **$559**. Units sold: about 384K.
- Fan Shop is the largest department at about **$17.1M (roughly 46% of sales)**, followed by Apparel ($8.0M), Golf ($4.6M) and Footwear ($4.0M).
- Europe and LATAM are the strongest markets. Africa is the smallest.

## 2. Delivery performance
- Only **42.7%** of order lines arrive on or before the scheduled date. **57.28%** arrive late.
- **Shipping mode drives lateness, not geography.**

| Shipping mode | Late % |
|---|---|
| First Class | 100% |
| Second Class | about 80% |
| Same Day | about 48% |
| Standard Class | about 40% |

- Late rates are nearly identical across markets (56.8% to 57.7%) and regions (about 58% to 60%), so location is not the cause.
- First Class averages about 1 day late and Second Class about 2 days late. A 100% late rate with a steady delay suggests the promised delivery time is set too tight for these services. This should be confirmed against the scheduled-days field before acting on it.

## 3. Product concentration (ABC analysis)
- **7 of 118 products (about 6%) generate about 77% of revenue** (class A, $28.3M).
- 16 class B products add about 18% ($6.65M).
- 95 class C products together add only about 5% ($1.86M).
- Profit rises almost in proportion to revenue across the top products, at roughly 11% margin, so no major seller looks like a high-volume, low-margin problem. This is read from the scatter chart and should be confirmed with a per-product margin measure.

## 4. Recommendations (suggested actions)
1. **Reset or fix First Class and Second Class delivery promises.** Either lengthen the quoted delivery time or improve carrier performance. These two modes account for the worst lateness.
2. **Protect the 7 class A products.** Prioritise their stock availability and supplier reliability, because they carry most of the revenue.
3. **Review the long tail of class C products.** 95 products contribute about 5% of revenue, so consider rationalising range or reducing the stock held for them.
4. **Investigate Standard Class.** At about 40% late it is the best mode but still far from a good on-time rate.

## 5. Data notes and limitations
- Sales fall sharply after September 2017, from about $1.14M to about $0.33M in January 2018, but order volume does not fall: it rises from about 1,700 orders a month in mid-2017 to about 2,100 a month from October 2017. The drop is therefore in revenue per order (about $664 in September 2017 versus about $156 in January 2018), not in the number of orders. The cause has not been determined, so the late-2017 months should be read with caution and the Year slicer should not be used to draw trend conclusions from them.
- "Late" in this project means actual shipping days exceed scheduled shipping days. The dataset's own `delivery_status` field reports 54.82% "Late delivery", which uses a different definition and includes cancelled orders. Headline figures use the first definition.
- The dataset has orders but no stock-level table, so inventory conclusions are demand-based proxies (sales velocity and ABC class), not actual inventory levels.
