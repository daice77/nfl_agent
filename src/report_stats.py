import pandas as pd

import nfl_data_py as nfl

DEBUG = False


# Function to import and clean data
def import_and_clean_data(import_func, data_type, *args, **kwargs):
    try:
        data = import_func(*args, **kwargs)
        data_cleaned = nfl.clean_nfl_data(data)
        differences = data.compare(data_cleaned)

        if not differences.empty:
            print(f"{data_type} cleaned these differences: {differences}")
        print(f"{data_type} imported: {data_cleaned.shape[0]}")
        if DEBUG:
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

# Import data
players = import_and_clean_data(nfl.import_players, "Players")
player_ids = import_and_clean_data(nfl.import_ids, "Player IDs")
weekly_roster = import_and_clean_data(
    nfl.import_weekly_rosters, "Weekly Roster", [YEAR]
)

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

# Snap count data
snap_columns = [
    "pfr_player_id",
    "team",
    "week",
    "offense_snaps",
    "offense_pct",
    "defense_snaps",
    "defense_pct",
    "st_snaps",
    "st_pct",
]
snap_counts = import_and_clean_data(nfl.import_snap_counts, "Snaps", [YEAR])[
    snap_columns
]

# Step 1: Merge Weekly Data with Player IDs using 'player_id' and 'gsis_id'
# (as they are equivalent)
weekly_data_with_ids = pd.merge(
    weekly_data,
    player_ids[["gsis_id", "pfr_id"]],  # We keep only relevant columns
    left_on="player_id",
    right_on="gsis_id",
    how="left",
)

# Step 2: Merge the result with Snap Counts using 'pfr_id' and 'pfr_player_id'
team_player_data = pd.merge(
    weekly_data_with_ids,
    snap_counts,
    left_on=["pfr_id", "week"],
    right_on=["pfr_player_id", "week"],
    how="left",
)

# Step 3: Merge with Weekly Roster if you need additional player information
# like height, weight, etc.
team_player_data = pd.merge(
    team_player_data,
    weekly_roster[
        ["player_id", "first_name", "last_name", "team", "position", "pfr_id", "week"]
    ],
    on=["player_id", "week"],
    how="left",
)

# Step 4: Aggregating weekly and snap data by player for the season
aggregated_data = (
    team_player_data.groupby(["player_id", "player_name", "position_x", "recent_team"])
    .agg(
        {
            "completions": "sum",
            "attempts": "sum",
            "passing_yards": "sum",
            "passing_tds": "sum",
            "interceptions": "sum",
            "carries": "sum",
            "rushing_yards": "sum",
            "rushing_tds": "sum",
            "receptions": "sum",
            "targets": "sum",
            "receiving_yards": "sum",
            "receiving_tds": "sum",
            "fantasy_points_ppr": "sum",
            "target_share": "mean",
            "air_yards_share": "mean",
            "wopr": "mean",
            "offense_snaps": "sum",
            "offense_pct": "mean",
            "defense_snaps": "sum",
            "defense_pct": "mean",
            "st_snaps": "sum",
            "st_pct": "mean",
            "week": "count",  # Weeks played
        }
    )
    .reset_index()
)

# Rename 'week' aggregation to 'weeks_played'
aggregated_data.rename(columns={"week": "weeks_played"}, inplace=True)

# Select key columns for final report
key_columns = [
    "player_name",
    "position_x",
    "recent_team",
    "weeks_played",
    "completions",
    "attempts",
    "passing_yards",
    "passing_tds",
    "interceptions",
    "carries",
    "rushing_yards",
    "rushing_tds",
    "receptions",
    "targets",
    "receiving_yards",
    "receiving_tds",
    "fantasy_points_ppr",
    "offense_snaps",
    "offense_pct",
    "defense_snaps",
    "defense_pct",
    "st_snaps",
    "st_pct",
]

# Filter data to include only the relevant columns
filtered_data = aggregated_data[key_columns]

# Export final aggregated season data to an Excel file
file_path = "season_player_data_with_snaps.xlsx"
filtered_data.to_excel(file_path, index=False)
print(f"Data exported to {file_path}")


# Function to generate a team roster report
def team_roster(data, team_name):
    team_data = data[data["recent_team"] == team_name]
    print(f"Team: {team_name}")
    print("=" * 40)
    for _, row in team_data.iterrows():
        print(f"Player: {row['player_name']}")
        print(f"  Position: {row['position_x']} | Weeks Played: {row['weeks_played']}")
        print(
            f"  Passing: {row['completions']} completions, {row['passing_yards']} yards, {row['passing_tds']} TDs"
        )
        print(
            f"  Rushing: {row['carries']} carries, {row['rushing_yards']} yards, {row['rushing_tds']} TDs"
        )
        print(
            f"  Receiving: {row['receptions']} receptions, {row['receiving_yards']} yards, {row['receiving_tds']} TDs"
        )
        print(f"  Fantasy Points: {row['fantasy_points_ppr']} PPR")
        print(
            f"  Offensive Snaps: {row['offense_snaps']} | Offensive Snap Percentage: {row['offense_pct']}%"
        )
        print(
            f"  Defensive Snaps: {row['defense_snaps']} | Defensive Snap Percentage: {row['defense_pct']}%"
        )
        print(
            f"  Special Teams Snaps: {row['st_snaps']} | Special Teams Snap Percentage: {row['st_pct']}%"
        )
        print("-" * 40)
    print("\n")


# Example usage for a specific team
team_roster(filtered_data, "NE")
