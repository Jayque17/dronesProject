from time import sleep
import numpy as np
from random import randint, uniform
import managerEnv
from functionnalities import *

def take_action(st, Q, eps, nb_actions):
    # Take an action
    if uniform(0, 1) < eps:
        action = randint(0, nb_actions-1)
    else: # Or greedy action
        action = np.argmax(Q[st])
    return action

def displayQTable(Q):
    for i, e in enumerate(Q):
        print(i, e)


if __name__ == '__main__':
    files_ap = "files_ap/" #path linux thomas
    env = parser(files_ap + "test.ap")
    st = env.reset()
    Q = [[0]*env.NB_ACTIONS]*env.NB_STATES

    for i in range(1_000):

        st = env.reset()
        done = False

        while not done:
            # Take an action
            action = take_action(st, Q, 0.8, env.NB_ACTIONS)
            stp1, reward, done, _ = env.step(action)

            print(i, st, reward, done)
            #env.render()
            # Update Q
            action1 = take_action(stp1, Q, 0., env.NB_ACTIONS)
            Q[st][action] = Q[st][action] + 0.01*(reward + 0.9*Q[stp1][action1] - Q[st][action])

            st = stp1
    
    displayQTable(Q)

    
    # 52 6
    # check if qlearning really work
    # total = 0 
    # st = env.reset()
    # while not done:
    #     best_action = np.argmax(Q[st])
    #     print("action", best_action)
    #     print("drone pos", env.drones[0].pos)
    #     stp1, reward, done, _ = env.step(best_action)
    #     print(stp1, reward, done)
    #     total += reward
    #     st = stp1
    #     env.render()
    # print(total)

