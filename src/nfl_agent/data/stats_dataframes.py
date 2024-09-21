import os
import warnings

from joblib import Memory
from tqdm import tqdm

import nfl_data_py as nfl

# Suppress specific warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="The win totals data source is currently in flux and may be out of date.",
)
warnings.filterwarnings("ignore", category=UserWarning, message="Downcasting floats.")

# Define the years for which you want to fetch data
years = [2024]  # Adjust as needed

# Determine the project root directory
data_root = os.path.dirname(os.path.abspath(__file__))

# Set up caching directory relative to the project root
cache_dir = os.path.join(data_root, ".nfl_cache")
os.makedirs(cache_dir, exist_ok=True)
memory = Memory(cache_dir, verbose=0)

# List of functions to call and their arguments
tasks = [
    (nfl.import_weekly_data, {"years": years}),
    (nfl.import_seasonal_data, {"years": years, "s_type": "ALL"}),
    (nfl.import_seasonal_rosters, {"years": years}),
    (nfl.import_weekly_rosters, {"years": years}),
    (nfl.import_win_totals, {"years": years}),
    (nfl.import_sc_lines, {"years": years}),
    (nfl.import_officials, {"years": years}),
    (nfl.import_draft_picks, {"years": years}),
    (nfl.import_draft_values, {}),
    (nfl.import_team_desc, {}),
    (nfl.import_schedules, {"years": years}),
    (nfl.import_combine_data, {"years": years}),
    (nfl.import_ids, {}),
    (nfl.import_ngs_data, {"stat_type": "passing", "years": years}),
    (nfl.import_ngs_data, {"stat_type": "receiving", "years": years}),
    (nfl.import_ngs_data, {"stat_type": "rushing", "years": years}),
    (nfl.import_depth_charts, {"years": years}),
    (nfl.import_injuries, {"years": years}),
    (nfl.import_qbr, {"years": years, "level": "nfl", "frequency": "season"}),
    (nfl.import_seasonal_pfr, {"s_type": "pass", "years": years}),
    (nfl.import_seasonal_pfr, {"s_type": "rush", "years": years}),
    (nfl.import_seasonal_pfr, {"s_type": "rec", "years": years}),
    (nfl.import_weekly_pfr, {"s_type": "pass", "years": years}),
    (nfl.import_weekly_pfr, {"s_type": "rush", "years": years}),
    (nfl.import_weekly_pfr, {"s_type": "rec", "years": years}),
    (nfl.import_snap_counts, {"years": years}),
    (nfl.import_ftn_data, {"years": years}),
]

# Initialize an empty dictionary to store the results
results = {}

# Iterate over tasks with a progress bar
for func, kwargs in tqdm(tasks, desc="Fetching NFL data"):
    cached_func = memory.cache(func)
    result_key = func.__name__
    results[result_key] = cached_func(**kwargs)

# Access the results using the keys
weekly_data = results["import_weekly_data"]
seasonal_data = results["import_seasonal_data"]
seasonal_rosters = results["import_seasonal_rosters"]
weekly_rosters = results["import_weekly_rosters"]
win_totals = results["import_win_totals"]
sc_lines = results["import_sc_lines"]
officials = results["import_officials"]
draft_picks = results["import_draft_picks"]
draft_values = results["import_draft_values"]
team_desc = results["import_team_desc"]
schedules = results["import_schedules"]
combine_data = results["import_combine_data"]
ids = results["import_ids"]
ngs_passing = results["import_ngs_data"]
ngs_receiving = results["import_ngs_data"]
ngs_rushing = results["import_ngs_data"]
depth_charts = results["import_depth_charts"]
injuries = results["import_injuries"]
qbr_data = results["import_qbr"]
pfr_seasonal_passing = results["import_seasonal_pfr"]
pfr_seasonal_rushing = results["import_seasonal_pfr"]
pfr_seasonal_receiving = results["import_seasonal_pfr"]
pfr_weekly_passing = results["import_weekly_pfr"]
pfr_weekly_rushing = results["import_weekly_pfr"]
pfr_weekly_receiving = results["import_weekly_pfr"]
snap_counts = results["import_snap_counts"]
ftn_data = results["import_ftn_data"]

# Include any other data frames as needed
