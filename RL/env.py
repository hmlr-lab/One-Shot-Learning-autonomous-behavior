import numpy as np 

import matplotlib.pyplot as plt

from gym import Env, spaces

import testData.occ_grid_1c as map

#import map

plt.ion()
class Lake(Env):
    def __init__(self, render_mode="rgb_array"):
        super(Lake, self).__init__()
        
        self.render_mode = render_mode
        # Define a 2-D observation space
        self.observation_shape = map.map.shape
        self.observation_space = spaces.Box(low =0,# np.zeros(self.observation_shape), 
                                            high =1,# np.ones(self.observation_shape),
                                            shape = self.observation_shape,
                                            dtype = np.float32)
    
        #self.observation_space = spaces.Discrete(np.prod(self.observation_shape))
        # Define an action space ranging from 0 to 8
        self.action_space = spaces.Discrete(8,)
                        
        # Create a canvas to render the environment images upon 
        self.canvas = map.map
        
        self.goal = Point()
        self.goal.set_position(0,0)
        # Maximum steps boat can take at once
        self.max_step = 500

        Xs = np.where(self.canvas==0)[1]
        Ys = np.where(self.canvas==0)[0]
        self.lake =[]
        for i in range(len(Xs)):
            self.lake.append([Xs[i],Ys[i]])

        self.lake =np.array(self.lake)

        # Intialise the goal
        
        self.reset()


    def draw_elements_on_canvas(self):
        # Init the canvas 
        self.canvas = map.map.copy()
        # Draw the boat on canvas
        x,y = self.boat.x, self.boat.y
        self.canvas[y][x] = self.boat.icon

        xg,yg = self.goal.x, self.goal.y
        self.canvas[yg][xg] = 0.5

        #text = 'Fuel Left: {} | Rewards: {}'.format(self.step_left, self.ep_return)


    def reset(self):
        # Reset the fuel consumed
        self.step_left = 0

        # Reset the reward
        self.ep_return  = 0

        # Number of birds
        self.bird_count = 0
        self.fuel_count = 0

        # Determine a place to intialise the boat in
        self.boat = Boat()
        #i = np.random.choice(range(len(self.lake)))
        #y = self.lake[i][1]
        #x = self.lake[i][0]
        self.boat.set_position(58,192)

        self.goal = Point()
        #ig = np.random.choice(range(len(self.lake)))
        #xg = self.lake[ig][0]
        #yg = self.lake[ig][1]
        self.goal.set_position(210,100)
        self.last_distance = 250

        # Reset the Canvas 
        self.canvas = map.map
        # return the observation
        return self.canvas 
    
    def get_action_meanings(self):
        return {0: "Right", 1: "Left", 2: "Down", 3: "Up",4:"UpRight",5:"DownRight",6:"DownLeft",7:"UpLeft"}
    
    def has_collided(self, elem1):
  
        elem1_x, elem1_y = elem1.get_position()
        if np.where((self.lake[:,0]==elem1_x) & (self.lake[:,1]==elem1_y))[0].__len__()==0:
            return True

        return False

    def step(self, action):
        # Flag that marks the termination of an episode
        done = False
        
        # Assert that it is a valid action 
        assert self.action_space.contains(action), "Invalid Action"

        # Decrease the fuel counter 
        self.step_left += 1 

        self.boat.last_pos = self.boat.get_position()
        # apply the action to the boat
        if action == 0:#right
            self.boat.move(10,0)
        elif action == 1:#left
            self.boat.move(-10,0)
        elif action == 2:#down
            self.boat.move(0,10)
        elif action == 3:#up
            self.boat.move(0,-10)
        elif action == 4:#UpRight
            self.boat.move(10,10)
        elif action == 5:#DownRight
            self.boat.move(10,-10)
        elif action == 6:#DownLeft
            self.boat.move(-10,-10)
        elif action == 7:#UpLeft
            self.boat.move(-10,10)

        dist =np.linalg.norm(np.array(self.boat.get_position()) - np.array(self.goal.get_position()))  
        if self.has_collided(self.boat):
                reward = -1
                self.boat.set_position(self.boat.last_pos[0],self.boat.last_pos[1])

        elif dist <= 10.0:
                reward = 10.0
                done=True
        else:
            if self.last_distance > dist:
                reward =1 
            else:
                reward = 0
            
        self.last_distance = dist
        # Increment the episodic return
        self.ep_return += 1

        # If out of step, end the episode.
        if self.step_left == self.max_step:
            done = True

        if not done:
            # Draw elements on the canvas
            self.draw_elements_on_canvas()

        return self.canvas, reward, done, {}
    def render(self, mode = "human"):
        if mode == None: mode = 'human'
        #assert mode in ["human", "rgb_array"], "Invalid mode, must be either 'human' or 'rgb_array'"
        if mode == "human":
            plt.title("Steps:" + str(self.step_left))
            plt.imshow(self.canvas,cmap='gray')
            plt.pause(0.01)
            plt.clf()
        
        else :
            return self.canvas
        
    def seed(self, seed=None):
        np.random.seed(seed)

    def close(self):
        # Clean up resources
        pass
def close(self):
    plt.close()

class Point(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def get_position(self):
        return (self.x, self.y)
    
    def move(self, del_x, del_y):
        self.x += del_x
        self.y += del_y
       

class Boat(Point):
    def __init__(self):
        super(Boat, self).__init__()
        self.icon = 0.5
        self.icon_w = 1
        self.icon_h = 1
        self.last_pos = []
        
