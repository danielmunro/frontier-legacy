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


def get_path(scene: Scene, start, end):
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
        neighbor_coords = [
            (this_move.coords[0] - 1, this_move.coords[1]),
            (this_move.coords[0] + 1, this_move.coords[1]),
            (this_move.coords[0], this_move.coords[1] - 1),
            (this_move.coords[0], this_move.coords[1] + 1),
        ]
        for neighbor_coord in neighbor_coords:
            if 0 < neighbor_coord[0] < len(scene.resources[0]) and 0 < neighbor_coord[1] < len(scene.resources) and \
                    scene.resources[neighbor_coord[1]][neighbor_coord[0]] == 0:
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
