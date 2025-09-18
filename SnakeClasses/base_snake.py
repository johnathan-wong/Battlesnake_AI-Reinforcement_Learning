import collections
import typing
import random

class MySnake:
    """
    This is the Base of all Snake for BattleSnake
    """
    
    def __init__(self, id):
        self.id = id
        pass
    
    def start(self, game_state: typing.Dict):
        game_id = game_state['game']['id']
        print(f"A New Game Have Started. \n Game ID - {game_id}")
        
    def end(self, game_state: typing.Dict):
        game_id = game_state['game']['id']
        print(f"A Game Have Ended. \n Game ID - {game_id}")
        
    def move(self, game_state: typing.Dict) -> typing.Dict:
        is_move_safe = {"up": True, "down": True, "left": True, "right": True}

        # We've included code to prevent your Battlesnake from moving backwards
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

        if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
            is_move_safe["left"] = False

        elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
            is_move_safe["right"] = False

        elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
            is_move_safe["down"] = False

        elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
            is_move_safe["up"] = False

        # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
        # board_width = game_state['board']['width']
        # board_height = game_state['board']['height']

        # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
        # my_body = game_state['you']['body']

        # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
        # opponents = game_state['board']['snakes']

        # Are there any safe moves left?
        safe_moves = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)

        if len(safe_moves) == 0:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            return {"move": "down"}

        # Choose a random move from the safe ones
        next_move = random.choice(safe_moves)

        # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
        # food = game_state['board']['food']

        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}
        print("A Move Have decided.")
        
    def get_id(self):
        return self.id