import typing
import copy

import numpy as np
from collections import deque

from helpers import manhattan_distance, is_point_on_board, is_terminal


# Constants for heuristic evaluation
POSITIVE_INFINITY = float('inf')
NEGATIVE_INFINITY = -float('inf')


def get_safe_moves(game_state: typing.Dict) -> typing.List[str]:
    """
    Gets a list of safe move directions that do not immediately lead to death.

    Args:
      game_state:
        Information about the state space of the game.

    Returns:
      A list of possible moves.
    """
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_head = game_state['you']['body'][0]  # Head of our snake
    my_body = game_state['you']['body']     # All body coordinates of our snake

    # Define the possible moves
    possible_moves = ['up', 'down', 'left', 'right']
    safe_moves = []

    # Check each possible move for safety
    for move in possible_moves:
        new_x, new_y = my_head['x'], my_head['y']
        if move == 'up':
            new_y += 1
        elif move == 'down':
            new_y -= 1
        elif move == 'left':
            new_x -= 1
        elif move == 'right':
            new_x += 1

        # Check if the move is within the boundaries of the board
        if 0 <= new_x < board_width and 0 <= new_y < board_height:
            # Check if the move doesn't collide with our snake's body
            if not any(part['x'] == new_x and part['y'] == new_y for part in my_body):
                safe_moves.append(move)

        # Prioritize food if health is low
        # if game_state['you']['health'] < 60:
        #     food_positions = game_state['board']['food']
        #     if food_positions:  # Check if there is food available
        #         food_directions = prioritize_food(my_head, food_positions, safe_moves)
        #         if food_directions:  # If there are safe moves leading to food, prioritize them
        #             return food_directions

    return safe_moves


# def prioritize_food(head: dict, food_positions: list, safe_moves: list, game_state: typing.Dict) -> list:
#     closest_food = min(food_positions, key=lambda food: manhattan_distance(head, food))
#     preferred_moves = []

#     # Consider the snake's current health
#     health = game_state['you']['health']

#     for move in safe_moves:
#         new_head = dict(head)  # Copy current head position
#         if move == 'up':
#             new_head['y'] -= 1
#         elif move == 'down':
#             new_head['y'] += 1
#         elif move == 'left':
#             new_head['x'] -= 1
#         elif move == 'right':
#             new_head['x'] += 1
        
#         # Prioritize moves that do not lead into dead-ends and are closer to food
#         if not is_dead_end(new_head, game_state) and manhattan_distance(new_head, closest_food) < manhattan_distance(head, closest_food):
#             preferred_moves.append(move)
    
#     # Return moves that head towards food and do not result in immediate dead-ends
#     return preferred_moves or safe_moves  # If no preferred moves, fallback to original safe moves


def is_dead_end(head: dict, game_state: typing.Dict) -> bool:
    """
    Simplified check for dead-ends. This could be replaced with a more complex flood-fill.
    For now, we just check if there are less than two safe moves from the new head position.

    Args:
      head:
        The head position of the snake.
      game_state:
        Information about the state space of the game.

    Returns:
      True if there is a dead-end.
    """
    # Simplified check for dead-ends. This could be replaced with a more complex flood-fill.
    # For now, we just check if there are less than two safe moves from the new head position
    safe_move_count = 0
    moves = [('up', 0, 1), ('down', 0, -1), ('left', -1, 0), ('right', 1, 0)]
    for move in moves:
        x, y = head['x'] + move[1], head['y'] + move[2]
        if 0 <= x < game_state['board']['width'] and 0 <= y < game_state['board']['height']:
            if not any(part['x'] == x and part['y'] == y for part in game_state['you']['body']):
                safe_move_count += 1
    return safe_move_count < 2  # Considered a dead-end if less than two safe moves


def apply_move(game_state: typing.Dict, move: str) -> typing.Dict:
    """
    Updates game state by simulating the effect of a move.

    Args:
      game_state:
        Information about the state space of the game.
      move:
        The direction to move in.

    Returns:
      The new game state after the move.
    """
    # Shallow copy the game state (deep copy is avoided for performance reasons)
    new_state = {
        'you': {
            'body': [{'x': game_state['you']['body'][0]['x'], 'y': game_state['you']['body'][0]['y']}] + game_state['you']['body'][:-1],
            'health': game_state['you']['health'],
            'id': game_state['you']['id']
        },
        'board': {
            'width': game_state['board']['width'],
            'height': game_state['board']['height'],
            'food': game_state['board']['food'],
            'snakes': game_state['board']['snakes']
        }
    }
    # Update the head position based on the move
    if move == 'up': new_state['you']['body'][0]['y'] += 1
    elif move == 'down': new_state['you']['body'][0]['y'] -= 1
    elif move == 'left': new_state['you']['body'][0]['x'] -= 1
    elif move == 'right': new_state['you']['body'][0]['x'] += 1

    return new_state


