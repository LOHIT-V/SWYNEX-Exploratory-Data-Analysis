# Exploratory Data Analysis – Retail Store Sales

## Dataset overview
- Rows: 12,575
- Columns: 11
- Unique customers: 25
- Transactions with recorded Total Spent: 11,971
- Transactions with missing Total Spent: 604

## Descriptive statistics
- Total recorded sales: 1,552,071.00
- Mean recorded transaction value: 129.65
- Median recorded transaction value: 108.50

## Key findings
1. **Highest-sales category:** Butchers recorded 208,118.00 in sales.
2. **Lowest-sales category:** Milk Products recorded 180,112.00 in sales.
3. **Purchase location:** Online recorded 791,401.00, compared with 760,670.00 for In-store.
4. **Payment method:** Cash had the highest recorded sales at 537,710.00.
5. **Highest full-year sales:** 2024 recorded 524,881.00 among the complete calendar years in the dataset.

## Data quality and limitations
- 604 rows have missing `Total Spent`; they are excluded from sales totals and averages.
- 604 rows have missing `Quantity`.
- Missing values are not guessed or artificially filled during EDA.
- 2025 contains only partial-year data in this dataset, so it is not compared directly with full calendar years.
- Sales figures describe recorded `Total Spent` values; they do not establish profit because costs are not provided.

## Visualizations
- `charts/sales_by_category.png`
- `charts/sales_by_location.png`
- `charts/sales_by_payment_method.png`
- `charts/sales_by_year.png`
