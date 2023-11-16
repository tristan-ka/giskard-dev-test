import heapq
import numpy as np
import sys
import json
import sqlite3
import os

sys.path.append('.')
from src.utils import create_graph, convert_to_undirected_graph, convert_bounty_hunters_dict

def compute_paths(graph, start, destination, car_autonomy, count_down):
    """
    Transversal search of the graph of the universe to output all the possible path starting form planet start
    and reaching planet destination considering car_autonomy and before count_down
    """

    # Create a priority queue to keep track of stuff
    pq = [(0, start, car_autonomy, [start], [0], [])]  # (time, planet, car_autonomy, path, time_path, refuel_mask)
    visited_states = set()
    possible_paths = []
    while pq:

        time, planet, current_autonomy, path, time_path, refuel_mask = heapq.heappop(pq)

        # Check if the current state has been visited
        state = (planet, current_autonomy, tuple(path))
        if state in visited_states:
            continue
        visited_states.add(state)

        if planet == destination and time <= count_down:
            possible_paths.append({'time': time, 'path': path, 'time_path': time_path, 'refuel_mask': refuel_mask})

        if time > count_down:
            return possible_paths

        for neighbor, time_to_neighbor in graph[planet]:
            if time_to_neighbor <= current_autonomy:
                travel_time = time_to_neighbor
                if neighbor == planet:  # if we just wait on a planet we do not consume fuel
                    new_autonomy = current_autonomy
                else:
                    new_autonomy = current_autonomy - travel_time
                new_planet = neighbor
                refuel = False
            else:
                travel_time = 1
                new_autonomy = car_autonomy
                new_planet = planet
                refuel = True

            new_time = time + travel_time
            new_path = path + [new_planet]
            new_time_path = time_path + [new_time]
            new_refuel_mask = refuel_mask + [refuel]
            heapq.heappush(pq, (new_time, new_planet, new_autonomy, new_path, new_time_path, new_refuel_mask))

    return possible_paths  # Destination is not reachable


def count_encounters(possible_paths, hunters_dict):
    """
    given the list of possible paths and bounty_hunters info count the number of encounters with hunters and calculate
    the associated proba to reach destination.
    """
    for path in possible_paths:
        counter = 0
        for planet, day in zip(path['path'], path['time_path']):
            if planet in hunters_dict.keys():
                if day in hunters_dict[planet]:
                    counter += 1
        path['counter'] = counter
        if counter >= 1:
            path['proba'] = 1 - np.sum([9 ** i / (10 ** (i + 1)) for i in range(counter)])
        else:
            path['proba'] = 1
    return possible_paths


def output_odds(possible_paths):
    if possible_paths:
        index_path = np.argmax([possible_paths[i]['proba'] for i in range(len(possible_paths))])
        proba = possible_paths[index_path]['proba']
        path = possible_paths[index_path]['path']
        time_path = possible_paths[index_path]['time_path']
    else:
        proba = 0
        path = []
        time_path = []
    return proba * 100, path, time_path


def main():
    if len(sys.argv) != 3:
        raise "Wrong usage of scripy calculate_odds.py. Script needs two arguments respectively the paths toward the millennium-falcon.json and empire.json files"

    millenium_file = sys.argv[1]
    empire_file = sys.argv[2]
    dir_name = os.path.dirname(millenium_file)

    with open(millenium_file, 'r') as f:
        millenium_data = json.load(f)
    with open(empire_file, 'r') as f:
        empire_data = json.load(f)

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

    count_down = empire_data['countdown']
    bounty_hunters = empire_data['bounty_hunters']
    hunters_dict = convert_bounty_hunters_dict(bounty_hunters)

    possible_paths = compute_paths(graph, start_planet, destination_planet, car_autonomy, count_down)
    possible_paths = count_encounters(possible_paths, hunters_dict)
    odds, final_path, final_time_path = output_odds(possible_paths)

    print("The odds of reaching " + destination_planet + " from " + start_planet + " are " + str(odds) + "%")


if __name__ == '__main__':
    # Example usage:
    main()
