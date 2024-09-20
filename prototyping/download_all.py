import sys
from datetime import datetime

import pandas as pd

import nfl_data_py as nfl

DUMP_COLUMNS = True


def fetch_and_save_data(fetch_function, writer, *args, **kwargs):
    """Fetch data, clean it, and save to an Excel file with timestamp.
    Also checks for changes in data after cleaning and reports differences."""
    try:
        # Fetch the data
        data = fetch_function(*args, **kwargs)

        # Count the number of rows in the fetched data
        num_rows_fetched = len(data)

        # Clean the data
        cleaned_data = nfl.clean_nfl_data(data)

        # Check for differences between original and cleaned data
        differences = data.compare(cleaned_data)

        # Save to Excel in a new sheet named after the fetch function
        sheet_name = fetch_function.__name__.replace("import_", "")
        cleaned_data.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"[{fetch_function.__name__}] Number of rows fetched: {num_rows_fetched}")

        if DUMP_COLUMNS:
            print(f"\nTABLE DUMP - Columns in {fetch_function}:", file=sys.stderr)
            for col in cleaned_data.columns:
                print(
                    f"Column: {col}, Type: {cleaned_data[col].dtype}, "
                    f"Example Values: {list(cleaned_data[col].unique()[:5])}",
                    file=sys.stderr,
                )

        if not differences.empty:
            print("Differences found after cleaning:")
            print(differences)

        return cleaned_data
    except Exception as e:
        print(f"Error fetching or saving {fetch_function.__name__}: {e}")


# Generate timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Create filename with timestamp
filename = f"nfl_data_download_{timestamp}.xlsx"

# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
    # Define the years for which you want to fetch data
    years = [2024]

    # Fetch and save play-by-play data
    if 2024 not in years:
        fetch_and_save_data(nfl.import_pbp_data, writer, years)

    # Fetch and save weekly data
    fetch_and_save_data(
        nfl.import_weekly_data,
        writer,
        years,
        columns=[col for col in nfl.see_weekly_cols()],
    )

    # Fetch and save seasonal data
    fetch_and_save_data(nfl.import_seasonal_data, writer, years, s_type="ALL")

    # Fetch and save seasonal rosters
    fetch_and_save_data(nfl.import_seasonal_rosters, writer, years)

    # Fetch and save weekly rosters
    fetch_and_save_data(nfl.import_weekly_rosters, writer, years)

    # Fetch and save win totals
    fetch_and_save_data(nfl.import_win_totals, writer, years)

    # Fetch and save scoring lines
    fetch_and_save_data(nfl.import_sc_lines, writer, years)

    # Fetch and save officials data
    fetch_and_save_data(nfl.import_officials, writer, years)

    # Fetch and save draft picks
    fetch_and_save_data(nfl.import_draft_picks, writer, years)

    # Fetch and save draft values
    fetch_and_save_data(nfl.import_draft_values, writer)

    # Fetch and save team descriptions
    fetch_and_save_data(nfl.import_team_desc, writer)

    # Fetch and save schedules
    fetch_and_save_data(nfl.import_schedules, writer, years)

    # Fetch and save combine data
    fetch_and_save_data(nfl.import_combine_data, writer, years)

    # Fetch and save ID mappings
    fetch_and_save_data(nfl.import_ids, writer)

    # Fetch and save NGS data
    fetch_and_save_data(nfl.import_ngs_data, writer, "passing", years)

    # Fetch and save depth charts
    fetch_and_save_data(nfl.import_depth_charts, writer, years)

    # Fetch and save injuries data
    fetch_and_save_data(nfl.import_injuries, writer, years)

    # Fetch and save QBR data
    fetch_and_save_data(nfl.import_qbr, writer, years, level="nfl", frequency="season")

    # Fetch and save seasonal PFR data
    fetch_and_save_data(nfl.import_seasonal_pfr, writer, "pass", years)

    # Fetch and save weekly PFR data
    fetch_and_save_data(nfl.import_weekly_pfr, writer, "pass", years)

    # Fetch and save snap counts
    fetch_and_save_data(nfl.import_snap_counts, writer, years)

    # Fetch and save FTN data
    fetch_and_save_data(nfl.import_ftn_data, writer, years)

print(f"All data saved to {filename}")
