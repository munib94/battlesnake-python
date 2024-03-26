import typing


def is_valid(grid_height: int, grid_width:int , row: int, col: int) -> bool:
    """
    Checks if a cell is valid (within the grid)

    Args:
      grid_height:
        Number of rows in the grid.
      grid_width:
        Number of columns in the grid.
      row:
        The x position of the cell to validate.
      col:
        The y position of the cell to validate.
		
    Returns:
      A boolean indicating whether the cell is within the grid bounds.
    """
    return (0 <= row < grid_width) and (0 <= col < grid_height)


def is_unblocked(obstacles: list, row: int, col: int):
    """
    Checks if a cell is unblocked by avoiding collision with self and collision with other snakes.

    Args:
      game_state:
        Information about the state space of the game.
      row:
        The x position of the cell to check.
      col:
        The y position of the cell to check.

    Returns:
      A boolean result that checks whether the grid cell is not occupied.
    """
    
    # Put cell to check in same format as game state
    coords = {"x": row, "y": col}

    # Avoid collision with self and other snakes
    for snake in obstacles:
        snake_body = snake['body'][:-1]  # Exclude the tail since it moves
        if coords in snake_body:
            return False
    return True


def is_destination(row: int, col: int, goal: dict) -> bool:
    """
    Check if current node is the goal node

    Args:
      row:
        The x position of the node to validate.
      col:
        The y position of the node to validate.
	  goal:
	    The position of the goal node.
		
    Returns:
      A boolean indicating whether the current node is the goal node.
    """
    return row == goal["x"] and col == goal["y"]


def calculate_h_value(row: int, col: int, goal: dict) -> int:
    """
    Calculate the heuristic distance of current node to the goal node (Manhattan distance to destination)
	
	Args:
      row:
        The x position of the node.
      col:
        The y position of the node.
	  goal:
	    The position of the goal node.
		
    Returns:
	  The Manhattan distance from the current node to the goal node.
    """
    return (abs(row - goal["x"]) + abs(col - goal["y"]))

def manhattan_distance(point_1: dict, point_2: dict) -> int:
    """
    Helper function to calculate the Manhattan distance between two points.

    Args:
      point_1:
        The position of the first point.
      point_2:
        The position of the second point.

    Returns:
      Manhattan distance.
    """
    return abs(point_1['x'] - point_2['x']) + abs(point_1['y'] - point_2['y'])


def is_point_on_board(point: dict, width: int, height: int) -> bool:
    """
    Helper function to check if a point is on the board.

    Args:
      point:
        The position of the point to validate.
      width:
        Number of columns on the board.
      height:
        Number of rows on the board.

    Returns:
      True if the point is within the boundaries of the board.
    """
    return 0 <= point['x'] < width and 0 <= point['y'] < height


def is_terminal(game_state: typing.Dict) -> bool:
    """
    Determines if the game state is a terminal state (either because the game is over or a certain depth has been reached).

    Args:
      game_state:
        Information about the state space of the game.

    Returns:
      True if our snake health is zero.
    """
    # Check if our snake is still alive in the game state
    return game_state['you']['health'] == 0
