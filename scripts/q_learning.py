from time import sleep
import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
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

def getInfoRewardAndBattery(listeRewardsBatteryEpisode, droneBatterry, totalReward, episode):
    listeRewardsBatteryEpisode.append((episode, droneBatterry, totalReward))

def plot(listeRewardsBatteryEpisode):
    episode = []
    droneBatterry = []
    totalReward = []
    for i in range(len(listeRewardsBatteryEpisode)):
        episode.append(listeRewardsBatteryEpisode[i][0])
        droneBatterry.append(listeRewardsBatteryEpisode[i][1])
        # print('reward',listeRewardsBatteryEpisode[i][2])
        totalReward.append(listeRewardsBatteryEpisode[i][2])
    
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig.suptitle('Rewards and Battery level by episodes')
    # ax1.plot(episode, droneBatterry)
    # ax2.plot(episode, totalReward)
    # fig.show()

    plt.subplot(2, 1, 1)
    plt.plot(episode, droneBatterry)

    plt.subplot(2, 1, 2)
    plt.plot(episode, totalReward)

    plt.show()




if __name__ == '__main__':
    # files_ap = "D:\dronesProject\\files_ap\\map_simu2997.ap" #path nader
    # files_ap = "C:\\Users\\Cancrelesh\\Documents\\ssio_courses\\dronesProject\\files_ap\\" #path windows julien
    files_ap = "files_ap/" #path linux thomas
    env = parser(files_ap + "test3.ap")
    st = env.reset()

    Q = np.zeros((env.NB_STATES, env.NB_ACTIONS))
    # displayQTable(Q)

    listeRewardsBatteryEpisode = []
    totalReward = 0
    
    for i in range(1000):

        st = env.reset()
        done = False

        while not done:
            # Take an action
            action = take_action(st, Q, 0.6, env.NB_ACTIONS)
            stp1, reward, done, _ = env.step(action)

            # print("_________________________________________________________"*3)
            # print(i, st, reward, done)
            # env.render(Q)

            # Update Q
            action1 = take_action(stp1, Q, 0., env.NB_ACTIONS)
            #displayQTable(Q)

            value = Q[st][action] + 0.01*(reward + 0.9*Q[stp1][action1] - Q[st][action])
            Q[st][action] = value

            st = stp1
            # print("st", st)
            # print("action", action)
            # print("value", value)
            #displayQTable(Q)

            totalReward += reward
            # print('total', totalReward)
            if done:
                getInfoRewardAndBattery(listeRewardsBatteryEpisode, env.drones[0].battery, totalReward, i+1)
                totalReward = 0

    displayQTable(Q)
    plot(listeRewardsBatteryEpisode)

    
    # 52 6
    # check if qlearning really work
    total = 0 
    done = False
    st = env.reset()
    while not done:
        best_action = np.argmax(Q[st])
        print("action", best_action)
        for d in env.drones:
            print("drone pos", d.pos)

        stp1, reward, done, _ = env.step(best_action)
        Q[st][best_action] = - Q[st][best_action]
        print(stp1, reward, done)
        total += reward
        st = stp1
        env.render(Q)
    print(total)


