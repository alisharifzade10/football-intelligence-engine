""" Read the 34 raw season CSVs, clean them and write ONE file: data/processed/matches.csv """
import csv
from pathlib import Path
import pandas as pd 


PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Set the project root to the parent directory of the current file's parent directory
RAW_DIR = PROJECT_ROOT /"data" / "raw" / "premier_league"
OUT_FILE = PROJECT_ROOT / "data" / "processed" / "matches.csv"


CURENT_SEASON = "2026/27"  # Still beeing played, no traning data yet, so not used for ML
COVIDE_SEASONS = "2020/21" # Empty stadiums, home advantage was different

# csv_files = list(RAW_DIR.glob("*.csv"))
# df=pd.read_csv(csv_files[0], encoding="latin1")
# print("Number of CSV files:", len(csv_files))
# print("First few files:", csv_files[:5])
# print(df.dtypes)

# RAW column name -> clean column name (also fixes the rversed word AS)
RENAME = {
    "Div:": "division", "Date": "match_date", "Time": "kickoff_time", "HomeTeam": "home_team", 
    "AwayTeam": "away_team", "FTHG": "home_goals", "FTAG": "away_goals", "FTR": "result",
    "HTHG": "ht_home_goals", "HTAG": "ht_away_goals", "HTR": "ht_result", "Referee": "referee", 
    "HS": "home_shots", "AS": "away_shots",
    "HST": "home_shots_on_target", "AST": "away_shots_on_target",
    "HF": "home_fouls", "AF": "away_fouls",
    "HC": "home_corners", "AC": "away_corners",
    "HY": "home_yellows", "AY": "away_yellows",
    "HR": "home_reds", "AR": "away_reds",
    "B365H": "b365_home", "B365D": "b365_draw", "B365A": "b365_away",
    # Old seasons (2005/06-2018/19) call the market max/average odds "Bb..."
    "BbMxH": "max_home", "BbMxD": "max_draw", "BbMxA": "max_away",
    "BbAvH": "avg_home", "BbAvD": "avg_draw", "BbAvA": "avg_away",
    # New seasons (2019/20+) call the same thing "Max..." / "Avg..."
    "MaxH": "max_home", "MaxD": "max_draw", "MaxA": "max_away",
    "AvgH": "avg_home", "AvgD": "avg_draw", "AvgA": "avg_away"
}

TEXT_COLS= ["division", "kickoff_time", "home_team", "away_team", "result", "ht_result", "referee"]

FINAL_COLS = [
    "match_id", "season", "season_start_year", "match_date", "kickoff_time",
    "home_team", "away_team", "home_goals", "away_goals", "result",
    "ht_home_goals", "ht_away_goals", "ht_result", "referee",
    "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
    "home_fouls", "away_fouls", "home_corners", "away_corners",
    "home_yellows", "away_yellows", "home_reds", "away_reds",
    "b365_home", "b365_draw", "b365_away",
    "max_home", "max_draw", "max_away", "avg_home", "avg_draw", "avg_away",
    "is_covid_season", "is_complete",
]

