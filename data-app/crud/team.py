from models import Team, League, Match


def create_team(name: str, league: League) -> Team:
    team = Team.create(name=name, league=league)
    return team


def get_team_by_name(name: str) -> Match:
    team = Team.get(Team.name == name)
    return team


team = get_team_by_name("")

team.home_team.id
