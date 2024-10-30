from typing import Hashable

class DAG:
    """A simple implementation of a Directed Acyclic Graph."""

    def __init__(self):
        self.dag_dict = {}        

    def add_node(self, node_to_add: Hashable):
        if node_to_add in self.dag_dict.keys():
            return
        
        self.dag_dict[node_to_add] = []

    def rm_node(self, node_to_remove: Hashable):
        if node_to_remove not in self.dag_dict.keys():
            return
        
        del self.dag_dict[node_to_remove]

        # Ensure no other nodes contain this node
        for node in self.dag_dict:
            if node_to_remove in self.dag_dict[node]:
                self.dag_dict[node].pop(node_to_remove)

    def add_edge(self, edge_to_add: tuple):
        """Add an edge. Note that it cannot contain any edge information, unlike in NetworkX."""
        if len(edge_to_add) != 2:
            raise ValueError("Edge tuple must contain exactly two nodes.")
        
        if not isinstance(edge_to_add[0], Hashable) or not isinstance(edge_to_add[1], Hashable):
            raise ValueError("Nodes in the edge must both be Hashable types")
        
        source_node = edge_to_add[0]
        target_node = edge_to_add[1]

        if source_node not in self.dag_dict.keys():
            self.add_node(source_node)

        if target_node not in self.dag_dict.keys():
            self.add_node(target_node)

        if target_node in self.dag_dict[source_node]:
            return
        
        self.dag_dict[source_node].append(target_node)

    def rm_edge(self, edge_to_remove: tuple):
        """Remove an edge."""
        if len(edge_to_remove) != 2:
            raise ValueError("Edge tuple must contain exactly two nodes.")
        
        if not isinstance(edge_to_remove[0], Hashable) or not isinstance(edge_to_remove[1], Hashable):
            raise ValueError("Nodes in the edge must both be Hashable types")
        
        source_node = edge_to_remove[0]
        target_node = edge_to_remove[1]

        self.dag_dict[source_node].pop(target_node)

    def successors(self, node: Hashable):
        return self.dag_dict[node]
    
    def predecessors(self, node: Hashable):
        predecessors = []
        for n in self.dag_dict:
            if node in self.dag_dict[n]:
                predecessors.append(n)
        return predecessors
    
    def indegree(self, node: Hashable):
        return len(self.predecessors(node))
    
    def outdegree(self, node: Hashable):
        return len(self.successors(node))
    
    def descendants(self, node: Hashable):
        """Get all downstream descendants of a node, recursively."""        
        def recurse_descendants(self: DAG, node: Hashable, descendants: list = []):
            successors = self.successors(node)
            descendants.append(successors)
            for n in successors:
                descendants.append(recurse_descendants(self, node, descendants))
            return descendants

        return recurse_descendants(self, node)

    def ancestors(self, node: Hashable):
        """Get all upstream descendants of a node, recursively."""
        def recurse_ancestors(self: DAG, node: Hashable, ancestors: list = []):
            predecessors = self.predecessors(node)
            ancestors.append(predecessors)
            for n in predecessors:
                predecessors.append(recurse_ancestors(self, node, ancestors))
            return predecessors
        
        return recurse_ancestors(self, node)
    
    def nodes(self):
        """Return all of the nodes."""
        return [n for n in self.dag_dict.keys()]
    
    def edges(self):
        """Return all of the edges."""
        edges = []
        for source in self.dag_dict:
            for target in self.dag_dict[source]:
                edges.append((source, target,))

        return edges
    
    def subgraph(self, nodes_in_subgraph: list):
        """Return a subgraph of the current DAG that contains the specified nodes, and all of the edges between them."""
        subgraph = DAG()
        # Add the nodes
        for node in nodes_in_subgraph:
            subgraph.add_node(node)

        # Add the edges
        all_edges = self.edges()
        for edge in all_edges:
            source = edge[0]
            target = edge[1]
            if source not in nodes_in_subgraph or target not in nodes_in_subgraph:
                continue

            subgraph.add_edge(source, target)

        return subgraph
    
    def reverse(self):
        """Reverse the order of the edges in the DAG."""
        edges = self.edges()
        # Remove all of the edges
        for edge in edges:
            self.rm_edge(edge)

        # Add all of the reversed edges
        for edge in edges:
            reversed_edge = (edge[1], edge[0])
            self.add_edge(reversed_edge)

