from typing import Hashable, Callable

class DAG:
    """A simple implementation of a Directed Acyclic Graph."""

    def __init__(self):
        self.dag_dict = {}        

    def add_node(self, node_to_add: Hashable):
        if node_to_add in self.dag_dict.keys():
            return
        
        self.dag_dict[node_to_add] = []

    def remove_node(self, node_to_remove: Hashable):
        if node_to_remove not in self.dag_dict.keys():
            return
        
        del self.dag_dict[node_to_remove]

        # Remove all edges to this node.
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

        if not self.has_path(target_node, source_node):
            self.dag_dict[source_node].remove(target_node)
            raise ValueError(f"Adding the edge from {source_node} to {target_node} failed, as it would result in a cycle!")

    def remove_edge(self, edge_to_remove: tuple):
        """Remove an edge."""
        if len(edge_to_remove) != 2:
            raise ValueError("Edge tuple must contain exactly two nodes.")
        
        if not isinstance(edge_to_remove[0], Hashable) or not isinstance(edge_to_remove[1], Hashable):
            raise ValueError("Nodes in the edge must both be Hashable types")
        
        source_node = edge_to_remove[0]
        target_node = edge_to_remove[1]

        self.dag_dict[source_node].remove(target_node)

    def successors(self, node: Hashable):
        return self.dag_dict[node]
    
    def predecessors(self, node: Hashable):        
        return [n for n in self.dag_dict if node in self.dag_dict[n]]
    
    def indegree(self, node: Hashable):
        return len(self.predecessors(node))
    
    def outdegree(self, node: Hashable):
        return len(self.successors(node))
    
    def descendants(self, node: Hashable):
        """Get all downstream descendants of a node in no particular order."""
        descendants = set()

        def recurse_descendants(current_node):
            for successor in self.successors(current_node):
                if successor not in descendants:
                    descendants.add(successor)
                    recurse_descendants(successor)

        recurse_descendants(node)
        return list(descendants)

    def ancestors(self, node: Hashable):
        """Get all upstream ancestors of a node in no particular order."""
        ancestors = set()

        def recurse_ancestors(current_node):
            for predecessor in self.predecessors(current_node):
                if predecessor not in ancestors:
                    ancestors.add(predecessor)
                    recurse_ancestors(predecessor)

        recurse_ancestors(node)
        return list(ancestors)

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
            self.remove_edge(edge)

        # Add all of the reversed edges
        for edge in edges:
            reversed_edge = (edge[1], edge[0],)
            self.add_edge(reversed_edge)

    def is_acyclic(self) -> bool:
        """Return True if the graph is acyclic, otherwise False, using DFS to detect cycles."""
        visited = set()
        recursion_stack = set()

        def dfs(node):
            # If the node is already in the recursion stack, we have a cycle
            if node in recursion_stack:
                return False
            # If the node has been visited and is not in the recursion stack, skip it
            if node in visited:
                return True

            # Mark the node as visited and add to the recursion stack
            visited.add(node)
            recursion_stack.add(node)

            # Recursively visit all successors
            for successor in self.successors(node):
                if not dfs(successor):
                    return False

            # Remove from recursion stack after all successors are visited
            recursion_stack.remove(node)
            return True

        # Check each node to ensure all components are covered
        for node in self.nodes():
            if node not in visited:
                if not dfs(node):
                    return False

        return True
    
    def topological_sort(self) -> list:
        """Return a topological sort of the DAG if it exists, else raise a ValueError for cyclic graphs."""
        # Create a dictionary to track the indegree of each node
        indegree_map = {node: self.indegree(node) for node in self.nodes()}
        # Initialize a list to hold nodes with zero indegree
        zero_indegree_nodes = [node for node, indegree in indegree_map.items() if indegree == 0]
        sorted_nodes = []

        while zero_indegree_nodes:
            # Remove a node with zero indegree
            current_node = zero_indegree_nodes.pop()
            # Add it to the sorted list
            sorted_nodes.append(current_node)

            # For each successor of the current node, decrease its indegree by 1
            for successor in self.successors(current_node):
                indegree_map[successor] -= 1
                # If indegree becomes zero, add the successor to the list of zero indegree nodes
                if indegree_map[successor] == 0:
                    zero_indegree_nodes.append(successor)

        # Check if the sorting includes all nodes (to ensure there's no cycle)
        if len(sorted_nodes) != len(self.nodes()):
            raise ValueError("Graph contains a cycle, so topological sort is not possible")

        return sorted_nodes

    def topological_generations(self) -> list:
        """Return the nodes in each topological generation as a list of lists."""
        # Create a dictionary to track the indegree of each node
        indegree_map = {node: self.indegree(node) for node in self.nodes()}
        # Initialize a list to hold nodes with zero indegree (initial generation)
        zero_indegree_nodes = [node for node, indegree in indegree_map.items() if indegree == 0]
        generations = []

        while zero_indegree_nodes:
            # Current generation will be all nodes with zero indegree
            current_generation = zero_indegree_nodes[:]
            generations.append(current_generation)
            next_generation = []

            # Process each node in the current generation
            for node in current_generation:
                # Remove it from zero_indegree_nodes
                zero_indegree_nodes.remove(node)
                # For each successor, reduce its indegree by 1
                for successor in self.successors(node):
                    indegree_map[successor] -= 1
                    # If indegree becomes zero, it belongs to the next generation
                    if indegree_map[successor] == 0:
                        next_generation.append(successor)

            # Update zero_indegree_nodes with the nodes in the next generation
            zero_indegree_nodes = next_generation

        # Check if we covered all nodes (if not, the graph has a cycle)
        if sum(len(gen) for gen in generations) != len(self.nodes()):
            raise ValueError("Graph contains a cycle, so topological generations are not possible")

        return generations
    
    def sorted_topological_generations(self, key: Callable = str) -> list:
        """Return the nodes in each topological generation as a list of lists,
        sorted within each generation based on the provided key."""
        # Get the topological generations without sorting within each generation
        generations = self.topological_generations()
        # Sort each generation based on the key
        sorted_generations = [sorted(generation, key=key) for generation in generations]
        return sorted_generations

    def has_path(self, start: Hashable, end: Hashable) -> bool:
        """Check if there is a path from start node to end node using DFS."""
        visited = set()

        def dfs(node):
            if node == end:
                return True
            visited.add(node)
            for successor in self.successors(node):
                if successor not in visited and dfs(successor):
                    return True
            return False

        return dfs(start)