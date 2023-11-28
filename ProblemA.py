import networkx as nx
import matplotlib.pyplot as plt


def augmenting_path_dfs(graph, source, sink, path=[]):
    if source == sink:
        return path
    for node in graph.neighbors(source):
        print(source, "->", node)
        residual_capacity = graph[source][node]['capacity'] - \
            graph[source][node]['flow']
        if residual_capacity > 0 and node not in path:
            result = augmenting_path_dfs(
                graph, node, sink, path + [(source, node)])
            if result is not None:
                return result


def ford_fulkerson(graph, source, sink):
    max_flow = 0
    path = augmenting_path_dfs(graph, source, sink)

    while path is not None:
        # Find the minimum residual capacity along the augmenting path
        residual_capacities = [graph[u][v]['capacity'] -
                               graph[u][v]['flow'] for u, v in path]
        min_residual_capacity = min(residual_capacities)

        # Update the flow along the augmenting path
        for u, v in path:
            graph[u][v]['flow'] += min_residual_capacity
            # graph[v][u]['flow'] -= min_residual_capacity

        # Update the maximum flow
        max_flow += min_residual_capacity

        # Find the next augmenting path
        path = augmenting_path_dfs(graph, source, sink)

    return max_flow


# Create the graph
G = nx.DiGraph()
G.add_edge('s', 'a', capacity=2, flow=1)
G.add_edge('s', 'b', capacity=3, flow=0)
G.add_edge('a', 'c', capacity=1, flow=1)
G.add_edge('c', 't', capacity=2, flow=0)
G.add_edge('b', 'd', capacity=2, flow=0)
G.add_edge('c', 'd', capacity=2, flow=1)
G.add_edge('d', 't', capacity=1, flow=0)

# Find the maximum flow
max_flow = ford_fulkerson(G, 's', 't')

# Visualize the final graph with flow values
pos = {'s': (0, 1), 'a': (1, 2), 'b': (1, 0),
       'c': (2, 2), 'd': (2, 0), 't': (3, 1)}
nx.draw(G, pos, with_labels=True, node_size=700,
        node_color='#FFA500', font_size=10, font_color='black')

# Add edge labels for flow and capacity
edge_labels = {
    (u, v): f"({G[u][v]['flow']},{G[u][v]['capacity']})" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title('Maximum Flow Network')
plt.show()

print(f"Maximum Flow: {max_flow}")
