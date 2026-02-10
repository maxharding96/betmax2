from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Float, Boolean, SmallInteger, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from schemas import League, Season, PredictionField


class Base(DeclarativeBase):
    pass


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    league: Mapped[League] = mapped_column(Enum(League))

    # Relationships
    players: Mapped[List["Player"]] = relationship(back_populates="team")
    home_matches: Mapped[List["Match"]] = relationship(
        "Match", foreign_keys="[Match.home_team_id]", back_populates="home_team"
    )
    away_matches: Mapped[List["Match"]] = relationship(
        "Match", foreign_keys="[Match.away_team_id]", back_populates="away_team"
    )


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="players")
    match_reports: Mapped[List["MatchReport"]] = relationship(back_populates="player")
    match_predictions: Mapped[List["MatchPrediction"]] = relationship(
        back_populates="player"
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    match_day: Mapped[int] = mapped_column(SmallInteger)
    date: Mapped[datetime] = mapped_column(DateTime)
    season: Mapped[Season] = mapped_column(Enum(Season))

    # Coefficients
    home_attack_coeffs: Mapped[Optional[float]] = mapped_column(Float, default=None)
    away_attack_coeffs: Mapped[Optional[float]] = mapped_column(Float, default=None)
    home_defence_coeffs: Mapped[Optional[float]] = mapped_column(Float, default=None)
    away_defence_coeffs: Mapped[Optional[float]] = mapped_column(Float, default=None)

    # Relationships
    home_team: Mapped["Team"] = relationship(
        "Team", foreign_keys=[home_team_id], back_populates="home_matches"
    )
    away_team: Mapped["Team"] = relationship(
        "Team", foreign_keys=[away_team_id], back_populates="away_matches"
    )
    player_reports: Mapped[List["MatchReport"]] = relationship(back_populates="match")
    player_predictions: Mapped[List["MatchPrediction"]] = relationship(
        back_populates="match"
    )


class MatchReport(Base):
    __tablename__ = "match_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    started: Mapped[bool] = mapped_column(Boolean)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    min: Mapped[int] = mapped_column(SmallInteger)
    sh: Mapped[int] = mapped_column(SmallInteger)
    sot: Mapped[int] = mapped_column(SmallInteger)
    fls: Mapped[int] = mapped_column(SmallInteger)
    fld: Mapped[int] = mapped_column(SmallInteger)

    # Relationships
    match: Mapped["Match"] = relationship(back_populates="player_reports")
    player: Mapped["Player"] = relationship(back_populates="match_reports")


class MatchPrediction(Base):
    __tablename__ = "match_predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    field: Mapped[PredictionField] = mapped_column(Enum(PredictionField))
    value: Mapped[float] = mapped_column(Float)

    # Relationships
    match: Mapped["Match"] = relationship(back_populates="player_predictions")
    player: Mapped["Player"] = relationship(back_populates="match_predictions")
