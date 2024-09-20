import pandas as pd
from data.stats_dataframes import weekly_data, seasonal_data

class StatsRetriever:
    def __init__(self):
        self.weekly_data = weekly_data
        self.seasonal_data = seasonal_data

    def get_player_stats(self, player_name):
        # Fetch stats for a specific player
        player_stats_weekly = self.weekly_data[self.weekly_data['player_name'] == player_name]
        player_stats_seasonal = self.seasonal_data[self.seasonal_data['player_name'] == player_name]
        if player_stats_weekly.empty and player_stats_seasonal.empty:
            return f"No stats found for player {player_name}."
        else:
            return {
                'weekly_stats': player_stats_weekly.to_dict('records'),
                'seasonal_stats': player_stats_seasonal.to_dict('records')
            }