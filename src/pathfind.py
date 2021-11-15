from src.scene import Scene


MAX_COST_GUARD = 1000


class Node:
    previous = None
    coords = None
    cost = None
    visited = False

    def __init__(self, coords, cost, previous=None):
        self.coords = coords
        self.cost = cost
        self.previous = previous


def create_neighbors(coords):
    return [
        (coords[0] - 1, coords[1]),
        (coords[0] + 1, coords[1]),
        (coords[0], coords[1] - 1),
        (coords[0], coords[1] + 1),
    ]


def get_path(game, start, end):
    cost = 0
    known_nodes = [Node(start, cost)]
    this_move = None
    while cost < MAX_COST_GUARD:
        unvisited = list(filter(lambda i: not i.visited, known_nodes))
        sorted(unvisited, key=lambda i: i.cost)
        this_move = unvisited[0]
        this_move.visited = True
        if this_move.coords == end:
            break
        neighbor_coords = create_neighbors(this_move.coords)
        for neighbor_coord in neighbor_coords:
            if game.is_passable(neighbor_coord):
                found = list(filter(lambda i: i.coords == neighbor_coord, known_nodes))
                if len(found) == 0:
                    known_nodes.append(Node(neighbor_coord, cost, this_move))
                elif cost < found[0].cost:
                    found[0].cost = cost
        cost += 1
    if this_move.coords != end:
        return []
    path = []
    while this_move:
        path.append(this_move.coords)
        this_move = this_move.previous
    reversed(path)
    return path
