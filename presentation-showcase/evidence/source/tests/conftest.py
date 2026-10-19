"""Insumos de prueba explícitos; sin .env, Atlas ni red."""

from pathlib import Path

import pytest

from economic_graph.simulator.design import load_design
from economic_graph.simulator.project import project_observations

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def approved_design():
    return load_design(ROOT / "design-data/restricted")


@pytest.fixture
def projection(approved_design):
    return project_observations(approved_design["observations"])
