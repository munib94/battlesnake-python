import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
def info() -> typing.Dict:
    return {
        "apiversion": "1",
        "author": "",  # Your Battlesnake Username
        "color": "#888888",  # Choose color
        "head": "default",  # Choose head
        "tail": "default",  # Choose tail
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_body = game_state['you']['body']
    food = game_state['board']['food']

    # Initialize movement options
    possible_moves = {
        "up": {"x": my_head["x"], "y": my_head["y"] + 1},
        "down": {"x": my_head["x"], "y": my_head["y"] - 1},
        "left": {"x": my_head["x"] - 1, "y": my_head["y"]},
        "right": {"x": my_head["x"] + 1, "y": my_head["y"]},
    }

    # Avoid walls
    safe_moves = {move: coords for move, coords in possible_moves.items() if 0 <= coords['x'] < board_width and 0 <= coords['y'] < board_height}

    # Avoid self-collision
    safe_moves = {move: coords for move, coords in safe_moves.items() if coords not in my_body}

    # Avoid other snakes
    for snake in game_state['board']['snakes']:
        if snake['id'] != game_state['you']['id']:
            snake_body = snake['body'][:-1]  # Exclude the tail since it moves
            safe_moves = {move: coords for move, coords in safe_moves.items() if coords not in snake_body}

    # Move towards food
    if food:
        food_distances = {move: min([abs(coords['x'] - f['x']) + abs(coords['y'] - f['y']) for f in food]) for move, coords in safe_moves.items()}
        next_move = min(food_distances, key=food_distances.get) if food_distances else "down"
    else:
        next_move = random.choice(list(safe_moves.keys())) if safe_moves else "down"

    print(f"MOVE: {next_move}")
    return {"move": next_move}

if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