def calculate_area_control(game_state: typing.Dict, head: dict) -> int:
    """
    Estimates the area of the board controlled by our snake using a flood fill algorithm.

    Args:
      game_state:
        Information about the state space of the game.
      head:
        The head of the snake.

    Returns:
      Number of squares on the board controlled by our snake.
    """
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    board_grid = np.zeros((board_width, board_height), dtype=int)  # Initialize a grid to represent the board

    # Mark the position of all snakes on the board
    for snake in game_state['board']['snakes']:
        for segment in snake['body']:
            if is_point_on_board(segment, board_width, board_height):
                board_grid[segment['x']][segment['y']] = 1  # Mark the segment as occupied

    # Flood fill from our snake's head to determine the size of the area we control
    area = 0
    queue = deque([head])
    directions = [{'x': 0, 'y': 1}, {'x': 1, 'y': 0}, {'x': 0, 'y': -1}, {'x': -1, 'y': 0}]
    while queue:
        current = queue.popleft()
        for direction in directions:
            neighbor = {'x': current['x'] + direction['x'], 'y': current['y'] + direction['y']}
            if is_point_on_board(neighbor, board_width, board_height) and board_grid[neighbor['x']][neighbor['y']] == 0:
                board_grid[neighbor['x']][neighbor['y']] = 1  # Mark as visited
                area += 1
                queue.append(neighbor)
    return area


# The evaluation heuristic function
def evaluation_heuristic(game_state: typing.Dict) -> float:
    """
    Defines what is considered a winning score according to some heuristics.

    Args:
      game_state:
        Information about the state space of the game.

    Returns:
      A value calculated by some heuristics.
    """
    my_snake = game_state['you']
    my_health = my_snake['health']
    my_head = my_snake['body'][0]
    my_length = len(my_snake['body'])
    
    score = (my_health / 100.0) + my_length  # Base score from health and length
    area_control_score = calculate_area_control(game_state, my_head)
    score += area_control_score / 10.0  # Add area control score
    
    # Adjust score based on proximity to other snakes
    for snake in game_state['board']['snakes']:
        if snake['id'] != my_snake['id']:
            distance_to_snake = manhattan_distance(my_head, snake['body'][0])
            score -= max(10 - distance_to_snake, 0) / 10.0  # Penalize based on closeness to other snakes
    
    # If low on health, prioritize food more
    if my_health < 50 and game_state['board']['food']:
        closest_food_distance = min(manhattan_distance(my_head, food) for food in game_state['board']['food'])
        # score += 10 / (closest_food_distance + 1)  # Increase score based on proximity to food when health is low
        # Adjust scoring for health urgency
        if my_health < 15:  # Increase urgency
            score += 20 / (closest_food_distance + 1)  # Much more aggressive towards food when health is critically low
        elif my_health < 25:  # Increase urgency
            score += 15 / (closest_food_distance + 1)  # More aggressive towards food when health is critically low
        elif my_health < 50:
            score += 10 / (closest_food_distance + 1)  # Standard food prioritization

    return score


def minimax(game_state: typing.Dict, depth: int, alpha: float=NEGATIVE_INFINITY, beta: float=POSITIVE_INFINITY, maximizing_player: bool=True) -> typing.Tuple[float, str | None]:
    """
    An adversarial search algorithm that tries to maximize a score while assuming that an opposing agent is
    trying to minimize the score. Utilized alpha-beta pruning for efficiency.

    Args:
      game_state:
        Information about the state space of the game.
      depth:
        The depth of the search tree.
      maximizing_player:
        The player doing the maximizing.

    Returns:
      The best move and its associated value.
    """
    # Base case: if we've reached the maximum depth or the game is over, evaluate the game state
    if depth == 0 or is_terminal(game_state):
        return evaluation_heuristic(game_state), None
    if maximizing_player:
        # Initialize the best value to the lowest possible number
        value = NEGATIVE_INFINITY
        # Initialize the best move to None
        best_move = None
        # Explore all possible safe moves for the maximizing player 
        for move_option in get_safe_moves(game_state):
            # Apply the move to get a new game state
            new_state = apply_move(game_state, move_option)
            # Recursively call minimax for the new state, decreasing the depth
            new_value, _ = minimax(new_state, depth-1, alpha, beta, False)
            # Update the best value - maximum and move if the new value is better
            if new_value > value:
                value, best_move = new_value, move_option
            alpha = max(alpha, value)
            if alpha >= beta:
                break # Beta cutoff
        
        # Return the best value and move found for the maximizing player
        return value, best_move
    else:
        # Initialize the best value to the highest possible number
        value = POSITIVE_INFINITY
        # Initialize the best move to None
        best_move = None
        # Explore all possible safe moves for the minimizing player
        for move_option in get_safe_moves(game_state):
            # Apply the move to get a new game state
            new_state = apply_move(game_state, move_option)
            # Recursively call minimax for the new state, decreasing the depth
            new_value, _ = minimax(new_state, depth-1, alpha, beta, True)
            # Update the best value - minimum and move if the new valued is better for the minimizing player
            if new_value < value:
                value, best_move = new_value, move_option
            beta = min(beta, value)
            if beta <=alpha:
                break # Alpha cutoff
        
        # Return the best value and move found for the minimizing player
        return value, best_move
