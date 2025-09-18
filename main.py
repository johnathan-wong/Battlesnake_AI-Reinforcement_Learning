# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#

'''
# This is a container for Battlesnake.
# To use this container, please import your own SnakeClass
# This is not the ORIGINAL SAMPLE CODE from https://docs.battlesnake.com/
'''

import random
import typing
from SnakeClasses.base_snake import MySnake
from SnakeClasses.AlgorithmSnake.algorithm_snake import AlgorithmSnake


DEBUG_MODE = True
game_instances: typing.Dict[str, typing.Dict[str, AlgorithmSnake]] = {}

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
    game_id = game_state['game']['id']
    my_id = game_state['you']['id']
    if game_id not in game_instances:
        game_instances[game_id] = {}
        print(f"GAME START \n Game {game_id} Have Been Initialized.")
    game_instances[game_id][my_id] = AlgorithmSnake(my_id)
    game_instances[game_id][my_id].start(game_state)
    print(f"Snake {my_id} Have Been Initialized.")
    


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    game_id = game_state['game']['id']
    my_id = game_state['you']['id']
    game_instances[game_id][my_id].end(game_state)
    print(f"GAME OVER\n Snake {my_id} Have Been Terminated.")
    del game_instances[game_id][my_id]
    if len(game_instances[game_id]) == 0:
        del game_instances[game_id]
        print(f"Game {game_id} Have Been Terminated.")



# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    game_id = game_state['game']['id']
    turn = game_state["turn"]
    my_id = game_state['you']['id']
    my_snake = game_instances[game_id][my_id]
    move = my_snake.move(game_state)
    if DEBUG_MODE:
        print(f"Snake-{my_id} Choose {move['move']} on step {turn}")
    return move



# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})