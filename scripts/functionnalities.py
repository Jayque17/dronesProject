import gym 
import random
import numpy as np 
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.processors import MultiInputProcessor
from tensorflow import keras
from keras import Input
from keras.layers import concatenate
from managerEnv import ManagerEnv
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Embedding

def build_veryenv(states, actions, env):
    target = Dense(8, activation='relu')
    #target.add(Flatten(input_shape=(len(env.targets_pos),), name='targets'))
    target_input = Input(shape=(len(env.targets_pos[0]),), name='targets')
    target_encoded = target(target_input)

    # obstacles = Sequential()
    # obstacles.add(Flatten(input_shape=(len(env.obstacles_pos),), name='obstacles'))
    # obstacles_input = Input(shape=(len(env.obstacles_pos),), name='obstacles')
    # obstacles_encoded = obstacles(obstacles_input)


    drones = Dense(8, activation='relu')
    # drones.add(Flatten(input_shape=(len(env.drones),), name='drones'))
    # drones_input = Input(shape=(len(env.drone_pos),), name='drones')
    # drones.add(Flatten(input_shape=(1,), name='drones'))
    drones_input = Input(shape=(1,), name='drones')
    drones_encoded = drones(drones_input)

    #con = concatenate([target_encoded, obstacles_encoded, drones_encoded])
    con = concatenate([target_encoded, drones_encoded])

    hidden = Dense(16, activation='relu')(con)
    for _ in range(2): 
      hidden = Dense(16, activation='relu')(hidden)
    output = Dense(actions, activation='linear')(hidden)
    #model_final = Model(inputs=[target_input, obstacles_input, drones_input], outputs=output)
    model_final = Model(inputs=[target_input, drones_input], outputs=output)
    return model_final

# def build_model(states, actions, env):
#     drones_model = Sequential()
#     drones_model.add(Flatten(input_shape = (len(env.drones),)))
#     drones_model.add(Dense(24, activation='relu'))
    
#     obstacles_model = Sequential()
#     obstacles_model.add(Flatten(input_shape = (len(env.obstacles_pos),)))
#     obstacles_model.add(Dense(8, activation='relu'))

#     target_model = Sequential()
#     target_model.add(Flatten(input_shape = (len(env.targets_pos),)))
#     target_model.add(Dense(8, activation='relu'))

#     conca_model = concatenate([drones_model, obstacles_model, target_model])

#     hidden = Dense(24, activation='relu')(conca_model)
#     for _ in range(2): 
#         hidden = Dense(16, activation='relu')(hidden)

#     output = Dense(actions, activation='linear')(hidden)
#     model_final = Model(inputs=[drones_model, obstacles_model, target_model], outputs=output)

#     return model_final

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, 
                  nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    dqn.processor = MultiInputProcessor(2)
    return dqn



##### Test #####
# MAX 34x25 block map render 


def parser(file_ap):
  f = open(file_ap, "r")
  elems = f.readlines()
  for i in range(len(elems)):
    if elems[i][-1] == "\n":
      elems[i] = elems[i][:-1]
  nb_drones = int(elems[0][0])
  map_meter = elems[1].split()
  map_width_meter = float(map_meter[0])
  map_height_meter = float(map_meter[1])
  nb_items = 0

  targets_pos = []
  obstacles_pos = []
  l = None
  for i in range(2, len(elems)):
    l = elems[i].split() 
    if(len(l) >= 3):
      nb_items += 1
      if(l[0] == "H"):
        start_pos = (int(l[1]), int(l[2]))
      elif(l[0] == "T"):
        targets_pos.append((int(l[1]), int(l[2])))
      else:
        raise Exception("unhandle parameter: " + l[0])
    elif(len(l) == 1):
      for j in range(len(l[0])):
        if(l[0][j] == "x"):
          obstacles_pos.append((j,i - 2 - nb_items , 0))
        elif(l[0][j] in "0123456789ABCDEF"):
          if(l[0][j] != "0"):
            obstacles_pos.append((j,i - 2 - nb_items,  l[0][j]))
        else:
          raise Exception("unhandle parameter: " + l[0][j])        
  map_simu_dims = (len(l[0]), len(elems) - nb_items - 2)
  map_real_dims = (map_width_meter, map_height_meter)

  return ManagerEnv(nb_drones, map_real_dims, map_simu_dims, start_pos, targets_pos, obstacles_pos)