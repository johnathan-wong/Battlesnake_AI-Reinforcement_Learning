from ..base_snake import MySnake
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class NNSnake(MySnake):
    def __init__(self, snake_id, model):
        super().__init__(snake_id)
        self.model = model

    def move(self, state):
        # convert state/obs to tensor
        obs = self._extract_obs(state)

        action, _ = self.model.predict(obs, deterministic=True)
        action = int(action)
        
        # translate NN action into Battlesnake move
        move = {0: "up", 1: "down", 2: "left", 3:"right"}[action]
        return {"move": move}

    def _extract_obs(self, game_state):
        width = game_state["board"]["width"]
        height = game_state["board"]["height"]
        grid = np.zeros((6, height, width), dtype=np.float32)
        stats = np.zeros(17, dtype=np.float32)
        
        # Extracting Grid
        snakes = game_state["board"]["snakes"]
        foods = game_state["board"]["food"]
        my_snake = next((snake for snake in snakes if snake["id"] == self.get_id()), None)
        opp_idx = 1
        for snake in snakes:
            # Head Pos
            pos  = snake["body"][0]
            if snake["id"] == my_snake["id"]:
                grid[0, pos["y"], pos["x"]] = 1
            else:
                grid[opp_idx, pos["y"], pos["x"]] = 1
                opp_idx += 1
            
            # Body Pos
            for pos in snake["body"][1:-1]:
                grid[4, pos["y"], pos["x"]] = 1
        
        for food_pos in foods:
            grid[5, food_pos["y"], food_pos["x"]] = 1
        
        opp_idx = 1
                 
        # Extracting Stats
        for snake in snakes:
            id = snake["id"]
            if id == my_snake["id"]:
                # My snakes Info
                stats[0] = snake["health"] / 100
                stats[1] = len(snake["body"]) / (height * width)
            else:
                # Opponents info (relative to my pos)
                if my_snake != None and snake != None:
                    delta = self._compute_delta(my_snake["body"][0], snake["body"][0])
                    stats[(opp_idx-1)*4+2] = snake["health"] / 100                           # Health
                    stats[(opp_idx-1)*4+3] = len(snake["body"]) / (height * width) # Length
                    stats[(opp_idx-1)*4+4] = delta["dx"] / width                        # Dx
                    stats[(opp_idx-1)*4+5] = delta["dy"] / height                       # Dy
                    opp_idx += 1
        return {"grid": grid, "stats": stats}
    
    def _compute_reward(self, state):
        snakes = state["board"]["snakes"]
        my_snake = next((snake for snake in snakes if snake["id"] == 0), None)
        reward = 0
        
        if my_snake:
            reward += 0.01
        else:
            reward -= 10
            return reward
            
        if my_snake["health"] == 100:
            reward += 0.5
            
        return reward
    
    def _compute_delta(self, target1, target2):
        if target1 == None or target2 == None:
            return {"dx": 0, "dy": 0}
        dx, dy = target1["x"] - target2["x"], target1["y"] - target2["y"]
        return {"dx": dx, "dy": dy}