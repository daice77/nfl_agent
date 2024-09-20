# data/stats_dataframes.py

import nfl_data_py as nfl
import pandas as pd

# Define the years for which you want to fetch data
years = [2024]  # Adjust as needed

# Load data frames using nfl_data_py

# Fetch play-by-play data (if needed)
# pbp_data = nfl.import_pbp_data(years=years)

# Fetch weekly data
weekly_data = nfl.import_weekly_data(years=years)

# Fetch seasonal data
seasonal_data = nfl.import_seasonal_data(years=years, s_type='ALL')

# Fetch seasonal rosters
seasonal_rosters = nfl.import_seasonal_rosters(years=years)

# Fetch weekly rosters
weekly_rosters = nfl.import_weekly_rosters(years=years)

# Fetch win totals
win_totals = nfl.import_win_totals(years=years)

# Fetch scoring lines
sc_lines = nfl.import_sc_lines(years=years)

# Fetch officials data
officials = nfl.import_officials(years=years)

# Fetch draft picks
draft_picks = nfl.import_draft_picks(years=years)

# Fetch draft values
draft_values = nfl.import_draft_values()

# Fetch team descriptions
team_desc = nfl.import_team_desc()

# Fetch schedules
schedules = nfl.import_schedules(years=years)

# Fetch combine data
combine_data = nfl.import_combine_data(years=years)

# Fetch IDs mapping
ids = nfl.import_ids()

# Fetch NGS data
ngs_passing = nfl.import_ngs_data(stat_type='passing', years=years)
ngs_receiving = nfl.import_ngs_data(stat_type='receiving', years=years)
ngs_rushing = nfl.import_ngs_data(stat_type='rushing', years=years)

# Fetch depth charts
depth_charts = nfl.import_depth_charts(years=years)

# Fetch injuries data
injuries = nfl.import_injuries(years=years)

# Fetch QBR data
qbr_data = nfl.import_qbr(years=years, level='nfl', frequency='season')

# Fetch PFR seasonal data
pfr_seasonal_passing = nfl.import_seasonal_pfr(stat_type='pass', years=years)
pfr_seasonal_rushing = nfl.import_seasonal_pfr(stat_type='rush', years=years)
pfr_seasonal_receiving = nfl.import_seasonal_pfr(stat_type='rec', years=years)

# Fetch PFR weekly data
pfr_weekly_passing = nfl.import_weekly_pfr(stat_type='pass', years=years)
pfr_weekly_rushing = nfl.import_weekly_pfr(stat_type='rush', years=years)
pfr_weekly_receiving = nfl.import_weekly_pfr(stat_type='rec', years=years)

# Fetch snap counts
snap_counts = nfl.import_snap_counts(years=years)

# Fetch FTN data
ftn_data = nfl.import_ftn_data(years=years)

# Include any other data frames as needed
