import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from Gym.environment import BattlesnakeEnv


# --- Callback to stop training after a set number of episodes ---
class TotalEpisodesCallback(BaseCallback):
    """
    Callback for stopping training after a certain number of episodes.
    """
    def __init__(self, total_episodes, verbose=0):
        super().__init__(verbose)
        self.total_episodes = total_episodes
        self.episode_count = 0

    def _on_step(self) -> bool:
        # Check if the episode is done
        if self.locals["dones"][0]:
            self.episode_count += 1
            if self.verbose > 0:
                print(f"Episode {self.episode_count}/{self.total_episodes} finished.")

        # Return a boolean value to indicate whether training should continue
        # We continue as long as the episode count is less than the total.
        return self.episode_count < self.total_episodes


# --- Config ---
height = 7
width = 7
total_episodes = 50_000 # Train for a specific number of games instead of steps

# --- Create environment ---
env = BattlesnakeEnv(width=width, height=height, num_snakes=2)
# Logs reward per episode. This wrapper is still useful for printing stats.
env = gym.wrappers.RecordEpisodeStatistics(env)

# --- Train model ---
model = PPO(
    policy="MultiInputPolicy",
    env=env,
    verbose=1,
    tensorboard_log="./logs"
)

# Initialize the callback
callback = TotalEpisodesCallback(total_episodes=total_episodes, verbose=1)

print(f"Starting training for {total_episodes} games...")
model.learn(total_timesteps=1e9, callback=callback)
print("Training done!")

# --- Save model ---
save_path = "snake_rl_model"
model.save(save_path)
print(f"Model saved to {save_path}")