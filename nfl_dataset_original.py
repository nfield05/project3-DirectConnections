import ssl
import nfl_data_py as nfl
import pandas as pd


ssl._create_default_https_context = ssl._create_unverified_context

# Specify the years you want to pull data for
years = range(1999, 2025)
columns = ['team','season','player_name','jersey_number','height','weight','college','player_id']

# Import the seasonal rosters
roster_data = nfl.import_seasonal_rosters(years=years, columns=columns)

# Save to a CSV file
roster_data.to_csv("nfl_rosters.csv", index=False)


