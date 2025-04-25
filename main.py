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

# main.py

from scenarios import get_scenario_weight
from graph import build_city_graph, draw_graph
import heapq
import requests

def dijkstra(graph, start, end, scenario_description):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)

        if node == end:
            return cost, path

        for neighbor, base_weight in graph.get_neighbors(node).items():
            if neighbor not in visited:
                scenario_weight = get_scenario_weight(scenario_description)
                total_weight = base_weight + scenario_weight
                heapq.heappush(queue, (cost + total_weight, neighbor, path))

    return float("inf"), []

def get_weather_condition_for_route(source, destination):
    prompt = (
        f"Please provide the current weather and traffic condition between '{source}' and '{destination}' in short."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        return message.strip()
    except Exception as e:
        print(f"Error fetching data from GROQ: {e}")
        print(response.text)
        return "Clear weather, light traffic"

def main():
    graph = build_city_graph()
    draw_graph(graph)

    print("\n🚗 Intelligent City Route Planner")

    source = input("Enter source city: ")
    destination = input("Enter destination city: ")

    print("\nFetching live scenario...")
    scenario = get_weather_condition_for_route(source, destination)
    print(f"Live scenario received: {scenario}")

    cost, path = dijkstra(graph, source, destination, scenario)

    if path:
        print("\nOptimal Path:")
        print(" → ".join(path))
        print(f"Total Cost: {cost}")
    else:
        print("No path found between cities.")

if __name__ == "__main__":
    main()

# scenarios.py

def get_scenario_weight(scenario):
    scenario = scenario.lower()

    mapping = {
        "light traffic": 0,
        "moderate traffic": 1,
        "heavy traffic": 2,
        "rain": 1,
        "snow": 2,
        "storm": 3,
        "fog": 1,
        "clear": 0,
        "cloudy": 0,
        "road block": 3,
        "accident": 2,
        "flood": 3,
        "construction": 2,
    }

    weight = 0
    for key, val in mapping.items():
        if key in scenario:
            weight = max(weight, val)

    return weight
