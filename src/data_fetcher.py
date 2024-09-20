import pandas as pd

import nfl_data_py as nfl


def import_and_clean_data(import_func, data_type, *args, **kwargs):
    try:
        data = import_func(*args, **kwargs)
        data_cleaned = nfl.clean_nfl_data(data)
        differences = data.compare(data_cleaned)

        if not differences.empty:
            print(f"{data_type} cleaned these differences: {differences}")
        print(f"{data_type} imported: {data_cleaned.shape[0]}")
        # Column descriptions
        print(f"Columns in {data_type}:")
        for col in data.columns:
            print(
                f"Column: {col}, Type: {data[col].dtype}, Example Values: {data[col].unique()[:5]}"
            )
        return data_cleaned
    except Exception as e:
        print(f"Error importing {data_type}: {e}")
        return None


YEAR = 2024
# print(f"Available Play-by-play coplumns: {[col for col in nfl.see_pbp_cols()]}")
print(f"Available Weekly coplumns: {[col for col in nfl.see_weekly_cols()]}")
# Weekly data columns for comprehensive reporting
weekly_columns = [
    "player_id",
    "player_name",
    "player_display_name",
    "position",
    "position_group",
    "recent_team",
    "season",
    "week",
    "opponent_team",
    "completions",
    "attempts",
    "passing_yards",
    "passing_tds",
    "interceptions",
    "sacks",
    "carries",
    "rushing_yards",
    "rushing_tds",
    "receptions",
    "targets",
    "receiving_yards",
    "receiving_tds",
    "fantasy_points_ppr",
    "target_share",
    "air_yards_share",
    "wopr",
]
weekly_data = import_and_clean_data(
    nfl.import_weekly_data, "WeeklyData", [YEAR], columns=weekly_columns
)

# Import and clean data
players = import_and_clean_data(nfl.import_players, "Players")
# team_desc = import_and_clean_data(nfl.import_team_desc, "Team Descriptions")
# seasons = import_and_clean_data(nfl.import_seasonal_data, "Season Data", [YEAR], "ALL")
# roster = import_and_clean_data(nfl.import_seasonal_rosters, "Season Roster", [YEAR])
roster = import_and_clean_data(nfl.import_weekly_rosters, "Weekly Roster", [YEAR])
# snaps = import_and_clean_data(nfl.import_snap_counts, "Snaps", [YEAR])
# ids = import_and_clean_data(nfl.import_ids, "Player IDs")

exit()
# Convert birth_date in both dataframes to datetime format
roster["birth_date"] = pd.to_datetime(roster["birth_date"], errors="coerce")
players["birth_date"] = pd.to_datetime(players["birth_date"], errors="coerce")

# Drop unnecessary columns from one of the dataframes to avoid conflicts during merge
players_cleaned = players.drop(
    columns=["position", "jersey_number", "height", "weight", "status"], errors="ignore"
)

# Merge roster and players data using 'player_id'
roster_data = pd.merge(
    roster, players_cleaned, on=["first_name", "last_name", "birth_date"]
)

# Merge the above with seasonal data to get the player's stats for that year
team_player_data = pd.merge(roster_data, seasons, on="player_id")

# Select relevant columns from season data (more than just fantasy points)
key_columns = [
    "team",
    "player_name",
    "position",
    "jersey_number",
    "height",
    "weight",
    "college",
    "years_exp",
    "status",
    "completions",
    "attempts",
    "passing_yards",
    "passing_tds",
    "interceptions",
    "sacks",
    "sack_yards",
    "sack_fumbles",
    "sack_fumbles_lost",
    "passing_air_yards",
    "passing_yards_after_catch",
    "passing_first_downs",
    "passing_epa",
    "passing_2pt_conversions",
    "carries",
    "rushing_yards",
    "rushing_tds",
    "rushing_fumbles",
    "rushing_fumbles_lost",
    "rushing_first_downs",
    "rushing_epa",
    "rushing_2pt_conversions",
    "targets",
    "receptions",
    "receiving_yards",
    "receiving_tds",
    "receiving_fumbles",
    "receiving_fumbles_lost",
    "receiving_air_yards",
    "receiving_yards_after_catch",
    "receiving_first_downs",
    "receiving_epa",
    "receiving_2pt_conversions",
    "special_teams_tds",
    "fantasy_points",
    "fantasy_points_ppr",
    "games",
    "tgt_sh",
    "ay_sh",
    "yac_sh",
    "wopr_x",
    "wopr_y",
    "completion_percentage",
    "drops",
    "target_share",
    "air_yards_share",
    "red_zone_targets",
    "snap_percentage",
    "drive_participation",
]

# Filter the data to only include the columns we are interested in
filtered_data = team_player_data[key_columns]

# Export the final team_player_data to an Excel file
file_path = "team_player_data_fantasy_detailed.xlsx"
filtered_data.to_excel(file_path, index=False)
print(f"Data exported to {file_path}")


def team_roster(data, team_name):
    # Group by the team
    grouped_data = filtered_data.groupby("team")

    # Build and print the report
    for team, data in grouped_data:
        if team != team_name:
            continue
        print(f"Team: {team}")
        print("=" * 40)
        for _, row in data.iterrows():
            print(
                f"Player: {row['player_name']} (Jersey Number: {int(row['jersey_number'])})"
            )
            print(f"  Position: {row['position']}")
            print(f"  Height: {row['height']} inches, Weight: {row['weight']} lbs")
            print(f"  College: {row['college']}, Experience: {row['years_exp']} years")
            print(f"  Status: {row['status']}")
            print(
                f"  Passing: {row['completions']} completions, {int(row['passing_yards'])} yards, {row['passing_tds']} TDs, {row['interceptions']} INTs"
            )
            print(
                f"  Attempts: {row['attempts']}, Completion %: {row['completion_percentage']}%"
            )
            print(f"  Rushing: {row['rushing_yards']} yards, {row['rushing_tds']} TDs")
            print(
                f"  Receiving: {row['targets']} targets, {row['receptions']} receptions, {row['receiving_yards']} yards, {row['receiving_tds']} TDs"
            )
            print(
                f"  Drops: {row['drops']}, Target Share: {row['target_share']}, Air Yards Share: {row['air_yards_share']}"
            )
            print(
                f"  Fantasy Points: {row['fantasy_points']}, PPR Points: {row['fantasy_points_ppr']}"
            )
            print(
                f"  Snap Percentage: {row['snap_percentage']}, Drive Participation: {row['drive_participation']}"
            )
            print("-" * 40)
        print("\n")


# Generate roster for a specific team
team_roster(filtered_data, "DAL")
