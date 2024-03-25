import random
import typing
import copy
import numpy as np

# THis code is working well.


# Constants for heuristic evaluation
POSITIVE_INFINITY = float('inf')
NEGATIVE_INFINITY = -float('inf')


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
def info() -> typing.Dict:
    return {
        "apiversion": "1",
        "author": "Team 8",  # Your Battlesnake Username
        "color": "#888888",  # Choose color
        "head": "default",  # Choose head
        "tail": "default",  # Choose tail
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

# Determines if the game state is a terminal state (either because the game is over or a certain depth has been reached)
def is_terminal(game_state: typing.Dict) -> bool:
    # Check if our snake is still alive in the game state
    return game_state['you']['health'] == 0


# Returns a list of safe move directions that do not immediately lead to death
def get_safe_moves(game_state: typing.Dict) -> typing.List[str]:
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

    return safe_moves

# Applies a move to the game state and returns the new state
def apply_move(game_state: typing.Dict, move: str) -> typing.Dict:
    # Clone the game state to avoid mutating the original state
    new_state = copy.deepcopy(game_state)
    head = new_state['you']['body'][0]

    # Apply the move to the head position
    if move == 'up':
        head['y'] += 1
    elif move == 'down':
        head['y'] -= 1
    elif move == 'left':
        head['x'] -= 1
    elif move == 'right':
        head['x'] += 1

    # Add the new head position to the front of the snake's body
    new_state['you']['body'].insert(0, head)

    # Remove the tail position to simulate the snake moving forward
    new_state['you']['body'].pop()

    # Return the new game state after the move
    return new_state

# Helper function to calculate the Manhattan distance between two points
def manhattan_distance(a, b):
    return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])

# Helper function to check if a point is on the board
def is_point_on_board(point, width, height):
    return 0 <= point['x'] < width and 0 <= point['y'] < height

# Helper function to estimate the area of the board controlled by our snake
def calculate_area_control(game_state, head):
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    # Create a grid to represent the board
    board_grid = np.zeros((board_width, board_height), dtype=int)
    
    # Mark the position of all snakes' bodies on the board
    for snake in game_state['board']['snakes']:
        for segment in snake['body']:
            # Ensure the body segment is on the board
            if is_point_on_board(segment, board_width, board_height):
                # Mark the segment as occupied
                board_grid[segment['x']][segment['y']] = 1

    # Perform a flood fill algorithm starting from our snake's head position
    # to determine the size of the area controlled
    area = 0
    queue = [head]
    directions = [{'x': 0, 'y': 1}, {'x': 1, 'y': 0}, {'x': 0, 'y': -1}, {'x': -1, 'y': 0}]
    while queue:
        current = queue.pop(0)
        for direction in directions:
            neighbor = {'x': current['x'] + direction['x'], 'y': current['y'] + direction['y']}
            if is_point_on_board(neighbor, board_width, board_height) and board_grid[neighbor['x']][neighbor['y']] == 0:
                board_grid[neighbor['x']][neighbor['y']] = 1  # Mark as visited
                area += 1
                queue.append(neighbor)
    return area

# The heuristic function
def heuristic(game_state: typing.Dict) -> float:
    my_snake = game_state['you']
    my_health = my_snake['health']
    my_head = my_snake['body'][0]
    my_length = len(my_snake['body'])
    
    # Initialize the score with the health ratio and length of our snake
    score = (my_health / 100.0) + my_length

    # Integrate the area control score into the heuristic
    area_control_score = calculate_area_control(game_state, my_head)
    score += area_control_score / 10.0  # Add the area control score to the heuristic with a weight
    
    # Penalize the proximity to other snakes (potential danger)
    for snake in game_state['board']['snakes']:
        if snake['id'] != my_snake['id']:
            distance_to_snake = manhattan_distance(my_head, snake['body'][0])
            # The closer the other snake's head, the higher the penalty
            score -= max(10 - distance_to_snake, 0) / 10.0

    # Encourage getting closer to food if health is below a certain threshold
    if my_health < 50 and game_state['board']['food']:
        closest_food_distance = min(manhattan_distance(my_head, food) for food in game_state['board']['food'])
        # The closer the food, the higher the score, especially when health is low
        score += 10 / (closest_food_distance + 1)

    return score



def minimax(game_state: typing.Dict, depth: int, maximizingPlayer: bool) -> typing.Tuple[float, str]:
    # Base case: if we've reached the maximum depth or the game is over, evaluate the game state
    if depth == 0 or is_terminal(game_state):
        return heuristic(game_state), None
    if maximizingPlayer:
        # Initialize the best value to the lowest possible number
        value = NEGATIVE_INFINITY
        # Initialize the best move to None
        best_move = None
        # Explore all possible safe moves for the maximizing player 
        for move_option in get_safe_moves(game_state):
            # Apply the move to get a new game state
            new_state = apply_move(game_state, move_option)
            # Recursively call minimax for the new state, decreasing the depth
            new_value, _ = minimax(new_state, depth-1, False)
            # Update the best value - maximum and move if the new value is better
            if new_value > value:
                value, best_move = new_value, move_option
        
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
            new_value, _ = minimax(new_state, depth-1, True)
            # Update the best value - minimum and move if the new valued is better for the minimizing player
            if new_value < value:
                value, best_move = new_value, move_option
            
        # Return the best value and move found for the minimizing player
        return value, best_move


def move(game_state: typing.Dict) -> typing.Dict:
    # Replace the original random move selection with minimax algorithm
    _, next_move = minimax(game_state, depth=3, maximizingPlayer=True)  # adjust the depth accordingly
    print(next_move)
    return {"move": next_move or "down"}  # Fallback to "down" if no move is found


if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
