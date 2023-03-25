import tensorflow as tf
from gym.spaces.utils import flatten_space
from numpy.core.numeric import shape
from gym.wrappers import FlattenObservation
from qlearn import ActorCritic
# from stable_baselines.common.env_checker import check_env

tf.keras.optimizers.Adam._name = 'test'

from functionnalities import *



if __name__ == "__main__":

    files_ap = "C:\\Users\\Cancrelesh\\Documents\\ssio_courses\\projet_drones\\files_ap\\" #path windows julien
    # files_ap = "files_ap/" #path linux thomas
    mana_env = parser(files_ap + "test.ap")
    mana_env = FlattenObservation(mana_env)
    
    print(mana_env.observation_space)
    print(mana_env.observation_space.sample())

    # states = flatten_space(mana_env.observation_space).shape
    # states = mana_env.observation_space[0]
    
    actions = mana_env.action_space.n

    # print('states', states)
    print(actions)
    print("simu dims", mana_env.map_simu_dims)
    print("real dims", mana_env.map_real_dims)
    print('observ_space', mana_env.observation_space)
    print('observ_space', mana_env.observation_space.shape)

    # check_env(mana_env)

    # model = build_veryenv(actions, mana_env)
    # model.summary()

    # dqn = build_agent(model, actions)
    # dqn.compile(tf.keras.optimizers.Adam(learning_rate=1e-3), metrics=['mae'])
    # print("ÇA A COMPILÉÉÉÉÉÉÉÉ")
    # print(mana_env)
    # dqn.fit(mana_env, nb_steps=50000, visualize=False, verbose=1)

    
    # done = False
    # state = mana_env.reset()
    # total = 0
    # print(mana_env.mapping_actions)
    # while not done:
    #     action = mana_env.action_space.sample()
    #     print("actions", mana_env.action_space)
    #     print("action", action, mana_env.mapping_actions[action])
    #     print("drone pos", mana_env.drones[0].pos)
    #     state, reward, done,_, _ = mana_env.step(action)
    #     print(state, reward, done)
    #     total += reward
    #     print("total", total, "\n")
    #     mana_env.render()

    
    num_epochs = 10
    batch_size = 64
    learning_rate = 0.00025

    # Initialize actor-critic model and optimizer
    model = ActorCritic(mana_env.observation_space.shape[0], mana_env.action_space.n)
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    # Run main training loop
    for epoch in range(num_epochs):
        # Initialize batch storage
        batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones = [], [], [], [], []
        batch_actor_logits_old, batch_critic_values_old = [], []

        # Collect batch of experiences
        for i in range(batch_size):
            state = mana_env.reset()
            done = False
            total_reward = 0

            while not done:
                # Collect experience
                actor_logits_old, critic_value_old = model(tf.convert_to_tensor(state[None, :], dtype=tf.float32))
                action = np.random.choice(mana_env.action_space.n, p=tf.nn.softmax(actor_logits_old)[0])
                next_state, reward, done, _ = mana_env.step(action)
                actor_logits_new, critic_value_new = model(tf.convert_to_tensor(next_state[None, :], dtype=tf.float32))

                # Append experience to batch storage
                batch_states.append(state)
                batch_actions.append(action)
                batch_rewards.append(reward)
                batch_next_states.append(next_state)
                batch_dones.append(done)
                batch_actor_logits_old.append(actor_logits_old)
                batch_critic_values_old.append(critic_value_old)

                # Update state
                state = next_state
                total_reward += reward

            # Print episode results
            print(f"Epoch {epoch+1}, Episode {i+1}, Reward: {total_reward}")

