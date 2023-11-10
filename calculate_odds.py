import heapq

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

    for node in undirected_graph:
        undirected_graph[node].append((node, 1))
    return undirected_graph


def compute_min_days(graph, start, destination, car_autonomy, count_down):
    '''

    :param graph:
    :type graph:
    :param start:
    :type start:
    :param destination:
    :type destination:
    :param car_autonomy:
    :type car_autonomy:
    :param count_down:
    :type count_down:
    :return:
    :rtype:
    '''

    # Create a priority queue to keep track of stuff
    pq = [(0, start, car_autonomy, [start], [0], [])]  # (time, planet, car_autonomy, path, time_path, refuel_mask)

    possible_path = []
    while pq:

        time, planet, current_autonomy, path, time_path, refuel_mask = heapq.heappop(pq)

        if planet == destination and time <= count_down:
            heapq.heappop(pq)
            possible_path.append((time, path, time_path, refuel_mask))

        if time > count_down:
            return possible_path

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

    return possible_path  # Destination is not reachable


if __name__ == '__main__':
    # Example usage:
    graph = {
        'Tatooine': [('Dagobah', 6), ('Hoth', 6)],
        'Dagobah': [('Endor', 4), ('Hoth', 1)],
        'Hoth': [('Endor', 1)],
    }

    # Because routes can be travelled in any direction, we convert the graph to undirected
    graph = convert_to_undirected_graph(graph)

    bounty_hunters = [
        {"planet": "Hoth", "day": 6},
        {"planet": "Hoth", "day": 7},
        {"planet": "Hoth", "day": 8}
    ]
    start_planet = 'Tatooine'
    destination_planet = 'Endor'
    car_autonomy = 6

    count_down = 8
    possible_paths = compute_min_days(graph, start_planet, destination_planet, car_autonomy, count_down)

    print(possible_paths)
    print(len(possible_paths))
