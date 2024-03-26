import random
import typing
import sys

from minimax_search import minimax


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
def info() -> typing.Dict:
    return {
        "apiversion": "1",
        "author": "Team 8",  
        "color": "#888888",  # Choose color
        "head": "default",  # Choose head
        "tail": "default",  # Choose tail
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:
    # Replace the original random move selection with minimax algorithm
    _, next_move = minimax(game_state, depth=3)  # adjust the depth accordingly
    print(next_move)
    return {"move": next_move or "down"}  # Fallback to "down" if no move is found

if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
