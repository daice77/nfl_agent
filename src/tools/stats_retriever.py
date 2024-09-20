import pandas as pd
from data.stats_dataframes import (
    weekly_data,
    seasonal_data,
    seasonal_rosters,
    weekly_rosters,
    win_totals,
    sc_lines,
    officials,
    draft_picks,
    draft_values,
    team_desc,
    schedules,
    combine_data,
    ids,
    ngs_passing,
    ngs_receiving,
    ngs_rushing,
    depth_charts,
    injuries,
    qbr_data,
    pfr_seasonal_passing,
    pfr_seasonal_rushing,
    pfr_seasonal_receiving,
    pfr_weekly_passing,
    pfr_weekly_rushing,
    pfr_weekly_receiving,
    snap_counts,
    ftn_data,
    # Include any other data frames you need
)

class StatsRetriever:
    def __init__(self):
        # Initialize all data frames
        self.weekly_data = weekly_data
        self.seasonal_data = seasonal_data
        self.seasonal_rosters = seasonal_rosters
        self.weekly_rosters = weekly_rosters
        self.win_totals = win_totals
        self.sc_lines = sc_lines
        self.officials = officials
        self.draft_picks = draft_picks
        self.draft_values = draft_values
        self.team_desc = team_desc
        self.schedules = schedules
        self.combine_data = combine_data
        self.ids = ids
        self.ngs_passing = ngs_passing
        self.ngs_receiving = ngs_receiving
        self.ngs_rushing = ngs_rushing
        self.depth_charts = depth_charts
        self.injuries = injuries
        self.qbr_data = qbr_data
        self.pfr_seasonal_passing = pfr_seasonal_passing
        self.pfr_seasonal_rushing = pfr_seasonal_rushing
        self.pfr_seasonal_receiving = pfr_seasonal_receiving
        self.pfr_weekly_passing = pfr_weekly_passing
        self.pfr_weekly_rushing = pfr_weekly_rushing
        self.pfr_weekly_receiving = pfr_weekly_receiving
        self.snap_counts = snap_counts
        self.ftn_data = ftn_data
        # Initialize any other data frames you need

    def get_player_stats(self, player_name: str):
        # Fetch stats for a specific player from multiple data frames
        stats = {}

        # Weekly data
        player_stats_weekly = self.weekly_data[self.weekly_data['player_name'] == player_name]
        stats['weekly_stats'] = player_stats_weekly.to_dict('records')

        # Seasonal data
        player_stats_seasonal = self.seasonal_data[self.seasonal_data['player_name'] == player_name]
        stats['seasonal_stats'] = player_stats_seasonal.to_dict('records')

        # PFR seasonal data
        player_pfr_seasonal_passing = self.pfr_seasonal_passing[self.pfr_seasonal_passing['player'] == player_name]
        player_pfr_seasonal_rushing = self.pfr_seasonal_rushing[self.pfr_seasonal_rushing['player'] == player_name]
        player_pfr_seasonal_receiving = self.pfr_seasonal_receiving[self.pfr_seasonal_receiving['player'] == player_name]
        stats['pfr_seasonal_passing'] = player_pfr_seasonal_passing.to_dict('records')
        stats['pfr_seasonal_rushing'] = player_pfr_seasonal_rushing.to_dict('records')
        stats['pfr_seasonal_receiving'] = player_pfr_seasonal_receiving.to_dict('records')

        # PFR weekly data
        player_pfr_weekly_passing = self.pfr_weekly_passing[self.pfr_weekly_passing['pfr_player_name'] == player_name]
        player_pfr_weekly_rushing = self.pfr_weekly_rushing[self.pfr_weekly_rushing['pfr_player_name'] == player_name]
        player_pfr_weekly_receiving = self.pfr_weekly_receiving[self.pfr_weekly_receiving['pfr_player_name'] == player_name]
        stats['pfr_weekly_passing'] = player_pfr_weekly_passing.to_dict('records')
        stats['pfr_weekly_rushing'] = player_pfr_weekly_rushing.to_dict('records')
        stats['pfr_weekly_receiving'] = player_pfr_weekly_receiving.to_dict('records')

        # Rosters
        player_seasonal_roster = self.seasonal_rosters[self.seasonal_rosters['player_name'] == player_name]
        player_weekly_roster = self.weekly_rosters[self.weekly_rosters['player_name'] == player_name]
        stats['seasonal_roster'] = player_seasonal_roster.to_dict('records')
        stats['weekly_roster'] = player_weekly_roster.to_dict('records')

        # Injuries
        player_injuries = self.injuries[self.injuries['full_name'] == player_name]
        stats['injuries'] = player_injuries.to_dict('records')

        # Depth charts
        player_depth_chart = self.depth_charts[self.depth_charts['full_name'] == player_name]
        stats['depth_chart'] = player_depth_chart.to_dict('records')

        # Combine data
        player_combine = self.combine_data[self.combine_data['player_name'] == player_name]
        stats['combine_data'] = player_combine.to_dict('records')

        # Next Gen Stats
        player_ngs_passing = self.ngs_passing[self.ngs_passing['player_display_name'] == player_name]
        player_ngs_receiving = self.ngs_receiving[self.ngs_receiving['player_display_name'] == player_name]
        player_ngs_rushing = self.ngs_rushing[self.ngs_rushing['player_display_name'] == player_name]
        stats['ngs_passing'] = player_ngs_passing.to_dict('records')
        stats['ngs_receiving'] = player_ngs_receiving.to_dict('records')
        stats['ngs_rushing'] = player_ngs_rushing.to_dict('records')

        # IDs mapping
        player_ids = self.ids[self.ids['name'] == player_name]
        stats['ids'] = player_ids.to_dict('records')

        # QBR data
        player_qbr = self.qbr_data[self.qbr_data['name_display'] == player_name]
        stats['qbr'] = player_qbr.to_dict('records')

        # Snap counts
        player_snap_counts = self.snap_counts[self.snap_counts['player'] == player_name]
        stats['snap_counts'] = player_snap_counts.to_dict('records')

        # FTN data
        # Assuming there is a 'player_name' column in ftn_data
        player_ftn_data = self.ftn_data[self.ftn_data['player_name'] == player_name] if 'player_name' in self.ftn_data.columns else pd.DataFrame()
        stats['ftn_data'] = player_ftn_data.to_dict('records')

        # Check if any stats are found
        if all(len(v) == 0 for v in stats.values()):
            return f"No stats found for player {player_name}."
        else:
            return stats

    def get_team_stats(self, team_abbr: str):
        # Fetch team stats from various data frames
        stats = {}

        # Team schedules
        team_schedule = self.schedules[
            (self.schedules['away_team'] == team_abbr) | (self.schedules['home_team'] == team_abbr)
        ]
        stats['schedule'] = team_schedule.to_dict('records')

        # Team depth chart
        team_depth_chart = self.depth_charts[self.depth_charts['club_code'] == team_abbr]
        stats['depth_chart'] = team_depth_chart.to_dict('records')

        # Team injuries
        team_injuries = self.injuries[self.injuries['team'] == team_abbr]
        stats['injuries'] = team_injuries.to_dict('records')

        # Team roster
        team_roster = self.seasonal_rosters[self.seasonal_rosters['team'] == team_abbr]
        stats['roster'] = team_roster.to_dict('records')

        # Win totals
        team_win_totals = self.win_totals[self.win_totals['abbr'] == team_abbr]
        stats['win_totals'] = team_win_totals.to_dict('records')

        # Scoring lines
        team_sc_lines = self.sc_lines[
            (self.sc_lines['away_team'] == team_abbr) | (self.sc_lines['home_team'] == team_abbr)
        ]
        stats['scoring_lines'] = team_sc_lines.to_dict('records')

        # Officials for team's games
        team_games = self.schedules[
            (self.schedules['away_team'] == team_abbr) | (self.schedules['home_team'] == team_abbr)
        ]['game_id']
        team_officials = self.officials[self.officials['game_id'].isin(team_games)]
        stats['officials'] = team_officials.to_dict('records')

        # Return the collected stats
        return stats

    def get_draft_picks(self, season: int = None):
        if season:
            draft_picks = self.draft_picks[self.draft_picks['season'] == season]
        else:
            draft_picks = self.draft_picks
        return draft_picks.to_dict('records')

    def get_draft_values(self):
        return self.draft_values.to_dict('records')

    def get_team_description(self, team_abbr: str):
        team_info = self.team_desc[self.team_desc['team_abbr'] == team_abbr]
        return team_info.to_dict('records')

    def get_officials(self, game_id: str = None):
        if game_id:
            officials = self.officials[self.officials['game_id'] == game_id]
        else:
            officials = self.officials
        return officials.to_dict('records')

    def get_ftn_data(self, **filters):
        ftn_data = self.ftn_data
        for key, value in filters.items():
            if key in ftn_data.columns:
                ftn_data = ftn_data[ftn_data[key] == value]
        return ftn_data.to_dict('records')

    # You can add more methods to interact with other data frames as needed
