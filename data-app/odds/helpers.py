from schemas import League, Field
from .schema import Match

league_to_ext: dict[League, str] = {
    League.PREMIER_LEAGUE: "/english/premier-league",
    League.CHAMPIONSHIP: "/english/championship",
}

league_to_team_selector: dict[League, str] = {
    League.PREMIER_LEAGUE: "div[class*='TeamWrapper']",
    League.CHAMPIONSHIP: "div[class*='TeamWrapper']",
}

field_to_str: dict[Field, str] = {
    Field.SH: "Player Shots",
    Field.SOT: "Player Shots On Target",
}

OC_TO_FBREF_TEAM = {
    # Premier League
    "Brighton": "Brighton & Hove Albion",
    "Leeds": "Leeds United",
    "Man City": "Manchester City",
    "Man Utd": "Manchester Utd",
    "Newcastle": "Newcastle United",
    "Tottenham": "Tottenham Hotspur",
    "West Ham": "West Ham United",
    "Wolverhampton": "Wolverhampton Wanderers",
}

FBREF_TO_OC_TEAM = {v: k for k, v in OC_TO_FBREF_TEAM.items()}


def convert_to_fbref_team(team: str) -> str:
    return OC_TO_FBREF_TEAM.get(team, team)


def convert_to_oc_team(team: str) -> str:
    return FBREF_TO_OC_TEAM.get(team, team)


def slugify(input: str) -> str:
    return input.replace(" ", "-").lower()


def get_odds_ext(match: Match) -> str:
    league_ext = league_to_ext[match.league]

    home = slugify(convert_to_oc_team(match.home_team))
    away = slugify(convert_to_oc_team(match.away_team))

    return f"{league_ext}/{home}-v-{away}/winner"
