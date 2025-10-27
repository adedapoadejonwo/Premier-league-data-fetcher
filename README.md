# FPL Data Collector Pipeline ⚽🔥

A comprehensive Python ETL pipeline that automatically fetches, transforms, and loads football + FPL data into your PostgreSQL database (Neon or Supabase).

## 🧩 Overview

This pipeline fetches data from multiple free APIs:
- **FPL API**: Player stats, team information, fixtures
- **Understat**: Expected Goals (xG) and Expected Assists (xA) data
- **The Odds API**: Betting odds for Premier League matches
- **WeatherAPI.com**: Weather conditions for match locations

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
WEATHERAPI_KEY=your_weatherapi_key_here
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
2. **WeatherAPI.com**: Get your free API key at [weatherapi.com](https://www.weatherapi.com/)

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

#### GitHub Actions Setup:
1. Go to your repository → Settings → Secrets and variables → Actions
2. Add these repository secrets:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ODDS_API_KEY`: Your Odds API key
   - `WEATHERAPI_KEY`: Your WeatherAPI.com key
3. The workflow will automatically run daily or can be triggered manually

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
- **WeatherAPI.com**: `http://api.weatherapi.com/v1/current.json`

## 🚨 Error Handling

The pipeline includes comprehensive error handling:
- **API Rate Limiting**: 30-second timeouts on all API calls
- **Database Connection Failures**: Proper validation and error logging
- **Data Validation**: Graceful handling of missing or malformed data
- **Environment Variables**: Validation for missing API keys
- **Logging**: Detailed error messages for debugging
- **Retry Logic**: Individual operation failures don't crash the entire pipeline

## 📝 License

MIT License - feel free to use and modify as needed!
