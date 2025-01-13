"""Useful fixtures for the tests."""

import pytest

from base_dag import DAG


@pytest.fixture
def dag() -> DAG:
    """Create a DAG instance for tests."""
    dag = DAG()
    dag.add_node(1)
    dag.add_node(2)
    dag.add_nodes_from((1, 2, 3, 4))
    dag.add_edges_from(
        ((1, 2), (3, 4)),
    )
    return dag
