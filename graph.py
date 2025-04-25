# graph.py

import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = {}

    def add_edge(self, from_node, to_node, base_weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node][to_node] = base_weight

    def get_neighbors(self, node):
        return self.edges.get(node, {})

def build_city_graph():
    graph = Graph()

    graph.add_edge("Tehran", "Qom", 10)
    graph.add_edge("Qom", "Esfahan", 20)
    graph.add_edge("Tehran", "Esfahan", 40)
    graph.add_edge("Esfahan", "Shiraz", 30)
    graph.add_edge("Qom", "Shiraz", 60)
    graph.add_edge("Shiraz", "Bushehr", 25)
    graph.add_edge("Tehran", "Sari", 15)
    graph.add_edge("Sari", "Gorgan", 10)
    graph.add_edge("Gorgan", "Mashhad", 30)
    graph.add_edge("Esfahan", "Yazd", 18)
    graph.add_edge("Yazd", "Kerman", 22)
    graph.add_edge("Kerman", "Zahedan", 35)
    graph.add_edge("Mashhad", "Neyshabur", 8)
    graph.add_edge("Neyshabur", "Sabzevar", 10)
    graph.add_edge("Esfahan", "Ahvaz", 45)
    graph.add_edge("Ahvaz", "BandarAbbas", 40)
    graph.add_edge("Bushehr", "BandarAbbas", 30)
    graph.add_edge("BandarAbbas", "Zahedan", 60)

    return graph

def draw_graph(graph):
    G = nx.DiGraph()
    for from_node, neighbors in graph.edges.items():
        for to_node, weight in neighbors.items():
            G.add_edge(from_node, to_node, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("City Route Graph")
    plt.show()
