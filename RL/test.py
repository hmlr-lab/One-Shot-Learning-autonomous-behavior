import gymnasium as gym
import env as Lake
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
#from stable_baselines3 import DQN

env = Lake.Lake(render_mode = "human")
env = make_vec_env(lambda: env, n_envs=1)
env.render_mode = "human"

#model = DQN("MlpPolicy", env, verbose=1)
#model = PPO(ActorCriticPolicy, env, verbose=1)
#model.learn(total_timesteps=5000)
#model.save("ppo_lake_3")

model = PPO.load("ppo_lake_3")

obs = env.reset()
moves={"up":0,"down":1,"left":2,"right":3,"upright":4,"downright":5,"upleft":6,"downleft":7}
for i in range(30000):
    action, _state = model.predict(obs)
    
    obs, reward, done, info = env.step(action)
    print(obs)
    print(reward)
    env.render("human")
    # VecEnv resets automatically
    if done:
       print(i)
       break
    #   obs = vec_env.reset()
#check how reward value should calculate
#def  act(action):
#    return obs, rewards,