from __future__ import annotations
from datetime import datetime
from typing import List

from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    SmallInteger,
    DateTime,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from schemas import League, Season
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    pass


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # Relationships
    home_matches: Mapped[List["Match"]] = relationship(
        "Match", foreign_keys="Match.home_team_id", back_populates="home_team"
    )
    away_matches: Mapped[List["Match"]] = relationship(
        "Match", foreign_keys="Match.away_team_id", back_populates="away_team"
    )
    player_match_reports: Mapped[List["PlayerMatchReport"]] = relationship(
        "PlayerMatchReport",
        foreign_keys="PlayerMatchReport.team_id",
        back_populates="team",
    )


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # Relationships
    reports: Mapped[List["PlayerMatchReport"]] = relationship(back_populates="player")
    probabilities: Mapped[List["PlayerMatchProbabilities"]] = relationship(
        back_populates="player"
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    league: Mapped[League] = mapped_column(Enum(League))
    season: Mapped[Season] = mapped_column(Enum(Season))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # Relationships
    home_team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[home_team_id],
        back_populates="home_matches",
    )
    away_team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[away_team_id],
        back_populates="away_matches",
    )
    player_match_reports: Mapped[List["PlayerMatchReport"]] = relationship(
        back_populates="match"
    )
    player_match_probabilities: Mapped[List["PlayerMatchProbabilities"]] = relationship(
        back_populates="match"
    )

    __table_args__ = (UniqueConstraint("season", "home_team_id", "away_team_id"),)


class PlayerMatchReport(Base):
    __tablename__ = "player_match_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    started: Mapped[bool] = mapped_column(Boolean)
    min: Mapped[int] = mapped_column(SmallInteger)
    sh: Mapped[int] = mapped_column(SmallInteger)
    sot: Mapped[int] = mapped_column(SmallInteger)
    fls: Mapped[int] = mapped_column(SmallInteger)
    fld: Mapped[int] = mapped_column(SmallInteger)

    # Relationships
    player: Mapped["Player"] = relationship(back_populates="reports")
    match: Mapped["Match"] = relationship(back_populates="player_match_reports")
    team: Mapped["Team"] = relationship(back_populates="player_match_reports")


class PlayerMatchProbabilities(Base):
    __tablename__ = "players_match_probabilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    probabilities: Mapped[dict] = mapped_column(JSONB)

    # Relationships
    match: Mapped["Match"] = relationship(back_populates="player_match_probabilities")
    player: Mapped["Player"] = relationship(back_populates="probabilities")
