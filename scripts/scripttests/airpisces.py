
from functionnalities import *

if __name__ == "__main__":

    files_ap = "C:\\Users\\Cancrelesh\\Documents\\ssio_courses\\projet_drones\\files_ap\\" #path windows julien
    # files_ap = "files_ap/" #path linux thomas
    mana_env = parser(files_ap + "test.ap")
    
    done = False
    state = mana_env.reset()
    total = 0
    print(mana_env.mapping_actions)
    while not done:
        action = mana_env.action_space.sample()
        print("actions", mana_env.action_space)
        print("action", action, mana_env.mapping_actions[action])
        print("drone pos", mana_env.drones[0].pos)
        state, reward, done,_, _ = mana_env.step(action)
        print(state, reward, done)
        total += reward
        print("total", total, "\n")
        mana_env.render()

    
   