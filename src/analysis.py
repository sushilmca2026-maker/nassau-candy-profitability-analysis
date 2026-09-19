"""Reusable data preparation and profitability analytics for Nassau Candy."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID",
    "Country/Region", "City", "State/Province", "Postal Code", "Division", "Region",
    "Product ID", "Product Name", "Sales", "Units", "Gross Profit", "Cost",
]
NUMERIC_COLUMNS = ["Sales", "Units", "Gross Profit", "Cost"]
FACTORIES = {
    "Lot's O' Nuts": {"Latitude": 32.881893, "Longitude": -111.768036},
    "Wicked Choccy's": {"Latitude": 32.076176, "Longitude": -81.088371},
    "Sugar Shack": {"Latitude": 48.11914, "Longitude": -96.18115},
    "Secret Factory": {"Latitude": 41.446333, "Longitude": -90.565487},
    "The Other Factory": {"Latitude": 35.1175, "Longitude": -89.971107},
}
PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack", "SweeTARTS": "Sugar Shack", "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack", "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory", "Fizzy Lifting Drinks": "Sugar Shack",
    "Lickable Wallpaper": "Secret Factory", "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}


def clean_data(path: str | Path) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Load, validate, standardize, and enrich the uploaded dataset."""
    raw = pd.read_csv(path)
    missing_required = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")
    df = raw[REQUIRED_COLUMNS].copy()
    initial_rows = len(df)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["Division", "Product Name", "Region", "Ship Mode", "State/Province", "City"]:
        df[col] = df[col].astype("string").str.strip()
    invalid_numeric = df[NUMERIC_COLUMNS].isna().any(axis=1)
    invalid_sales = df["Sales"].fillna(0) <= 0
    invalid_units = df["Units"].fillna(0) <= 0
    invalid_dates = df["Order Date"].isna()
    invalid = invalid_numeric | invalid_sales | invalid_units | invalid_dates
    duplicates = int(df.duplicated().sum())
    df = df.loc[~invalid].drop_duplicates().copy()
    # Reconcile to the supplied gross profit where possible, while retaining an auditable check.
    df["Calculated Gross Profit"] = df["Sales"] - df["Cost"]
    df["Profit Check Difference"] = df["Gross Profit"] - df["Calculated Gross Profit"]
    df["Gross Margin %"] = np.where(df["Sales"] != 0, df["Gross Profit"] / df["Sales"] * 100, 0.0)
    df["Profit per Unit"] = np.where(df["Units"] != 0, df["Gross Profit"] / df["Units"], 0.0)
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    df["Revenue Contribution %"] = np.where(total_sales != 0, df["Sales"] / total_sales * 100, 0.0)
    df["Profit Contribution %"] = np.where(total_profit != 0, df["Gross Profit"] / total_profit * 100, 0.0)
    df["Factory"] = df["Product Name"].map(PRODUCT_FACTORY).fillna("Unmapped")
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year
    stats = {
        "raw_rows": initial_rows, "clean_rows": len(df), "removed_rows": initial_rows - len(df),
        "duplicate_rows": duplicates, "invalid_rows": int(invalid.sum()),
        "missing_values_after_cleaning": int(df.isna().sum().sum()),
    }
    return df, stats


def aggregate_products(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["Product Name", "Division", "Sales", "Cost", "Units", "Gross Profit", "Gross Margin %", "Profit per Unit", "Revenue Contribution %", "Profit Contribution %", "Margin Risk", "Diagnostic", "Factory"])
    g = df.groupby(["Product Name", "Division", "Factory"], as_index=False).agg({"Sales":"sum", "Cost":"sum", "Units":"sum", "Gross Profit":"sum"})
    total_sales, total_profit = g["Sales"].sum(), g["Gross Profit"].sum()
    g["Gross Margin %"] = np.where(g["Sales"] != 0, g["Gross Profit"] / g["Sales"] * 100, 0.0)
    g["Profit per Unit"] = np.where(g["Units"] != 0, g["Gross Profit"] / g["Units"], 0.0)
    g["Revenue Contribution %"] = np.where(total_sales != 0, g["Sales"] / total_sales * 100, 0.0)
    g["Profit Contribution %"] = np.where(total_profit != 0, g["Gross Profit"] / total_profit * 100, 0.0)
    median_margin = float(g["Gross Margin %"].median()) if len(g) else 0.0
    median_sales = float(g["Sales"].median()) if len(g) else 0.0
    def classify(row):
        if row["Gross Margin %"] <= 0: return "Negative/zero margin"
        if row["Gross Margin %"] < median_margin and row["Sales"] >= median_sales: return "High sales / low margin"
        if row["Gross Profit"] >= g["Gross Profit"].median() and row["Gross Margin %"] >= median_margin: return "High profit / high margin"
        if row["Sales"] < median_sales and row["Gross Profit"] < g["Gross Profit"].median(): return "Low sales / low profit"
        return "Monitor"
    g["Margin Risk"] = g.apply(classify, axis=1)
    g["Diagnostic"] = g.apply(lambda r: "Review pricing/cost" if r["Gross Margin %"] < median_margin else "Healthy margin", axis=1)
    return g.sort_values("Gross Profit", ascending=False).reset_index(drop=True)


