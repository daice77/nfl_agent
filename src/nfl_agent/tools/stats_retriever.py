from typing import Any, Dict, List, Optional

from data.stats_dataframes import (
    combine_data,
    depth_charts,
    draft_picks,
    draft_values,
    ftn_data,
    ids,
    injuries,
    ngs_passing,
    ngs_receiving,
    ngs_rushing,
    officials,
    pfr_seasonal_passing,
    pfr_seasonal_receiving,
    pfr_seasonal_rushing,
    pfr_weekly_passing,
    pfr_weekly_receiving,
    pfr_weekly_rushing,
    qbr_data,
    sc_lines,
    schedules,
    seasonal_data,
    seasonal_rosters,
    snap_counts,
    team_desc,
    weekly_data,
    weekly_rosters,
    win_totals,
)


class StatsRetriever:
    def __init__(self):
        self.data_frames = {
            "weekly_data": weekly_data,
            "seasonal_data": seasonal_data,
            "seasonal_rosters": seasonal_rosters,
            "weekly_rosters": weekly_rosters,
            "win_totals": win_totals,
            "sc_lines": sc_lines,
            "officials": officials,
            "draft_picks": draft_picks,
            "draft_values": draft_values,
            "team_desc": team_desc,
            "schedules": schedules,
            "combine_data": combine_data,
            "ids": ids,
            "ngs_passing": ngs_passing,
            "ngs_receiving": ngs_receiving,
            "ngs_rushing": ngs_rushing,
            "depth_charts": depth_charts,
            "injuries": injuries,
            "qbr_data": qbr_data,
            "pfr_seasonal_passing": pfr_seasonal_passing,
            "pfr_seasonal_rushing": pfr_seasonal_rushing,
            "pfr_seasonal_receiving": pfr_seasonal_receiving,
            "pfr_weekly_passing": pfr_weekly_passing,
            "pfr_weekly_rushing": pfr_weekly_rushing,
            "pfr_weekly_receiving": pfr_weekly_receiving,
            "snap_counts": snap_counts,
            "ftn_data": ftn_data,
        }
        self.load_data_frames()

    def load_data_frames(self):
        for name, df in self.data_frames.items():
            setattr(self, name, df)

    def get_player_stats(self, player_name: str) -> Dict[str, List[Dict[str, Any]]]:
        stats = {}
        for df_name, df in self.data_frames.items():
            if "player_name" in df.columns:
                player_data = df[df["player_name"] == player_name]
            elif "player" in df.columns:
                player_data = df[df["player"] == player_name]
            elif "full_name" in df.columns:
                player_data = df[df["full_name"] == player_name]
            elif "name_display" in df.columns:
                player_data = df[df["name_display"] == player_name]
            elif "player_display_name" in df.columns:
                player_data = df[df["player_display_name"] == player_name]
            else:
                continue

            if not player_data.empty:
                stats[df_name] = player_data.to_dict("records")

        if not stats:
            return {"error": f"No stats found for player {player_name}."}
        return stats

    def get_team_stats(self, team_abbr: str) -> Dict[str, List[Dict[str, Any]]]:
        stats = {}
        for df_name, df in self.data_frames.items():
            if "team" in df.columns:
                team_data = df[df["team"] == team_abbr]
            elif "away_team" in df.columns and "home_team" in df.columns:
                team_data = df[
                    (df["away_team"] == team_abbr) | (df["home_team"] == team_abbr)
                ]
            elif "club_code" in df.columns:
                team_data = df[df["club_code"] == team_abbr]
            elif "abbr" in df.columns:
                team_data = df[df["abbr"] == team_abbr]
            else:
                continue

            if not team_data.empty:
                stats[df_name] = team_data.to_dict("records")

        if not stats:
            return {"error": f"No stats found for team {team_abbr}."}
        return stats

    def get_draft_picks(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        if season:
            draft_picks = self.draft_picks[self.draft_picks["season"] == season]
        else:
            draft_picks = self.draft_picks
        return draft_picks.to_dict("records")

    def get_draft_values(self) -> List[Dict[str, Any]]:
        return self.draft_values.to_dict("records")

    def get_team_description(self, team_abbr: str) -> List[Dict[str, Any]]:
        team_info = self.team_desc[self.team_desc["team_abbr"] == team_abbr]
        return team_info.to_dict("records")

    def get_officials(self, game_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if game_id:
            officials = self.officials[self.officials["game_id"] == game_id]
        else:
            officials = self.officials
        return officials.to_dict("records")

    def get_ftn_data(self, **filters) -> List[Dict[str, Any]]:
        ftn_data = self.ftn_data
        for key, value in filters.items():
            if key in ftn_data.columns:
                ftn_data = ftn_data[ftn_data[key] == value]
        return ftn_data.to_dict("records")

    def get_schedules(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        if season:
            schedules = self.schedules[self.schedules["season"] == season]
        else:
            schedules = self.schedules
        return schedules.to_dict("records")

    def get_injuries(self, team: Optional[str] = None) -> List[Dict[str, Any]]:
        if team:
            injuries = self.injuries[self.injuries["team"] == team]
        else:
            injuries = self.injuries
        return injuries.to_dict("records")

    def get_snap_counts(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        if season:
            snap_counts = self.snap_counts[self.snap_counts["season"] == season]
        else:
            snap_counts = self.snap_counts
        return snap_counts.to_dict("records")

    def get_stats(self, query: str) -> Dict[str, Any]:
        query_parts = query.lower().split()
        if "player" in query_parts:
            player_name = " ".join(query_parts[query_parts.index("player") + 1 :])
            return self.get_player_stats(player_name)
        elif "team" in query_parts:
            team_abbr = query_parts[query_parts.index("team") + 1]
            if "description" in query_parts:
                return self.get_team_description(team_abbr)
            return self.get_team_stats(team_abbr)
        elif "draft" in query_parts:
            if "picks" in query_parts and "season" in query_parts:
                season = int(query_parts[query_parts.index("season") + 1])
                return self.get_draft_picks(season)
            elif "values" in query_parts:
                return self.get_draft_values()
        elif "officials" in query_parts:
            if "game" in query_parts:
                game_id = query_parts[query_parts.index("game") + 1]
                return self.get_officials(game_id)
            else:
                return self.get_officials()
        elif "schedules" in query_parts:
            if "season" in query_parts:
                season = int(query_parts[query_parts.index("season") + 1])
                return self.get_schedules(season)
            else:
                return self.get_schedules()
        elif "injuries" in query_parts:
            if "team" in query_parts:
                team = query_parts[query_parts.index("team") + 1]
                return self.get_injuries(team)
            else:
                return self.get_injuries()
        elif "snap" in query_parts and "counts" in query_parts:
            if "season" in query_parts:
                season = int(query_parts[query_parts.index("season") + 1])
                return self.get_snap_counts(season)
            else:
                return self.get_snap_counts()
        elif "ftn" in query_parts:
            filters = {}
            for part in query_parts:
                if "=" in part:
                    key, value = part.split("=")
                    filters[key] = value
            return self.get_ftn_data(**filters)
        else:
            return {
                "error": "Invalid query. Please specify player, team, or other specific stats you're looking for."
            }


# Example usage
if __name__ == "__main__":
    retriever = StatsRetriever()
    print(retriever.get_stats("player Tom Brady"))
    print(retriever.get_stats("team NE"))
    print(retriever.get_stats("draft picks season 2021"))
    print(retriever.get_stats("officials game 2021091200"))
    print(retriever.get_stats("schedules season 2022"))
    print(retriever.get_stats("injuries team NE"))
    print(retriever.get_stats("snap counts season 2022"))
    print(retriever.get_stats("team description NE"))
    print(retriever.get_stats("ftn position=QB"))
