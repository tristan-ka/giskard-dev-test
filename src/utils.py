import json
import os
import sqlite3

def create_graph(rows):
    graph = {}
    for row in rows:
        if row[0] not in graph.keys():
            graph[row[0]] = [(row[1], row[2])]
        else:
            graph[row[0]].append((row[1], row[2]))
    return graph


def convert_to_undirected_graph(graph):
    undirected_graph = {}

    for node, neighbors in graph.items():
        if node not in undirected_graph:
            undirected_graph[node] = []
        for neighbor, weight in neighbors:
            # Add the edge in both directions
            undirected_graph[node].append((neighbor, weight))
            if neighbor not in undirected_graph:
                undirected_graph[neighbor] = []
            undirected_graph[neighbor].append((node, weight))

    # add self-directed edges
    for node in undirected_graph:
        undirected_graph[node].append((node, 1))
    return undirected_graph


def convert_bounty_hunters_dict(bounty_hunters):
    out_dict = {}
    for entry in bounty_hunters:
        out_dict.setdefault(entry["planet"], []).append(entry["day"])
    return out_dict

def load_default_millenium_data():
    default_millenium_file = 'examples/example1/millennium-falcon.json'
    dir_name = os.path.dirname(default_millenium_file)
    with open(default_millenium_file, 'r') as f:
        millenium_data = json.load(f)
    db_path = os.path.join(dir_name, millenium_data['routes_db'])
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ROUTES')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    graph = create_graph(rows)
    graph = convert_to_undirected_graph(
        graph)  # Because routes can be travelled in any direction, we convert the graph to undirected

    car_autonomy = millenium_data['autonomy']
    start_planet = millenium_data['departure']
    destination_planet = millenium_data['arrival']

    return graph, car_autonomy, start_planet, destination_planet