def aggregate_divisions(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame(columns=["Division", "Sales", "Cost", "Units", "Gross Profit", "Gross Margin %", "Profit per Unit", "Revenue Contribution %", "Profit Contribution %"])
    g = df.groupby("Division", as_index=False).agg({"Sales":"sum", "Cost":"sum", "Units":"sum", "Gross Profit":"sum"})
    total_sales, total_profit = g["Sales"].sum(), g["Gross Profit"].sum()
    g["Gross Margin %"] = np.where(g["Sales"] != 0, g["Gross Profit"] / g["Sales"] * 100, 0.0)
    g["Profit per Unit"] = np.where(g["Units"] != 0, g["Gross Profit"] / g["Units"], 0.0)
    g["Revenue Contribution %"] = np.where(total_sales != 0, g["Sales"] / total_sales * 100, 0.0)
    g["Profit Contribution %"] = np.where(total_profit != 0, g["Gross Profit"] / total_profit * 100, 0.0)
    return g.sort_values("Gross Profit", ascending=False).reset_index(drop=True)


def pareto(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    p = aggregate_products(df).sort_values(metric, ascending=False).copy()
    total = p[metric].sum() if not p.empty else 0
    p["Cumulative Value"] = p[metric].cumsum()
    p["Cumulative %"] = np.where(total != 0, p["Cumulative Value"] / total * 100, 0.0)
    return p


def margin_volatility(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame(columns=["Product Name", "Margin Volatility"])
    x = df.copy(); x["Margin"] = np.where(x["Sales"] != 0, x["Gross Profit"] / x["Sales"] * 100, 0)
    return x.groupby("Product Name", as_index=False)["Margin"].std().rename(columns={"Margin":"Margin Volatility"}).fillna(0)


def factory_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame(columns=["Factory", "Sales", "Cost", "Units", "Gross Profit", "Gross Margin %", "Products"])
    g = df.groupby("Factory", as_index=False).agg({"Sales":"sum", "Cost":"sum", "Units":"sum", "Gross Profit":"sum", "Product Name":pd.Series.nunique})
    g = g.rename(columns={"Product Name":"Products"})
    g["Gross Margin %"] = np.where(g["Sales"] != 0, g["Gross Profit"] / g["Sales"] * 100, 0.0)
    return g.sort_values("Gross Profit", ascending=False).reset_index(drop=True)


def validation_report(df: pd.DataFrame, stats: Dict[str, int]) -> pd.DataFrame:
    checks = [
        ("Required columns present", True, "All required source columns were found."),
        ("Rows retained after validation", len(df) > 0, f"{len(df):,} rows available for analysis."),
        ("Sales positive", bool((df["Sales"] > 0).all()) if len(df) else False, "No zero or negative sales remain."),
        ("Units positive", bool((df["Units"] > 0).all()) if len(df) else False, "No missing, zero, or negative units remain."),
        ("No missing values", int(df.isna().sum().sum()) == 0, f"{int(df.isna().sum().sum())} missing values after cleaning."),
        ("Factory mapping coverage", bool((df["Factory"] != "Unmapped").all()) if len(df) else False, f"{(df['Factory'] != 'Unmapped').mean() * 100:.1f}% of rows mapped."),
    ]
    return pd.DataFrame(checks, columns=["Check", "Passed", "Evidence"])

if __name__ == "__main__":
    import sys
    frame, info = clean_data(sys.argv[1] if len(sys.argv) > 1 else "data/NassauCandyDistributor.csv")
    print(info)
    print(aggregate_products(frame).to_string(index=False))
