import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import (
    Patch, Hero, Counter, Synergy, CompArchetype,
    HeroCompArchetype, Map, MapHeroPerformance,
    MetaScore, UserMatch
)

# path to seed file
SEED_FILE = os.path.join(os.path.dirname(__file__), "seed_data.json")

def load_seed_data():
    """Reads seed_data.json and inserts data into the database."""
    with open(SEED_FILE, "r") as f:
        data = json.load(f)
    
    db: Session = SessionLocal()

    try:
        print("Loading patches...")
        for item in data["patches"]:
            if not db.get(Patch, item["id"]):
                db.add(Patch(
                    id=item["id"],
                    label=item["label"],
                    released_at=datetime.fromisoformat(item["released_at"]),
                    is_current=item["is_current"]
                ))
        db.commit()
        print(f"{len(data['patches'])} patches")

        print("Loading heroes...")
        for item in data["heroes"]:
            if not db.get(Hero, item["id"]):
                db.add(Hero(
                    id=item["id"],
                    name=item["name"],
                    role=item["role"],
                    difficulty=item["difficulty"],
                    is_available=item["is_available"]
                ))
        db.commit()
        print(f"{len(data['heroes'])} heroes")

        print("Loading maps...")
        for item in data["maps"]:
            if not db.get(Map, item["id"]):
                db.add(Map(
                    id=item["id"],
                    name=item["name"],
                    game_mode=item["game_mode"]
                ))
        db.commit()
        print(f"{len(data['maps'])} maps")

        print("Loading comp archetypes...")
        for item in data["comp_archetypes"]:
            if not db.get(CompArchetype, item["id"]):
                db.add(CompArchetype(
                    id=item["id"],
                    name=item["name"],
                    description=item.get("description"),
                    strengths=item.get("strengths"),
                    weaknesses=item.get("weaknesses")
                ))
        db.commit()
        print(f"{len(data['comp_archetypes'])} comp archetypes")

        print("Loading counters...")
        inserted = 0
        for item in data["counters"]:
            exists = db.query(Counter).filter_by(
                hero_id=item["hero_id"],
                countered_by_id=item["countered_by_id"],
                rank_bracket=item["rank_bracket"]
            ).first()
            if not exists:
                db.add(Counter(
                    hero_id=item["hero_id"],
                    countered_by_id=item["countered_by_id"],
                    win_rate_delta=item["win_rate_delta"],
                    rank_bracket=item["rank_bracket"]
                ))
                inserted += 1
        db.commit()
        print(f"{inserted} counters")

        print("Loading synergies...")
        inserted = 0
        for item in data["synergies"]:
            exists = db.query(Synergy).filter_by(
                hero_a_id=item["hero_a_id"],
                hero_b_id=item["hero_b_id"],
                rank_bracket=item["rank_bracket"]
            ).first()
            if not exists:
                db.add(Synergy(
                    hero_a_id=item["hero_a_id"],
                    hero_b_id=item["hero_b_id"],
                    synergy_strength=item["synergy_strength"],
                    has_team_up_ability=item["has_team_up_ability"],
                    description=item.get("description"),
                    rank_bracket=item["rank_bracket"]
                ))
                inserted += 1
        db.commit()
        print(f"{inserted} synergies")

        print("Loading hero comp archetypes...")
        inserted = 0
        for item in data["hero_comp_archetypes"]:
            exists = db.query(HeroCompArchetype).filter_by(
                hero_id=item["hero_id"],
                archetype_id=item["archetype_id"],
                rank_bracket=item["rank_bracket"]
            ).first()
            if not exists:
                db.add(HeroCompArchetype(
                    hero_id=item["hero_id"],
                    archetype_id=item["archetype_id"],
                    fit_score=item["fit_score"],
                    rank_bracket=item["rank_bracket"]
                ))
                inserted += 1
        db.commit()
        print(f"{inserted} hero comp archetypes")

        print("Loading meta scores...")
        inserted = 0
        for item in data["meta_scores"]:
            exists = db.query(MetaScore).filter_by(
                hero_id=item["hero_id"],
                patch_id=item["patch_id"],
                rank_bracket=item["rank_bracket"]
            ).first()
            if not exists:
                db.add(MetaScore(
                    hero_id=item["hero_id"],
                    patch_id=item["patch_id"],
                    rank_bracket=item["rank_bracket"],
                    win_rate=item["win_rate"],
                    pick_rate=item["pick_rate"],
                    ban_rate=item["ban_rate"],
                    tier=item["tier"]
                ))
                inserted += 1
        db.commit()
        print(f"{inserted} meta scores")

        print("Loading map hero performance...")
        inserted = 0
        for item in data["map_hero_performance"]:
            exists = db.query(MapHeroPerformance).filter_by(
                map_id=item["map_id"],
                hero_id=item["hero_id"],
                rank_bracket=item["rank_bracket"]
            ).first()
            if not exists:
                db.add(MapHeroPerformance(
                    map_id=item["map_id"],
                    hero_id=item["hero_id"],
                    performance_delta=item["performance_delta"],
                    rank_bracket=item["rank_bracket"]
                ))
                inserted += 1
        db.commit()
        print(f"{inserted} map hero performance records")

        print("Seed data loaded successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error loading seed data: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    load_seed_data()