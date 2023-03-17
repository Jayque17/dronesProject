import gym
from babyrobot import BabyRobotEnv_v1

if __name__ == "__main__":

        # create an instance of our custom environment
    env = BabyRobotEnv_v1()

    # use the Gymnasium 'check_env' function to check the environment
    # - returns nothing if the environment is verified as ok
    from gym.utils.env_checker import check_env
    check_env(env)

    print(f'Action Space: {env.action_space}')
    print(f'Action Space Sample: {env.action_space.sample()}')
          
    # env = gym.make('BabyRobotEnv-v2')

    # # initialize the environment
    # env.reset()
    # env.render()

    # terminated = False
    # while not terminated:  

    #     # choose a random action    
    #     action = env.action_space.sample()   

    #     # take the action and get the information from the environment
    #     new_state, reward, terminated, truncated, info = env.step(action)
        
    #     # show the current position and reward
    #     env.render(action=action, reward=reward) 


  


