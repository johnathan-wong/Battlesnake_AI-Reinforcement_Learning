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
import sys
from stable_baselines3 import PPO
from SnakeClasses.base_snake import MySnake
from SnakeClasses.AlgorithmSnake.algorithm_snake import AlgorithmSnake
from SnakeClasses.AISnake.snake_nn import NNSnake

SNAKE_CLASSES = {
    "AlgorithmSnake": AlgorithmSnake,
    "NNSnake": NNSnake,
    "MySnake": MySnake # Assuming MySnake is your base/default class
}


class BattlesnakeServer:
    def __init__(self, snake_class: type, model = None):
        self.snake_class = snake_class
        self.model = model
        self.game_instances: typing.Dict[str, typing.Dict[str, object]] = {}
        self.DEBUG_MODE = True
    

    # info is called when you create your Battlesnake on play.battlesnake.com
    # and controls your Battlesnake's appearance
    # TIP: If you open your Battlesnake URL in a browser you should see this data
    def info(self) -> typing.Dict:
        print("INFO")

        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#888888",  # TODO: Choose color
            "head": "default",  # TODO: Choose head
            "tail": "default",  # TODO: Choose tail
        }



    # start is called when your Battlesnake begins a game
    def start(self, game_state: typing.Dict):
        game_id = game_state['game']['id']
        my_id = game_state['you']['id']
        if game_id not in self.game_instances:
            self.game_instances[game_id] = {}
            print(f"GAME START \n Game {game_id} Have Been Initialized.")
            
        if self.snake_class.__name__ == "NNSnake":
            my_snake = self.snake_class(my_id, model=self.model)
        else:
            my_snake = self.snake_class(my_id)
        # my_snake = self.snake_class(my_id)
        self.game_instances[game_id][my_id] = my_snake
        my_snake.start(game_state)
        print(f"Snake {my_id} Have Been Initialized.")
        


    # end is called when your Battlesnake finishes a game
    def end(self, game_state: typing.Dict):
        game_id = game_state['game']['id']
        my_id = game_state['you']['id']
        self.game_instances[game_id][my_id].end(game_state)
        print(f"GAME OVER\n Snake {my_id} Have Been Terminated.")
        del self.game_instances[game_id][my_id]
        if len(self.game_instances[game_id]) == 0:
            del self.game_instances[game_id]
            print(f"Game {game_id} Have Been Terminated.")



    # move is called on every turn and returns your next move
    # Valid moves are "up", "down", "left", or "right"
    # See https://docs.battlesnake.com/api/example-move for available data
    def move(self, game_state: typing.Dict) -> typing.Dict:
        game_id = game_state['game']['id']
        turn = game_state["turn"]
        my_id = game_state['you']['id']
        my_snake = self.game_instances[game_id][my_id]
        move = my_snake.move(game_state)
        if self.DEBUG_MODE:
            print(f"Snake-{my_id} Choose {move['move']} on step {turn}")
        return move



# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    # Argv attrival
    if len(sys.argv) > 1:
        snake_class_name = sys.argv[1]
        snake_class_to_run = SNAKE_CLASSES.get(snake_class_name)
        if not snake_class_to_run:
            print(f"Error: Unknown snake class '{snake_class_name}'.")
            print("Available classes are:", list(SNAKE_CLASSES.keys()))
            sys.exit(1)
    else:
        # Default to AlgorithmSnake if no argument is provided.
        print("Running with default Snake Class - AlgorithmSnake")
        snake_class_to_run = AlgorithmSnake
        
    if len(sys.argv)>2:
        try:
            port_arg = int(sys.argv[2])
        except ValueError:
            print("Warning: Port must be an integer. Using default port 3000.")
            port_arg = 3000
    else: 
        # Default port if no argument is provided.
        print("Running with default Port - 3000")
        port_arg = 3000
     
    # Load the model only if the selected snake is the NNSnake.
    # This prevents loading a large file unnecessarily.
    model_to_pass = None
    if snake_class_to_run == NNSnake:
        save_path = "snake_rl_model"
        try:
            model_to_pass = PPO.load(save_path)
            model_to_pass.policy.eval() # Set the policy to evaluation mode
            print(f"Successfully loaded model from {save_path}")
        except FileNotFoundError:
            print(f"Error: Could not find trained model at {save_path}.")
            print("NNSnake requires a trained model to run.")
            sys.exit(1)

    # Launching Server 
    server_instance = BattlesnakeServer(snake_class_to_run, model=model_to_pass)
    
    run_server({
        "info": server_instance.info, 
        "start": server_instance.start, 
        "move": server_instance.move, 
        "end": server_instance.end,
        "port": port_arg
    })