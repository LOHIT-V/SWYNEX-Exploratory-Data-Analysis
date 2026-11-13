import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "SWYNEX-cleaned-retail-sales.csv"
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_FILE)
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
sales = df.dropna(subset=["Total Spent"]).copy()
sales["Year"] = sales["Transaction Date"].dt.year

# Summary statistics
total_rows = len(df)
valid_sales_rows = int(df["Total Spent"].notna().sum())
missing_sales_rows = int(df["Total Spent"].isna().sum())
total_sales = float(sales["Total Spent"].sum())
average_transaction = float(sales["Total Spent"].mean())
median_transaction = float(sales["Total Spent"].median())
unique_customers = int(df["Customer ID"].nunique())

category_sales = sales.groupby("Category")["Total Spent"].sum().sort_values(ascending=False)
location_sales = sales.groupby("Location")["Total Spent"].sum().sort_values(ascending=False)
payment_sales = sales.groupby("Payment Method")["Total Spent"].sum().sort_values(ascending=False)
year_sales = sales.groupby("Year")["Total Spent"].sum().sort_index()

# Potential outliers using the IQR rule (investigate; do not delete automatically)
q1 = float(sales["Total Spent"].quantile(0.25))
q3 = float(sales["Total Spent"].quantile(0.75))
iqr = q3 - q1
upper_fence = q3 + 1.5 * iqr
potential_outliers = sales[sales["Total Spent"] > upper_fence]

# Chart 1: category sales
plt.figure(figsize=(10, 6))
category_sales.sort_values().plot(kind="barh")
plt.title("Total Sales by Product Category")
plt.xlabel("Total Spent")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "sales_by_category.png"), dpi=160)
plt.close()

# Chart 2: sales by purchase location
plt.figure(figsize=(7, 5))
location_sales.plot(kind="bar")
plt.title("Total Sales by Purchase Location")
plt.xlabel("Location")
plt.ylabel("Total Spent")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "sales_by_location.png"), dpi=160)
plt.close()

# Chart 3: sales by payment method
plt.figure(figsize=(8, 5))
payment_sales.plot(kind="bar")
plt.title("Total Sales by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Total Spent")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "sales_by_payment_method.png"), dpi=160)
plt.close()

# Chart 4: yearly sales
plt.figure(figsize=(8, 5))
year_sales.plot(kind="bar")
plt.title("Recorded Sales by Year")
plt.xlabel("Year")
plt.ylabel("Total Spent")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "sales_by_year.png"), dpi=160)
plt.close()

with open("EDA-REPORT.md", "w", encoding="utf-8") as f:
    f.write("# Exploratory Data Analysis – Retail Store Sales\n\n")
    f.write("## Dataset overview\n")
    f.write(f"- Rows: {total_rows:,}\n- Columns: {df.shape[1]}\n")
    f.write(f"- Unique customers: {unique_customers:,}\n")
    f.write(f"- Transactions with recorded Total Spent: {valid_sales_rows:,}\n")
    f.write(f"- Transactions with missing Total Spent: {missing_sales_rows:,}\n\n")
    f.write("## Descriptive statistics\n")
    f.write(f"- Total recorded sales: {total_sales:,.2f}\n")
    f.write(f"- Mean recorded transaction value: {average_transaction:,.2f}\n")
    f.write(f"- Median recorded transaction value: {median_transaction:,.2f}\n\n")
    f.write("## Key findings\n")
    f.write(f"1. **Highest-sales category:** {category_sales.index[0]} recorded {category_sales.iloc[0]:,.2f} in sales.\n")
    f.write(f"2. **Lowest-sales category:** {category_sales.index[-1]} recorded {category_sales.iloc[-1]:,.2f} in sales.\n")
    f.write(f"3. **Purchase location:** {location_sales.index[0]} recorded {location_sales.iloc[0]:,.2f}, compared with {location_sales.iloc[-1]:,.2f} for {location_sales.index[-1]}.\n")
    f.write(f"4. **Payment method:** {payment_sales.index[0]} had the highest recorded sales at {payment_sales.iloc[0]:,.2f}.\n")
    full_years = year_sales.drop(index=[2025], errors="ignore")
    if len(full_years):
        best_year = int(full_years.idxmax())
        f.write(f"5. **Highest full-year sales:** {best_year} recorded {full_years.max():,.2f} among the complete calendar years in the dataset.\n")
    f.write("\n## Data quality and limitations\n")
    f.write(f"- {missing_sales_rows:,} rows have missing `Total Spent`; they are excluded from sales totals and averages.\n")
    f.write(f"- {int(df['Quantity'].isna().sum()):,} rows have missing `Quantity`.\n")
    f.write("- Missing values are not guessed or artificially filled during EDA.\n")
    f.write("- 2025 contains only partial-year data in this dataset, so it is not compared directly with full calendar years.\n")
    f.write("- Sales figures describe recorded `Total Spent` values; they do not establish profit because costs are not provided.\n\n")
    f.write("## Visualizations\n")
    f.write("- `charts/sales_by_category.png`\n- `charts/sales_by_location.png`\n- `charts/sales_by_payment_method.png`\n- `charts/sales_by_year.png`\n")

print("EDA complete")
print(f"Rows: {total_rows}; columns: {df.shape[1]}")
print(f"Recorded sales: {total_sales:.2f}; valid sales rows: {valid_sales_rows}")
print(f"Missing Total Spent: {missing_sales_rows}")
print(f"Top category: {category_sales.index[0]} ({category_sales.iloc[0]:.2f})")
print(f"Top location: {location_sales.index[0]} ({location_sales.iloc[0]:.2f})")
print(f"Top payment method: {payment_sales.index[0]} ({payment_sales.iloc[0]:.2f})")
print(f"Potential high-value outliers (IQR): {len(potential_outliers)}; upper fence: {upper_fence:.2f}")
