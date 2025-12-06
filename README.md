# ⚽ Moneyball Football Analytics

Advanced player scouting and value analysis application using **real football data from FBref**.

## Features

- 🎯 **Player Discovery**: Find undervalued players based on performance metrics
- 📊 **Advanced Statistics**: xG, xAG, progressive actions, defensive metrics
- 🔍 **Smart Filtering**: Filter by league, position, age, market value
- 💎 **Hidden Gems**: Identify best value-for-money players
- 📈 **Interactive Visualizations**: Performance charts and comparisons
- 🏆 **Top 5 European Leagues**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- ⚡ **Real Data**: Live data from FBref (StatsBomb)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Download Real Player Data

```bash
python download_real_data.py
```

This will download actual player statistics from FBref for the 2024-2025 season across Europe's top 5 leagues.

### Step 2: Run the Analytics App

```bash
streamlit run app.py
```

## Files

- `app.py` - Main Streamlit application with advanced analytics
- `download_real_data.py` - Download real player data from FBref
- `radar_charts.py` - Player comparison radar charts (optional)
- `players_real_data.csv` - Real player dataset from FBref
- `requirements.txt` - Python dependencies

## Tech Stack

- **Streamlit**: Web interface
- **Pandas**: Data manipulation
- **Matplotlib/Seaborn**: Visualizations
- **soccerdata**: Real football data from FBref
- **BeautifulSoup**: Web scraping fallback

## Moneyball Methodology

The app calculates a "Moneyball Score" for each player based on:
- Position-specific performance metrics
- Expected goals (xG) and assists (xAG)
- Progressive actions (carries, passes, receptions)
- Defensive contributions (tackles, interceptions, blocks)
- Passing accuracy and volume
- Market value efficiency (performance per €)

**Players with high scores at low market values represent the best value targets!**

## Data Sources

- **FBref.com** (StatsBomb): Player statistics
- Market values estimated based on performance metrics

## Credits

Developed with ❤️ using Streamlit and powered by FBref/StatsBomb data.
