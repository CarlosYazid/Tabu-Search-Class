"""Evalúa una respuesta externa al CVRP de distribución de vacunas (Trípoli, Libia).
"""
from pathlib import Path

import pandas as pd
import pytest

from test.utils import solve_with_tabu_search

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="session")
def data() -> dict:
    """Carga los datos desde data/*.parquet (ver data/Info.md)."""

    time_df = pd.read_parquet(DATA_DIR / "time.parquet")
    dist_df = pd.read_parquet(DATA_DIR / "distance.parquet")
    demand_df = pd.read_parquet(DATA_DIR / "demand.parquet")
    p = pd.read_parquet(DATA_DIR / "params.parquet").iloc[0]

    names = list(time_df.index)
    assert list(time_df.columns) == names == list(dist_df.index) == list(demand_df["Location"])

    return {
        "names": names,
        "time": time_df.to_numpy(dtype=int).tolist(),
        "distance": dist_df.to_numpy(dtype=float).tolist(),
        "demand": demand_df["Demand (units)"].astype(int).tolist(),
        "num_vehicles": int(p["Number of vehicles"]),
        "capacity": int(p["Vehicle capacity (each)"]),
        "depot": int(p["Depot index"]),
        "cost_per_km": float(p["Cost per km"]),
        "cost_per_min": float(p["Cost per minute"]),
    }