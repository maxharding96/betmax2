from database import db
from peewee import (
    Model,
    CharField,
    IntegerField,
    ForeignKeyField,
    DateTimeField,
    SmallIntegerField,
    BooleanField,
    FloatField,
)
from schemas import League, Season, PredictionField


class BaseModel(Model):
    class Meta:
        database = db


class Team(BaseModel):
    name = CharField(unique=True)
    league = IntegerField(
        choices=[(s.value, s.name) for s in League],
    )


class Player(BaseModel):
    name = CharField(unique=True)
    team = ForeignKeyField(Team, backref="players")


class Match(BaseModel):
    home_team = ForeignKeyField(Team, backref="home_matches")
    away_team = ForeignKeyField(Team, backref="away_matches")
    match_day = SmallIntegerField()
    date = DateTimeField()
    season = IntegerField(choices=[(s.value, s.name) for s in Season])
    # coefficients
    home_attack_coeffs = FloatField(null=True, default=None)
    away_attack_coeffs = FloatField(null=True, default=None)
    home_defence_coeffs = FloatField(null=True, default=None)
    away_defence_coeffs = FloatField(null=True, default=None)


class MatchReport(BaseModel):
    started = BooleanField()
    match = ForeignKeyField(Match, backref="player_reports")
    player = ForeignKeyField(Player, backref="match_reports")
    min = SmallIntegerField()
    sh = SmallIntegerField()
    sot = SmallIntegerField()
    fls = SmallIntegerField()
    fld = SmallIntegerField()


class MatchPrediction(BaseModel):
    match = ForeignKeyField(Match, backref="player_predictions")
    player = ForeignKeyField(Player, backref="match_predictions")
    field = IntegerField(choices=[(s.value, s.name) for s in PredictionField])
    value = FloatField()
