# energy

UK energy grid data analysis. Focused on NESO operating margin data during summer 2026 heatwaves.

## Data sources

All data from [NESO Data Portal](https://www.neso.energy/data-portal):

| File | Source | Description |
|------|--------|-------------|
| `opmr_daily.csv` | [Daily OPMR](https://api.neso.energy/dataset/8e0c417f-ee54-4c8b-8ed2-0d64b042c6ed/resource/0eede912-8820-4c66-a58a-f7436d36b95f/download/csv_opmr_daily.csv) | Daily operating margin: peak demand forecast, generator availability, national surplus |
| `demand_2025.csv` | [Historic Demand 2025](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/b2bde559-3455-4021-b179-dfe60c0337b0/download/demanddata_2025.csv) | Half-hourly demand outturn: ND, TSD, interconnector flows, embedded wind/solar |
| `demand_2026.csv` | [Historic Demand 2026](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/8a4a771c-3929-4e56-93ad-cdf13219dea5/download/demanddataupdate_2026.csv) | Same, updated daily (~21 days in arrears) |
| `demand_forecast_archive.csv` | [Day Ahead Demand Forecast](https://api.neso.energy/dataset/8fbc8a09-06af-4c90-886f-d3025d38a349/resource/9847e7bb-986e-49be-8138-717b25933fbb/download/archive_1dayahead.csv) | Historic day-ahead demand forecasts with cardinal points |

## Setup

```bash
uv sync
```

## Download raw data

Raw CSVs are gitignored. Download with:

```bash
mkdir -p data/raw
curl -sL "https://api.neso.energy/dataset/8e0c417f-ee54-4c8b-8ed2-0d64b042c6ed/resource/0eede912-8820-4c66-a58a-f7436d36b95f/download/csv_opmr_daily.csv" -o data/raw/opmr_daily.csv
curl -sL "https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/b2bde559-3455-4021-b179-dfe60c0337b0/download/demanddata_2025.csv" -o data/raw/demand_2025.csv
curl -sL "https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/8a4a771c-3929-4e56-93ad-cdf13219dea5/download/demanddataupdate_2026.csv" -o data/raw/demand_2026.csv
curl -sL "https://api.neso.energy/dataset/8fbc8a09-06af-4c90-886f-d3025d38a349/resource/9847e7bb-986e-49be-8138-717b25933fbb/download/archive_1dayahead.csv" -o data/raw/demand_forecast_archive.csv
```

## Clean data

Filters to June–July 2026, normalizes column names, writes parquet:

```bash
uv run python main.py
```

Output in `data/clean/`:

- `opmr_daily.parquet` - daily operating margin and national surplus
- `demand.parquet` - half-hourly demand outturn (through June 25, ~21 days arrears)
- `demand_forecast.parquet` - day-ahead demand forecasts
