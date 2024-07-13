import env as Lake
from stable_baselines3 import PPO
import numpy as np
from stable_baselines3.common.env_util import make_vec_env


env = make_vec_env(Lake.Lake, n_envs=4)
# Create the environment

#env.reset()
# Create the PPO agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=10000)

# Save the trained model
model.save("ppo_lake")

# Load the trained model
# model = PPO.load("ppo_cartpole")
def evaluate_policy(model, env, n_eval_episodes=10):
    episode_rewards = []
    for _ in range(n_eval_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _ = env.step(action)
            episode_reward += reward
        episode_rewards.append(episode_reward)
    mean_reward = sum(episode_rewards) / n_eval_episodes
    std_reward = np.std(episode_rewards)
    return mean_reward, std_reward

# Evaluate the agent
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
