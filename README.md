# base-dag
A simple base implementation of a DAG. Users should feel free to subclass this DAG class to provide their desired functionality. The API is intended to be similar to the NetworkX API, though not an exact replica. Note that multiple edges between the same two nodes are not supported by this package.

## Creating a DAG.
 ```python
from base_dag import DAG

# Initialize the DAG
dag = DAG()

# Add nodes and edges
dag.add_nodes_from([1, 2])
dag.add_node(3)
dag.add_edge((1, 2))
dag.add_edge((2, 3))

# Remove nodes and edges
dag.remove_edge((2, 3))
dag.remove_node(3)
```

## Subgraph
```python
# Re-add a third node.
dag.add_node(3)
# Extract the subgraph of nodes 1 and 2.
sub_dag = dag.subgraph([1, 2])
```

## Other Operations
### All nodes & edges
```python
all_nodes = dag.nodes() # (1, 2, 3)
all_edges = dag.edges() # ( (1, 2), (2, 3) )
```

### Successors and Predecessors
```python
successors = dag.successors(1) # [2]
predecessors = dag.predecessors(2) # [1]
```

### Descendants and Ancestors
```python
descendants = dag.descendants(1) # [2, 3]
ancestors = dag.ancestors(2) # [1]
```

### Indegree and Outdegree
```python
in_degree = dag.indegree(2) # 1
out_degree = dag.outdegree(1) # 1
```

### Reverse
```python
# Reverse the direction of the edges in the graph in place, without affecting the nodes at all.
dag.reverse()
```

### Topological sort
```python
sorted_nodes = dag.topological_sort()
```

### Topological generations
```python
generations = dag.topological_generations()
```

### Sorted topological generations
```python
sorted_generations = dag.sorted_topological_generations()
```

### has_path
```python
has_path = dag.has_path(1, 3) # True
```

### is_acyclic
```python
is_acyclic = dag.is_acyclic() # True
```

