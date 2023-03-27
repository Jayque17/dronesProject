import numpy as np
from random import randint, uniform
from .managerEnv import ManagerEnv

def take_action(st, Q, eps, nb_actions):
    # Take an action
    if uniform(0, 1) < eps:
        action = randint(0, nb_actions-1)
    else: # Or greedy action
        action = np.argmax(Q[st])
    return action


if __name__ == '__main__':
    env = ManagerEnv()
    st = env.reset()

    Q = [[0]*env.NB_ACTIONS]*env.NB_ACTIONS