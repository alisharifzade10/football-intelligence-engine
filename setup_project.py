from pathlib import Path

# Define the directories for the project
directories = [
    "config",
    "data/raw/premier_league",
    "data/processed",
    "sql",
    "src/ingestion",
    "src/processing",
    "src/db",
    "tableau",
    "notebooks",
    "tests",
    "scripts",
]

# Define the files for the project
files = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    ".env.example",
    "config/settings.yaml",
    "src/__init__.py",
    "src/ingestion/__init__.py",
    "src/processing/__init__.py",
    "src/db/__init__.py",
    "src/ingestion/download_data.py",
    "src/processing/clean_data.py",
    "src/processing/validate_data.py",
    "src/db/connection.py",
    "src/db/load_to_mysql.py",
    "sql/01_schema.sql",
    "sql/02_validation.sql",
    "sql/03_views.sql",
    "sql/04_analysis.sql",
    "sql/05_features.sql",
]

# Starter content, written only if the file is missing or empty
default_content = {
    "README.md": "# Football Intelligence Engine\n\n"
    "Premier League data pipeline: Python -> MySQL -> Tableau, "
    "with match prediction as the later goal.\n",
    "requirements.txt": "pandas\nsqlalchemy\npymysql\ncryptography\n"
    "python-dotenv\npyyaml\npytest\n",
    ".gitignore": "# Python\n.venv/\n__pycache__/\n*.pyc\n.ipynb_checkpoints/\n"
    ".pytest_cache/\n\n# Secrets\n.env\n\n# Generated data\ndata/processed/\n\n"
    "# Tableau extracts\n*.hyper\n*.tde\n\n# OS\n.DS_Store\nThumbs.db\n",
    ".env.example": "DB_HOST=localhost\nDB_PORT=3306\nDB_NAME=football\n"
    "DB_USER=your_user\nDB_PASSWORD=your_password\n",
    "config/settings.yaml": "paths:\n  raw_data: data/raw/premier_league\n"
    "  processed_data: data/processed\n\ndatabase:\n  name: football\n\n"
    "analysis:\n  full_stats_from_season: \"2000/01\"\n"
    "  odds_benchmark_from_season: \"2002/03\"\n",
}

# Set the project root to the current directory
project_path = Path(".")

print(f"Creating project structure in: {project_path.resolve()}")

# Create directories
for directory in directories:
    (project_path / directory).mkdir(parents=True, exist_ok=True)

# Create files only if they do not already exist
for file in files:
    path = project_path / file
    path.touch(exist_ok=True)
    # Fill starter content only into empty files, never overwrite existing work
    if file in default_content and path.stat().st_size == 0:
        path.write_text(default_content[file], encoding="utf-8")
        print(f"  wrote starter content: {file}")

print("\nProject structure created successfully!")
print("\nManual steps (not automated, to avoid losing work):")
print("  1. Move src/scraper/fetcher.py -> src/ingestion/download_data.py")
print("  2. Delete src/scraper/ once parser.py and scraper.py are not needed")
print("  3. Delete the empty database/ folder")
print("  4. Copy .env.example to .env and fill in your MySQL credentials")