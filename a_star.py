# Adapted from https://www.geeksforgeeks.org/a-search-algorithm/

import heapq
import typing

from numpy import float16

from helpers import is_valid, is_unblocked, is_destination, calculate_h_value

# Define the Cell class


class Node:
    """
    Defines the node class.

    Attributes:
        parent_i:
          The x position of the parent node.
        parent_j:
          The y position of the parent node.
        f:
          The total cost from the start node to the goal node (g + h).
        g:
          The actual cost from the start node to the current node.
        h:
          The heuristic cost from the current node to the goal node
    """

    def __init__(self):
        """
        Initializes the Node class.
        """
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0


def trace_path(node_details: Node, goal: dict) -> list[tuple[int, int]]:
    """
    Traces the path from source to destination.

    Args:
      node_details:
        Information about the node.
      dest:
        The goal node.

    Returns:
      The full path from the start node to goal node.
    """
    print("The Path is \n")
    path = []
    row = goal["x"]
    col = goal["y"]

    # Trace the path from destination to source using parent cells
    while not (node_details[row][col].parent_i == row and node_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = node_details[row][col].parent_i
        temp_col = node_details[row][col].parent_j
        row = temp_row
        col = temp_col

        # Add the source node to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        # Print the path
        for i in path:
            print("->", i, end=" ")
        print("\n")

    return path


def a_star_search(game_state: typing.Dict, src: dict, dest: dict) -> list[tuple[int, int]] | None:
    """
    Implement the A* search algorithm.

    Args:
      game_state:
        Information about the state space of the game.
      src:
        The starting node position.
      dest:
        The goal node position.

    Returns:
      If a path is found, then the function will return a list containing the path to the goal node.
      If a path is not found, then return None.
    """
    # Obtain the game height and width
    board_height = game_state["board"]["height"]
    board_width = game_state["board"]["width"]

    # Get current game state information about self and other snakes
    snakes = game_state["board"]["snakes"]

    # Check if the destination is unblocked
    if not is_unblocked(snakes, dest["x"], dest["y"]):
        print("Destination is blocked \n")
        return None  # Exit and check path to next food

    # Check if we are already at the destination
    if is_destination(src["x"], src["y"], dest):
        print("We are already at the destination \n")
        return None  # Exit and check path to next food

    # Initialize the closed list (visited nodes)
    closed_list = [[False for _ in range(board_width)]
                   for _ in range(board_height)]
    # Initialize the details of each node
    node_details = [[Node() for _ in range(board_width)]
                    for _ in range(board_height)]

    # Initialize the start node details
    i = src["x"]
    j = src["y"]
    node_details[i][j].f = 0
    node_details[i][j].g = 0
    node_details[i][j].h = 0
    node_details[i][j].parent_i = i
    node_details[i][j].parent_j = j

    # Initialize the open list (node to be visited) with the start node
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the node with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the node as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        # Corresponds to UP, DOWN, RIGHT, LEFT
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(board_height, board_width, new_i, new_j) and is_unblocked(snakes, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    node_details[new_i][new_j].parent_i = i
                    node_details[new_i][new_j].parent_j = j
                    print("The destination cell is found \n")
                    # Trace and print the path from source to destination
                    path = trace_path(node_details, dest)
                    found_dest = True
                    return path
                else:
                    # Calculate the new f, g, and h values
                    g_new = node_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the node is not in the open list or the new f value is smaller
                    if node_details[new_i][new_j].f == float('inf') or node_details[new_i][new_j].f > f_new:
                        # Add the node to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the node details
                        node_details[new_i][new_j].f = f_new
                        node_details[new_i][new_j].g = g_new
                        node_details[new_i][new_j].h = h_new
                        node_details[new_i][new_j].parent_i = i
                        node_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all nodes
    if not found_dest:
        print("Failed to find the destination node \n")
        return None  # Exit and move to next food
