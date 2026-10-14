
from pathlib import Path
import time
import requests

# Project root: football-intelligence-engine/
PROJECT_ROOT=Path(__file__).resolve().parents[2] # Set the project root to the parent directory of the current file's parent directory

#Folder for original source files
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "premier_league"

# URL to fetch the Premier League data from data.co.uk
PREMIER_LEAGUE_DATA_URL = "https://www.football-data.co.uk/mmz4281"

# Download season from 1993/1994 to 2026/2027
FIRST_SEASON = 1993
LAST_SEASON = 2026

# Refresh the current season every time the scrapper runs, as the data is updated frequently
# Histrical data is not updated, so we can skip downloading it again if it already exists
Current_season_code = "2627"

Headers = {
    "User-Agent": "football-intelligence-engine/0.1" #Set a custom User-Agent header to identify the scraper when making requests
}


def generate_seasons() -> list[tuple[str,str]]: #Set the return type of the function to a list of tuples containing two strings (season name and code
    """
    Generate season names and their Football Data URLs for the Premier League from the first season to the last season.
    """
    seasons=[]
    for start_year in range (FIRST_SEASON, LAST_SEASON + 1):
        end_year=start_year + 1
        season_name=f"{start_year}/{str(end_year)[-2:]}" #Format the season name as "YYYY/YY"
        season_code=(
            f"{start_year % 100:02d}" # format the start year as a two-digit number
            f"{end_year % 100:02d}"
        )

        seasons.append((season_name, season_code))
    return seasons


def fetch_season(session: requests.Session, season_name:str, season_code:str)-> str:
    """
    Fetch the Premier League data for a specific season from the data.co.uk website and save it to a CSV file.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)  # Create the raw data directory if it doesn't exist

    output_path=RAW_DATA_DIR / (f"premier_league_{season_code}.csv") #Set the output path for the CSV file based on the season code

    url=f"{PREMIER_LEAGUE_DATA_URL}/{season_code}/E0.csv" # Construct the URL for the specific season's data


    # Skip downloading the file if it already exists and refresh the current season
    if output_path.exists() and season_code != Current_season_code:
        print(f"Skipping download for {season_name} as the file already exists.")
        return "skipped"

    try:
        response=session.get(url,timeout=30)

        if response.status_code==404:
            print(f"Data for {season_name} not found (404). Skipping.")
            return "unavailable"

        response.raise_for_status()  # Raise an exception for HTTP errors

        content=response.content

        # check if the response resembles a CSV file, not an HTML
        text = response.content.decode("utf-8-sig", errors="replace")
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if not content or "<html" in text[:1000].lower() or "HomeTeam" not in first_line:
            print(f"Data for {season_name} is not a valid CSV file. Skipping.")
            return "invalid_csv"

        # Save the content to a CSV file
        output_path.write_bytes(content)
        print(f"Downloaded data for {season_name}:", f"{len(content):,} bytes")
        return "downloaded"

    except requests.RequestException as error:
        print(f"Failed to fetch data for {season_name}: {error}")
        return "failed"


#Set the main function to run the scraper when executed as a script
def main() -> None:
    seasons = generate_seasons() # Generate the list of seasons to fetch

    results = {
        "downloaded": 0,
        "skipped": 0,
        "unavailable": 0,
        "invalid_csv": 0,
        "failed": 0,
    }

    print(f"Project directory: {PROJECT_ROOT}")
    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Seasons to fetch: {len(seasons)}")
    print("-"*60)

    with requests.Session() as session:
        session.headers.update(Headers)  # Update the session headers with the custom User-Agent

        for season_name, season_code in seasons:
            result = fetch_season(session, season_name, season_code)
            results[result]+=1

            time.sleep(1)  # Add a delay between requests to avoid overwhelming the server

    print("\n" + "=" *60)
    print("Download Summary:")

    for status, count in results.items():
        print(f"{status.capitalize()}: {count}")

    print("\nFiles are saved in:", RAW_DATA_DIR)


if __name__ == "__main__":
    main()
