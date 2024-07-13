import env as lakeEnv

env = lakeEnv.Lake()
obs = env.reset()
while True:
    # Take a random action
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    # Render the game
    print(reward)
    env.render(mode="human")
    if done == True:
        break

env.close()