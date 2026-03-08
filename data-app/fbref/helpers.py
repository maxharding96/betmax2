from schemas import League, Season

CURRENT_SEASON = Season.S_25


league_to_code: dict[League, int] = {League.PREMIER_LEAGUE: 9, League.CHAMPIONSHIP: 10}

league_to_str: dict[League, str] = {
    League.PREMIER_LEAGUE: "Premier-League",
    League.CHAMPIONSHIP: "Championship",
}

season_to_str: dict[Season, str] = {
    Season.S_23: "2023-2024",
    Season.S_24: "2024-2025",
    Season.S_25: "2025-2026",
}


def is_current_season(season: Season) -> bool:
    return season == CURRENT_SEASON


def get_schedule_ext(league: League, season: Season) -> str:
    league_code = league_to_code[league]
    league_str = league_to_str[league]
    season_str = season_to_str[season]

    is_current = is_current_season(season)

    season_ext = "" if is_current else "/" + {season_str}

    end_ext = f"{league_str}-Score-and-Fixtures"
    if is_current:
        end_ext = season_str + "-" + end_ext

    return f"/en/comps/{league_code}{season_ext}/schedule/{end_ext}"


def get_schedule_table_id(league: League, season: Season) -> str:
    league_code = league_to_code[league]
    season_str = season_to_str[season]

    return f"sched_{season_str}_{league_code}_1"


def get_matches_ext(date: str) -> str:
    return f"/en/matches/{date}"


str_to_league: dict[str, League] = {
    "Premier League": League.PREMIER_LEAGUE,
    "Championship": League.CHAMPIONSHIP,
}
