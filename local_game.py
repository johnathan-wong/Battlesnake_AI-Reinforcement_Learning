from stable_baselines3 import PPO
from Gym.environment import BattlesnakeEnv
from Gym.engine import BattlesnakeEngine
from SnakeClasses.AlgorithmSnake.algorithm_snake import AlgorithmSnake
from SnakeClasses.AISnake.snake_nn import NNSnake

width = 7
height = 7

env = BattlesnakeEnv(width=width, height=height, num_snakes=2)
save_path = "snake_rl_model"
model = PPO.load(save_path, env=env)
model.policy.eval()

snakes = [AlgorithmSnake(0), NNSnake(1, model)]



engine = BattlesnakeEngine(width, height, len(snakes))
for i in range(10):
    engine.reset(2)
    done = False
    while not done:
        state = engine._get_game_state()
        actions = {}
        for snake in snakes:
            actions[snake.get_id()] = snake.move(state)["move"]
        state = engine.step(actions)
        done = engine.done
