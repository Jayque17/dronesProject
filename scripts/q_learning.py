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
    Q = [[0]*env.NB_ACTIONS]*env.NB_STATES

    for _ in range(100):
        # Take an action
        action = take_action(st, Q, 0.3, env.NB_ACTIONS)
        stp1, reward, done, _ = env.step(action)

        print(st, reward, done)
        env.render()
        
        # Update Q
        action1 = take_action(stp1, Q, 0., env.NB_ACTIONS)
        Q[st][action] = Q[st][action] + 0.1*(reward + 0.9*Q[stp1][action1] - Q[st][action])

        st = stp1
        
        if done:
            st = env.reset()

    for i, e in enumerate(Q):
        print(i, e)
        