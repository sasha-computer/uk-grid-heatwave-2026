"""Download and clean NESO daily grid data into tidy parquet files."""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
CLEAN = Path("data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)

HEATWAVE_START = "2026-06-01"
HEATWAVE_END = "2026-07-31"


def clean_opmr() -> pd.DataFrame:
    df = pd.read_csv(RAW / "opmr_daily.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")
    df["date"] = pd.to_datetime(df["date"])
    df["publish_date"] = pd.to_datetime(df["publish_date"])
    df = df[df["date"] >= HEATWAVE_START].copy()
    df.sort_values("date", inplace=True)
    df.to_parquet(CLEAN / "opmr_daily.parquet", index=False)
    print(f"opmr_daily: {len(df)} rows, {df['date'].min().date()} to {df['date'].max().date()}")
    return df


def clean_demand() -> pd.DataFrame:
    frames = []
    for f in ("demand_2025.csv", "demand_2026.csv"):
        path = RAW / f
        if path.exists():
            frames.append(pd.read_csv(path))
    df = pd.concat(frames, ignore_index=True)
    df.columns = df.columns.str.strip().str.lower()
    df["settlement_date"] = pd.to_datetime(df["settlement_date"])
    df = df[df["settlement_date"] >= HEATWAVE_START].copy()
    df.sort_values(["settlement_date", "settlement_period"], inplace=True)
    df.to_parquet(CLEAN / "demand.parquet", index=False)
    print(f"demand: {len(df)} rows, {df['settlement_date'].min().date()} to {df['settlement_date'].max().date()}")
    return df


def clean_forecast() -> pd.DataFrame:
    df = pd.read_csv(RAW / "demand_forecast_archive.csv")
    df.columns = df.columns.str.strip().str.lower()
    df["targetdate"] = pd.to_datetime(df["targetdate"])
    df["forecast_timestamp"] = pd.to_datetime(df["forecast_timestamp"], errors="coerce")
    df = df[df["targetdate"] >= HEATWAVE_START].copy()
    df.sort_values(["targetdate", "forecast_timestamp"], inplace=True)
    df.to_parquet(CLEAN / "demand_forecast.parquet", index=False)
    print(f"demand_forecast: {len(df)} rows, {df['targetdate'].min().date()} to {df['targetdate'].max().date()}")
    return df


def main():
    print("Cleaning NESO data...\n")
    clean_opmr()
    clean_demand()
    clean_forecast()
    print("\nDone. Clean files in data/clean/")


if __name__ == "__main__":
    main()
