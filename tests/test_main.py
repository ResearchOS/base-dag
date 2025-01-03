"""Test main code."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from base_dag import DAG


def test_create_dag(dag: DAG):
    assert dag.nodes == (1, 2, 3, 4)
    assert dag.edges == (
        (1, 2),
        (3, 4),
    )


def test_remove_node(dag: DAG):
    dag.remove_node(4)
    assert dag.nodes == (1, 2, 3)
    assert dag.edges == ((1, 2),)


def test_add_node_via_edge(dag: DAG):
    dag.add_edge(4, 5)
    assert dag.nodes == (1, 2, 3, 4, 5)
    assert dag.edges == (
        (1, 2),
        (3, 4),
        (4, 5),
    )


def test_successors(dag: DAG):
    dag.add_edge(1, 3)
    successors = dag.successors(1)
    assert set(successors) == {2, 3}

    predecessors = dag.predecessors(3)
    assert predecessors == [1]


def test_indegree_outdegree(dag: DAG):
    indeg = dag.in_degree(1)
    assert indeg == 0
    outdeg = dag.out_degree(1)
    assert outdeg == 1


def test_descendants(dag: DAG):
    desc = dag.descendants(1)
    assert set(desc) == {2}
    dag.add_edge(2, 3)
    desc = dag.descendants(1)
    assert set(desc) == {2, 3, 4}
    desc = dag.descendants(1, include_node=True)
    assert set(desc) == {1, 2, 3, 4}


def test_ancestors(dag: DAG):
    anc = dag.ancestors(4)
    assert set(anc) == {3}
    dag.add_edge(2, 3)
    anc = dag.ancestors(4)
    assert set(anc) == {1, 2, 3}
    anc = dag.ancestors(4, include_node=True)
    assert set(anc) == {1, 2, 3, 4}


def test_subgraph(dag: DAG):
    subgraph = dag.subgraph([1, 2, 3])
    assert subgraph.nodes == (
        1,
        2,
        3,
    )
    assert subgraph.edges == ((1, 2),)


def test_topological_sort(dag: DAG):
    sorted_nodes = dag.topological_sort()
    assert sorted([1, 2, 3, 4]) == sorted(sorted_nodes)


def test_relabel_nodes(dag: DAG):
    mapping = {1: "1", 2: "2", 3: "3", 4: "4"}
    dag.relabel_nodes(mapping)
    assert set(dag.nodes) == set(mapping.values())


if __name__ == "__main__":
    pytest.main([__file__])
