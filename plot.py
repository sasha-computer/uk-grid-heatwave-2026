"""Plot half-hourly demand data for June 1-25, 2026."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

OUT = Path("data/plots")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet("data/clean/demand.parquet")
df["datetime"] = df["settlement_date"] + pd.to_timedelta((df["settlement_period"] - 1) * 30, unit="m")

interconnectors = [
    "ifa_flow", "ifa2_flow", "britned_flow", "moyle_flow",
    "east_west_flow", "nemo_flow", "nsl_flow", "eleclink_flow",
    "viking_flow", "greenlink_flow",
]
df["interconnector_total"] = df[interconnectors].sum(axis=1)

fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=True)

ax1, ax2, ax3, ax4 = axes

ax1.plot(df["datetime"], df["nd"], color="#d62728", linewidth=0.8, label="National Demand")
ax1.set_ylabel("MW")
ax1.set_title("National Demand", fontweight="bold")
ax1.legend(loc="upper left", fontsize=9)
ax1.grid(True, alpha=0.3)

ax2.plot(df["datetime"], df["embedded_solar_generation"], color="#ff7f0e", linewidth=0.8, label="Solar")
ax2.plot(df["datetime"], df["embedded_wind_generation"], color="#2ca02c", linewidth=0.8, label="Wind")
ax2.set_ylabel("MW")
ax2.set_title("Embedded Generation (distribution-connected)", fontweight="bold")
ax2.legend(loc="upper left", fontsize=9)
ax2.grid(True, alpha=0.3)

ax3.plot(df["datetime"], df["interconnector_total"], color="#1f77b4", linewidth=0.8, label="Total Interconnector Flow (+ = import)")
ax3.axhline(0, color="grey", linewidth=0.5, linestyle="--")
ax3.set_ylabel("MW")
ax3.set_title("Interconnector Flows", fontweight="bold")
ax3.legend(loc="upper left", fontsize=9)
ax3.grid(True, alpha=0.3)

ax4.plot(df["datetime"], df["pump_storage_pumping"], color="#9467bd", linewidth=0.8, label="Pumped Storage Pumping")
ax4.fill_between(df["datetime"], df["non_bm_stor"], color="#8c564b", alpha=0.5, label="Non-BM STOR")
ax4.set_ylabel("MW")
ax4.set_title("Storage & Reserve", fontweight="bold")
ax4.legend(loc="upper left", fontsize=9)
ax4.grid(True, alpha=0.3)

for ax in axes:
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d Jun"))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

axes[0].set_title("GB Electricity Demand — Half-Hourly Outturn (1–25 June 2026)", fontsize=14, fontweight="bold", pad=15)

fig.tight_layout()
fig.subplots_adjust(top=0.93)

path = OUT / "demand_june2026.png"
fig.savefig(path, dpi=150)
print(f"Saved to {path}")
