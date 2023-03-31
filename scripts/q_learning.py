from time import sleep
import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
from functionnalities import *


def take_action(st, Q, eps, nb_actions):
    # Take an action
    if uniform(0, 1) < eps:
        action = randint(0, nb_actions - 1)
    else:  # Or greedy action
        action = np.argmax(Q[st])
    return action


def displayQTable(Q):
    for i, e in enumerate(Q):
        print(i, e)


def getInfoRewardAndBattery(listeRewardsBatteryEpisode, droneBatterry, totalReward, episode, numQtable):
    if len(listeRewardsBatteryEpisode) <= numQtable: 
        listeRewardsBatteryEpisode.append([(episode, droneBatterry, totalReward)])
    else:
        listeRewardsBatteryEpisode[numQtable].append((episode, droneBatterry, totalReward))

def dronePlot(listeRewardsBatteryEpisode):

    fig, ax = plt.subplots(2, len(listeRewardsBatteryEpisode))

    for i in range(len(listeRewardsBatteryEpisode)):
        ax[0, i].plot([x for x, _, _ in listeRewardsBatteryEpisode[i]], [x for _, x, _ in listeRewardsBatteryEpisode[i]] , 'tab:green')
        ax[1, i].plot([x for x, _, _ in listeRewardsBatteryEpisode[i]], [x for _, _, x in listeRewardsBatteryEpisode[i]] , 'tab:orange')

    plt.show()


if __name__ == '__main__':
    # files_ap = "D:\\dronesProject\\files_ap\\map_simu2997.ap"  # path nader
    # files_ap = "C:\\Users\\Cancrelesh\\Documents\\ssio_courses\\dronesProject\\files_ap\\" #path windows julien
    files_ap = "files_ap/" #path linux thomas
    env = parser(files_ap + "map_soutenance.ap")
    st = env.reset()

    Q = []
    listeRewardsBatteryEpisode = []
    totalReward = 0
    done = 0
    j = 0


    for _ in range(len(env.targets_pos)+1):
        Q.append(np.zeros((env.NB_STATES, env.NB_ACTIONS)))
        for i in range(500):

            st = env.reset(seed=j)
            done = 0

            while not done:
                # Take an action
                action = take_action(st, Q[j], 0.4, env.NB_ACTIONS)
                stp1, reward, done, _ = env.step(action)

                # Update Q
                action1 = take_action(stp1, Q[j], 0., env.NB_ACTIONS)
            
                value = Q[j][st][action] + 0.01 * (reward + 0.9 * Q[j][stp1][action1] - Q[j][st][action])
                Q[j][st][action] = value

                st = stp1
                totalReward += reward
                if not done:
                    getInfoRewardAndBattery(listeRewardsBatteryEpisode, env.drones[0].battery, totalReward, i + 1, j)
                    totalReward = 0

        st = env.reset(seed=j, options=True)
        j += 1
        done = 0

    print(len(Q))
    for i in range(len(Q)):
        displayQTable(Q[i])
    dronePlot(listeRewardsBatteryEpisode)

    total = 0
    done = 0
    st = env.reset()
    j = 0
    action_list = []
    for j in range(len(Q)):
        done = 0
        while not done:
            best_action = np.argmax(Q[j][st])
            action_list.append(best_action)
            print("action", best_action)
            for d in env.drones:
                print("drone pos", d.pos)
                print("drone battery", d.battery)

            stp1, reward, done, _ = env.step(best_action)
            print(j, stp1, reward, done)
            total += reward
            st = stp1
            env.render(Q[j])
    print(total)
    print(action_list)

    writeActionsToPythonScript(action_list, ".\\gen_files\\q_learning_actions.py", env.map_real_dims, env.map_simu_dims)

