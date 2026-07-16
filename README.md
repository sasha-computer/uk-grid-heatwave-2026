# uk-grid-heatwave-2026

How close did the UK grid come to breaking during the 2026 summer heatwaves?

## Data sources

- **NESO Data Portal** (https://www.neso.energy/data-portal) - daily operating margin, generator availability, peak demand forecast, national surplus
- **NESO Historic Demand Data** - half-hourly demand outturn, interconnector flows, embedded wind/solar generation
- **Open-Meteo ERA5** (https://open-meteo.com/) - daily max temperature for central England

## What's plotted

- **Native Surplus** - generator availability minus peak demand (MW), excluding imports
- **Operating Margin Requirement** - NESO's required safety buffer (MW), dynamic per day
- **Daily Max Temperature** - highest recorded temperature per day (°C)
- **Seconds to Midnight** - national surplus mapped to a Doomsday Clock-style countdown (0 surplus = midnight = power cut)
- **EMN markers** - blue dashed lines on dates NESO issued an Electricity Margin Notice (Jun 24, Jul 9)

## Setup

```bash
uv sync
mkdir -p data/raw
# Download raw CSVs from NESO (URLs in main.py)
uv run python main.py
python3 -m http.server 8765
open http://localhost:8765/index.html
```
