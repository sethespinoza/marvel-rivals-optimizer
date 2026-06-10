import networkx as nx
from sqlalchemy.orm import Session
from app.db.models import Hero, Counter

def build_hero_graph(db: Session, rank_bracket: str) -> nx.DiGraph:
    """
    Build a directed weighted graph of hero counter relationships.

    Nodes: every hero (keyed by hero_id, with name and role as attributes)
    Edges: counter relationships for the given rank bracket
           direction: from_hero_id -> to_hero_id means from_hero COUNTERS to_hero
           weight: win_rate_delta (how strongly the counter applies)
    
    Args:
        db: SQLAlchemy session (used to query heroes and counters)
        rank_bracket: e.g. "diamond" (filters counters to the right rank data)
    
    Returns:
        nx.DiGraph with all heroes as nodes and rank-appropriate counter edges
    """

    # Build directed graph object
    G = nx.DiGraph()

    # Add every hero as a node
    heroes = db.query(Hero).all()
    for hero in heroes:
        G.add_node(
            hero.hero_id,
            name=hero.name,
            role=hero.role,
        )
    
    # Add counter relationships as directed, weighted edges
    counters = (
        db.query(Counter)
        .filter(Counter.rank_bracket == rank_bracket)
        .all()
    )
    for counter in counters:
        G.add_edge(
            counter.from_hero_id,
            counter.to_hero_id,
            weight=float(counter.win_rate_delta),
        )
    
    return G