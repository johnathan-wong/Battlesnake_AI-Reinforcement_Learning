import gymnasium as gym
from gymnasium import spaces
import numpy as np
from .engine import BattlesnakeEngine
from SnakeClasses.AlgorithmSnake.algorithm_snake import AlgorithmSnake

class BattlesnakeEnv(gym.Env):
    def __init__(self, width = 11, height = 11, num_snakes = 2):
        self.action_map = {
            0: "up",
            1: "down",
            2: "left",
            3: "right"
        }
        self.width = width
        self.height = height
        self.num_snakes = num_snakes
        self.snakes = [AlgorithmSnake(id) for id in range(1, num_snakes)]
        self.engine = BattlesnakeEngine(width, height, num_snakes)
        # Action Spaces: 4 (Left, Right, Up, Down)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict({
            "grid": spaces.Box(low=0, high=1, shape=(6, self.height, self.width), dtype=np.float32),
            # [You, E1, E2, E3]
            "stats": spaces.Box(low=0, high=1, shape=(17,), dtype=np.float32)  
            # [health, length, E1health, E1dx, E1dy, ... , Fdx, Fdy]
        })

    def reset(self, *, seed = None, options = None):
        state = self.engine.reset(self.num_snakes)
        obs = self._extract_obs(state)
        return obs, state
    
    def step(self, action):
        
        actions = {0:self.action_map[action]}
        for snake in self.snakes:
            actions[snake.get_id()] = snake.move(self.engine._get_game_state())["move"]
        
        state = self.engine.step(actions)
        obs = self._extract_obs(state)
        # print(obs)
        # --- Print the shape here ---
        # print("--- Processed Observation Shapes ---")
        # for key, array in obs.items():
        #     print(f"Key '{key}': Shape {array.shape}, Dtype {array.dtype}")
        # print("------------------------------------")
        
        reward = self._compute_reward(state)
        done = self.engine.done
        # if done:
        #     print(done, self.engine.turn)

        return obs, reward, done, False, state
        
        
    def _extract_obs(self, game_state):
        grid = np.zeros((6, self.height, self.width), dtype=np.float32)
        stats = np.zeros(17, dtype=np.float32)
        
        # Extracting Grid
        snakes = game_state["board"]["snakes"]
        foods = game_state["board"]["food"]
        my_snake = next((snake for snake in snakes if snake["id"] == 0), None)
        
        for snake in snakes:
            # Head Pos
            pos  = snake["body"][0]
            grid[snake["id"], pos["y"], pos["x"]] = 1
            # Body Pos
            for pos in snake["body"][1:-1]:
                grid[4, pos["y"], pos["x"]] = 1
        
        for food_pos in foods:
            grid[5, food_pos["y"], food_pos["x"]] = 1
                    
        # Extracting Stats
        for snake in snakes:
            id = snake["id"]
            if id == 0:
                # My snakes Info
                stats[0] = snake["health"] / 100
                stats[1] = len(snake["body"]) / (self.height * self.width)
            else:
                # Opponents info (relative to my pos)
                if my_snake != None and snake != None:
                    delta = self._compute_delta(my_snake["body"][0], snake["body"][0])
                    stats[(id-1)*4+2] = snake["health"] / 100                           # Health
                    stats[(id-1)*4+3] = len(snake["body"]) / (self.height * self.width) # Length
                    stats[(id-1)*4+4] = delta["dx"] / self.width                        # Dx
                    stats[(id-1)*4+5] = delta["dy"] / self.height                       # Dy
        
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