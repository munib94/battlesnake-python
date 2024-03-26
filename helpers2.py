import typing

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
