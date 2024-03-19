# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import sys

from a_star import a_star_search, Node, trace_path


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # Get list of food nodes
    foods = game_state["board"]["food"]
    start = game_state["you"]["head"]

    possible_moves = []
    path_lengths = []
    # Perform A* search for all foods. This will return optimal paths to all foods.
    for food in foods:
        result = a_star_search(game_state, start, food)
        if result is not None:
            possible_moves.append(result)
            path_lengths.append(len(result))

    # Get shortest path from all possible paths and the corresponding next move
    # best_move = possible_moves[f_scores.index(best_f_score)]
    shortest_path = min(path_lengths)
    best_path = possible_moves[path_lengths.index(shortest_path)]
    best_move = best_path[1]
    row, col = best_move[0] - start["x"], best_move[1] - start["y"]
    if row == 1:
        next_move = "right"
    elif row == -1:
        next_move = "left"
    elif col == 1:
        next_move = "up"
    elif col == -1:
        next_move = "down"

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move or "down"}


# Start server when `python main.py` is run
if __name__ == "__main__":

    from server import run_server

    # Run on official server
    run_server({"info": info, "start": start, "move": move, "end": end})

    # Run on local server
    # port = "8000"
    # for i in range(len(sys.argv) - 1):
    #     if sys.argv[i] == '--port':
    #         port = sys.argv[i+1]

    # run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
