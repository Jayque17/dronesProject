import tensorflow as tf
from gym.spaces.utils import flatten_space
from numpy.core.numeric import shape

tf.keras.optimizers.Adam._name = 'test'

from functionnalities import *



if __name__ == "__main__":

    files_ap = "C:\\Users\\Cancrelesh\\Documents\\ssio_courses\\projet_drones\\files_ap\\" #path windows julien
    mana_env = parser(files_ap + "test.ap")

    
    print(mana_env.observation_space)
    print(mana_env.observation_space.sample())

    states = flatten_space(mana_env.observation_space).shape
    actions = mana_env.action_space.n

    print(states)
    print(actions)
    print("simu dims", mana_env.map_simu_dims)
    print("real dims", mana_env.map_real_dims)
    print(mana_env.observation_space)

    # model = build_veryenv(states, actions, mana_env)
    # model.summary()

    # dqn = build_agent(model, actions)
    # dqn.compile(tf.keras.optimizers.Adam(learning_rate=1e-3), metrics=['mae'])
    # dqn.fit(mana_env, nb_steps=50000, visualize=False, verbose=1)

    done = False
    state = mana_env.reset()
    total = 0
    print(mana_env.mapping_actions)
    # while not done:
    action = mana_env.action_space.sample()
    print("actions", mana_env.action_space)
    print("action", action, mana_env.mapping_actions[action])
    print("drone pos", mana_env.drones[0].pos)
    # state, reward, done,_, _ = mana_env.step(action)
    # print(state, reward, done)
    # total += reward
    # print("total", total, "\n")
    mana_env.render()
    while True:
        pass



