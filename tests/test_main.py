import pytest

from base_dag import DAG


def create_dag():
    dag = DAG()
    dag.add_node(1)
    dag.add_node(2)
    dag.add_nodes_from([1, 2, 3, 4])
    dag.add_edges_from(
        (
            (1, 2),
            (3, 4),
        ),
    )
    return dag


def test_create_dag():
    dag = create_dag()
    assert dag.nodes == (1, 2, 3, 4)
    assert dag.edges == (
        (1, 2),
        (3, 4),
    )


def test_remove_node():
    dag = create_dag()
    dag.remove_node(4)
    assert dag.nodes == (1, 2, 3)
    assert dag.edges == ((1, 2),)


def test_add_node_via_edge():
    dag = create_dag()
    dag.add_edge(4, 5)
    assert dag.nodes == (1, 2, 3, 4, 5)
    assert dag.edges == (
        (1, 2),
        (3, 4),
        (4, 5),
    )


def test_successors():
    dag = create_dag()
    dag.add_edge(1, 3)
    successors = dag.successors(1)
    assert set(successors) == {2, 3}

    predecessors = dag.predecessors(3)
    assert predecessors == [1]


def test_indegree_outdegree():
    dag = create_dag()
    indeg = dag.in_degree(1)
    assert indeg == 0
    outdeg = dag.out_degree(1)
    assert outdeg == 1


def test_descendants():
    dag = create_dag()
    desc = dag.descendants(1)
    assert set(desc) == {2}
    dag.add_edge(2, 3)
    desc = dag.descendants(1)
    assert set(desc) == {2, 3, 4}
    desc = dag.descendants(1, include_node=True)
    assert set(desc) == {1, 2, 3, 4}


def test_ancestors():
    dag = create_dag()
    anc = dag.ancestors(4)
    assert set(anc) == {3}
    dag.add_edge(2, 3)
    anc = dag.ancestors(4)
    assert set(anc) == {1, 2, 3}
    anc = dag.ancestors(4, include_node=True)
    assert set(anc) == {1, 2, 3, 4}


def test_subgraph():
    dag = create_dag()
    subgraph = dag.subgraph([1, 2, 3])
    assert subgraph.nodes == (
        1,
        2,
        3,
    )
    assert subgraph.edges == ((1, 2),)


def test_topological_sort():
    dag = create_dag()
    sorted_nodes = dag.topological_sort()
    assert sorted([1, 2, 3, 4]) == sorted(sorted_nodes)


def test_relabel_nodes():
    dag = create_dag()
    mapping = {1: "1", 2: "2", 3: "3", 4: "4"}
    dag.relabel_nodes(mapping)
    assert set(dag.nodes) == set(mapping.values())


if __name__ == "__main__":
    pytest.main([__file__])
