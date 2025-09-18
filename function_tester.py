import os
import gymnasium as gym
from stable_baselines3 import PPO
from Gym.environment import BattlesnakeEnv


# --- Config ---
height = 7
width = 7
total_timesteps = 1_000_000   # adjust later (start small for testing)

# --- Create environment ---
env = BattlesnakeEnv(width=width, height=height, num_snakes=2)
env = gym.wrappers.RecordEpisodeStatistics(env)  # logs reward per episode

# --- Train model ---
model = PPO(
    policy="MultiInputPolicy",      # you can swap with CNN or custom later
    env=env,
    verbose=1,
    tensorboard_log="./logs"  # optional: monitor in TensorBoard
)

print("Starting training...")
model.learn(total_timesteps=total_timesteps)
print("Training done!")

# --- Save model ---
save_path = "snake_rl_model"
model.save(save_path)
print(f"Model saved to {save_path}")

# --- Load model later (for inference/testing) ---
# model = PPO.load(save_path, env=env)

# --- Test the trained snake ---
obs, _ = env.reset()
done, truncated = False, False

while not (done or truncated):
    action, _ = model.predict(obs, deterministic=True)
    action = int(action)
    obs, reward, done, truncated, info = env.step(action)
    # env.render()   # make sure you implemented .render() in BattlesnakeEnv
