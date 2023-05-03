import numpy as np
from functionnalities import *
import sys, os

if __name__ == '__main__':
    # files_ap = "D:\\dronesProject\\files_ap\\map_simu2997.ap"  # path nader
    # files_ap = "C:\\Users\\Cancrelesh\\Documents\\ssio_courses\\dronesProject\\files_ap\\" #path windows julien
    # files_ap = "files_ap/" #path linux thomas

    base_ap_dir = "files_ap"

    argv = sys.argv
    if len(argv) != 2:
        print("Usage: python q_learning.py <map_name>")
        exit(1)

    env = parser(os.path.join(base_ap_dir, argv[1])) # Change name of the map here
    st = env.reset()

    Q = []
    listeRewardsBatteryEpisode = []
    totalReward = 0
    done = 0
    j = 0

    for _ in range(len(env.targets_pos)+1):
        Q.append(np.zeros((env.NB_STATES, env.NB_ACTIONS)))
        for i in range(1000):

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

    writeActionsToPythonScript(action_list, "./gen_files/q_learning_action.py", env.map_real_dims, env.map_simu_dims)

