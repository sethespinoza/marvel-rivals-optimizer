from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Patch(Base):
    __tablename__ = "patches"

    id = Column(String, primary_key=True) # e.g. "season-2-patch-3"
    label = Column(String, nullable=False) # e.g. "Season 2 Patch 3"
    released_at = Column(DateTime, nullable=False)
    is_current = Column(Boolean, default=False)

    meta_scores = relationship("MetaScore", back_populates="patch")

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(String, primary_key=True) # e.g. "spider-man"
    name = Column(String, nullable=False) # e.g. "Spider-Man"
    role = Column(String, nullable=False) # "duelist", "strategist", "vanguard"
    difficulty = Column(String, nullable=False) # "easy", "medium", "hard"
    is_available = Column(Boolean, default=True)

    meta_scores = relationship("MetaScore", back_populates="hero")
    counters_given = relationship(
        "Counter", foreign_keys="Counter.hero_id", back_populates="hero"
    )
    counters_received = relationship(
        "Counter", foreign_keys="Counter.countered_by_id", back_populates="countered_by"
    )
    synergies_a = relationship(
        "Synergy", foreign_keys="Synergy.hero_a_id", back_populates="hero_a"
    )
    synergies_b = relationship(
        "Synergy", foreign_keys="Synergy.hero_b_id", back_populates="hero_b"
    )
    comp_archetypes = relationship("HeroCompArchetype", back_populates="hero")
    map_performance = relationship("MapHeroPerformance", back_populates="hero")
    user_matches = relationship("UserMatch", back_populates="hero")

class Counter(Base):
    __tablename__ = "counters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    countered_by_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    win_rate_delta = Column(Float, nullable=False) # how much countered_by beats hero
    rank_bracket = Column(String, nullable=False) # "bronze-silver", "gold-platinum", etc.

    __table_args__ = (
        UniqueConstraint("hero_id", "countered_by_id", "rank_bracket"),
    )

    hero = relationship(
        "Hero", foreign_keys=[hero_id], back_populates="counters_given"
    )
    countered_by = relationship(
        "Hero", foreign_keys=[countered_by_id], back_populates="counters_received"
    )

class Synergy(Base):
    __tablename__ = "synergies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_a_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    hero_b_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    synergy_strength = Column(Float, nullable=False) # 0.0 to 1.0
    has_team_up_ability = Column(Boolean, default=False) # built-in game mechanic
    description = Column(Text, nullable=True)
    rank_bracket = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("hero_a_id", "hero_b_id", "rank_bracket"),
    )

    hero_a = relationship("Hero", foreign_keys=[hero_a_id], back_populates="synergies_a")
    hero_b = relationship("Hero", foreign_keys=[hero_b_id], back_populates="synergies_b")

class CompArchetype(Base):
    __tablename__ = "comp_archetypes"

    id = Column(String, primary_key=True) # "brawl", "dive", "poke"
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)

    heroes = relationship("HeroCompArchetype", back_populates="archetype")

class HeroCompArchetype(Base):
    __tablename__ = "hero_comp_archetypes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    archetype_id = Column(String, ForeignKey("comp_archetypes.id"), nullable=False)
    fit_score = Column(Float, nullable=False) # 0.0 to 1.0, (how well does the hero fit the comp)
    rank_bracket = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("hero_id", "archetype_id", "rank_bracket"),
    )

    hero = relationship("Hero", back_populates="comp_archetypes")
    archetype = relationship("CompArchetype", back_populates="heroes")

class Map(Base):
    __tablename__ = "maps"

    id = Column(String, primary_key=True) # "Tokyo 2099", "Yggsgard", etc.
    name = Column(String, nullable=False)
    game_mode = Column(String, nullable=False) # "Convergence", "Convoy", etc.

    hero_performance = relationship("MapHeroPerformance", back_populates="map")
    user_matches = relationship("UserMatch", back_populates="map")

class MapHeroPerformance(Base):
    __tablename__ = "map_hero_performance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_id = Column(String, ForeignKey("maps.id"), nullable=False)
    hero_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    performance_delta = Column(Float, nullable=False) # modifier vs baseline
    rank_bracket = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("map_id", "hero_id", "rank_bracket"),
    )

    map = relationship("Map", back_populates="hero_performance")
    hero = relationship("Hero", back_populates="map_performance")

class MetaScore(Base):
    __tablename__ = "meta_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    patch_id = Column(String, ForeignKey("patches.id"), nullable=False)
    rank_bracket = Column(String, nullable=False)
    win_rate = Column(Float, nullable=False)
    pick_rate = Column(Float, nullable=False)
    ban_rate = Column(Float, nullable=False)
    tier = Column(String, nullable=False) # "S", "A", "B", etc.
    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("hero_id", "patch_id", "rank_bracket"),
    )

    hero = relationship("Hero", back_populates="meta_scores")
    patch = relationship("Patch", back_populates="meta_scores")

class UserMatch(Base):
    __tablename__ = "user_matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero_id = Column(String, ForeignKey("heroes.id"), nullable=False)
    map_id = Column(String, ForeignKey("maps.id"), nullable=False)
    result = Column(String, nullable=False) # "win" or "loss"
    rank = Column(String, nullable=False) # "bronze", "silver", etc.
    rank_bracket = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    played_at = Column(DateTime, default=datetime.utcnow)

    hero = relationship("Hero", back_populates="user_matches")
    map = relationship("Map", back_populates="user_matches")






