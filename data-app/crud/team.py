from models import Team


def get_team_by_name(name: str) -> Team:
    team = Team.get(Team.name == name)
    return team
