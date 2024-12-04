import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating synthetic data
faker = Faker()

# Load your dataset
file_path = 'nfl_rosters.csv'  # Replace with your dataset's path
rosters = pd.read_csv(file_path)

# Define the number of additional nodes required
current_nodes = len(rosters['player_id'].unique())
target_nodes = 100000
additional_nodes = target_nodes - current_nodes

# Step 1: Reuse existing players and extend their careers
existing_players = rosters[['team', 'player_name', 'height', 'weight', 'college', 'player_id']].drop_duplicates()
years = range(1970, 2023)  # Random years for extending careers
reused_data = []

# Ensure teams are a Python list and valid
teams = rosters['team'].dropna().unique().tolist()

if not teams:  # Ensure there are valid teams
    raise ValueError("No valid teams found in the dataset. Check the 'team' column.")

for _ in range(int(0.5 * additional_nodes)):  # 50% of additional nodes will reuse existing players
    player = existing_players.sample(1).iloc[0]
    team = player['team']
    player_name = player['player_name']
    player_id = player['player_id']
    height = player['height']
    weight = player['weight']
    college = player['college']
    season = random.choice(years)  # Assign to a random year
    jersey_number = random.randint(1, 99)

    reused_data.append([team, season, player_name, jersey_number, height, weight, college, player_id])

# Step 2: Generate entirely new players
new_data = []

for _ in range(int(0.5 * additional_nodes)):  # 50% of additional nodes will be new players
    season = random.choice(years)
    team = random.choice(teams)  # Randomly select a valid team
    player_name = faker.name()
    jersey_number = random.randint(1, 99)
    height = round(random.uniform(68, 78), 1)  # Random height in inches
    weight = random.randint(160, 300)  # Random weight in lbs
    college = faker.company() if random.random() > 0.3 else ''  # Some players with no college
    player_id = f"{random.randint(10, 99):02}-{random.randint(0, 9999999):07}"  # Unique player ID

    new_data.append([team, season, player_name, jersey_number, height, weight, college, player_id])

# Combine reused and new data
synthetic_data = pd.DataFrame(reused_data + new_data, columns=rosters.columns)

# Combine the synthetic data with the original dataset
expanded_rosters = pd.concat([rosters, synthetic_data], ignore_index=True)

# Save the expanded dataset
output_file_path = 'expanded_nfl_rosters.csv'
expanded_rosters.to_csv(output_file_path, index=False)

print(f"Dataset expanded to {len(expanded_rosters['player_id'].unique())} unique nodes and saved to {output_file_path}.")
