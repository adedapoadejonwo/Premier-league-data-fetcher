# FPL Data Collector Pipeline ⚽🔥

A comprehensive Python ETL pipeline that automatically fetches, transforms, and loads football + FPL data into your PostgreSQL database (Neon or Supabase).

## 🧩 Overview

This pipeline fetches data from multiple free APIs:
- **FPL API**: Player stats, team information, fixtures
- **Understat**: Expected Goals (xG) and Expected Assists (xA) data
- **The Odds API**: Betting odds for Premier League matches
- **WeatherAPI**: Weather conditions for match locations

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd fpl_data_collector

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file with your credentials:

```env
DATABASE_URL=postgresql://user:password@neon-host/dbname?sslmode=require
ODDS_API_KEY=your_oddsapi_key_here
OPENWEATHER_API_KEY=your_weather_api_key_here
```

### 3. Run the Pipeline

```bash
python main.py
```

## 📁 Project Structure

```
fpl_data_collector/
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore file
├── main.py                # Main pipeline runner
├── db.py                  # Database connection helper
├── fpl_api.py            # FPL API fetcher
├── understat_api.py      # Understat xG/xA fetcher
├── odds_api.py           # Betting odds fetcher
├── weather_api.py        # Weather data fetcher
├── requirements.txt      # Python dependencies
└── .github/workflows/    # GitHub Actions automation
    └── data-update.yml
```

## 🔧 API Keys Required

1. **The Odds API**: Get your free API key at [the-odds-api.com](https://the-odds-api.com/)
2. **OpenWeather**: Get your free API key at [openweathermap.org](https://openweathermap.org/api)

## 🗄️ Database Schema

The pipeline expects the following PostgreSQL schema:

### Core Tables
- `player.person` - Player information
- `core.team` - Team information
- `features.team_strength` - Team strength metrics
- `markets.odds_snapshot` - Betting odds data
- `match.weather` - Weather conditions

## 🤖 Automation Options

### Option A: Cron Job
Run daily at 8 AM:
```bash
0 8 * * * /usr/bin/python3 /path/to/fpl_data_collector/main.py
```

### Option B: GitHub Actions (Recommended)
The pipeline includes a GitHub Actions workflow that:
- Runs daily at 8 AM UTC
- Can be triggered manually
- Automatically commits results
- Uses GitHub Secrets for API keys

## 🔄 Pipeline Flow

1. **Fetch FPL Data**: Player stats and team information
2. **Load Understat Data**: xG/xA metrics for team strength
3. **Collect Odds**: Betting odds for upcoming matches
4. **Get Weather**: Weather conditions for match locations
5. **Store in Database**: All data transformed and loaded

## 🧠 Next Steps

Once the ETL runs successfully, you can:

- Add AI model training after data load
- Extend to player predictions
- Add Discord notifications for new predictions
- Create data visualization dashboards

## 🛠️ Development

To extend the pipeline:

1. Add new data sources in separate modules
2. Update the main pipeline runner
3. Extend database schema as needed
4. Add new transformation logic

## 📊 Data Sources

- **FPL API**: `https://fantasy.premierleague.com/api/bootstrap-static/`
- **Understat**: `https://understat.com/team/{team}/2024`
- **The Odds API**: `https://api.the-odds-api.com/v4/sports/soccer_epl/odds/`
- **OpenWeather**: `https://api.openweathermap.org/data/2.5/weather`

## 🚨 Error Handling

The pipeline includes basic error handling:
- API rate limiting
- Database connection failures
- Data validation
- Logging for debugging

## 📝 License

MIT License - feel free to use and modify as needed!
