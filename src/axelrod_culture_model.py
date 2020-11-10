import random
from scipy import stats
from tqdm import tqdm
import pandas as pd

# ------------- #
# parameters
# ------------- # 
SIZE = 10 # size of lattice (if SIZE=10, then 10*10 lattice)
N_TRAITS = 10 # number of traits
N_FEATURES = 4 # number of features
TIME = 10000 # number of repeats
N_AGENTS = SIZE**2 # number of agents which is automatically determined if you decide SIZE

# example
# N_TRAITS = 10
# N_FEATURES = 4
# [3, 2, 9, 0, 1]
# each feature is 0 ~ 9

# ------------- #
# utils
# ------------- # 
def _get_agent_position(agent_list, agent):
    """エージェントリストからエージェントの格子における位置を出す

    Args:
        agent_list: agentのlist
        agent: listの中のagent

    Returns:
        x, y: エージェントの格子における座標位置
    """
    index = agent_list.index(agent)
    x = (index % SIZE) 
    y = (index // SIZE)

    return x, y

def get_neighbor_position(agent_list, agent):
    agent_x, agent_y = _get_agent_position(agent_list, agent)

    neighbor_left_x, neighbor_left_y = agent_x-1, agent_y
    neighbor_right_x, neighbor_right_y = agent_x+1, agent_y
    neighbor_above_x, neighbor_above_y = agent_x, agent_y+1
    neighbor_below_x, neighbor_below_y = agent_x, agent_y-1

    neighbors_position_list = []

    if (0 <= neighbor_left_x <=(SIZE-1)) and (0 <= neighbor_left_y <=(SIZE-1)):
        neighbors_position_list.append([neighbor_left_x, neighbor_left_y])

    if (0 <= neighbor_right_x <=(SIZE-1)) and (0 <= neighbor_right_y <=(SIZE-1)):
        neighbors_position_list.append([neighbor_right_x, neighbor_right_y])

    if (0 <= neighbor_above_x <=(SIZE-1)) and (0 <= neighbor_above_y <=(SIZE-1)):
        neighbors_position_list.append([neighbor_above_x, neighbor_above_y])

    if (0 <= neighbor_below_x <=(SIZE-1)) and (0 <= neighbor_below_y <=(SIZE-1)):
        neighbors_position_list.append([neighbor_below_x, neighbor_below_y])

    neighbor_position = random.choice(neighbors_position_list) # pick randomly

    return neighbor_position[0], neighbor_position[1]

def get_list_index_from_position(x, y):
    return SIZE*y+x


# ------------- #
# agent based model
# ------------- # 
class Agent:
    def __init__(self):
        self.culture = [random.randint(0, (N_TRAITS-1)) for _ in range(N_FEATURES)]

    def share_culture(self, agent_list):
        neighbor_x, neighbor_y = get_neighbor_position(agent_list, self)
        neighbor_index = get_list_index_from_position(neighbor_x, neighbor_y)
        neighbor_agent = agent_list[neighbor_index]

        similarity = 0 
        for agent_trait, neighbor_agent_trait in zip(self.culture, neighbor_agent.culture):
            if agent_trait == neighbor_agent_trait:
                similarity += 1
        prob_interact = similarity / N_FEATURES

        if stats.bernoulli.rvs(p = prob_interact) == 1: # do share culture
            different_trait_index_list = []
            for i, (agent_trait, neighbor_agent_trait) in enumerate(zip(self.culture, neighbor_agent.culture)):
                if agent_trait != neighbor_agent_trait:
                    different_trait_index_list.append(i)

            if 1 <= len(different_trait_index_list):
                different_trait_index = random.choice(different_trait_index_list)
                neighbor_agent.culture[different_trait_index] = self.culture[different_trait_index]

class Model:
    def __init__(self):
        self.agent_list = [Agent() for _ in range(N_AGENTS)]
        self.dic = {'0': [self.agent_list[i].culture for i in range(N_AGENTS)]}

    def show_lattice(self):
        for y in range(SIZE):
            row = []
            for x in range(SIZE):
                idx_agent_showed = get_list_index_from_position(x, y)
                agent_culture_show = self.agent_list[idx_agent_showed].culture
                row.append(agent_culture_show)
            print(row)
    
    def summarize_lattice(self):
        culture_list = []
        for idx in range(N_AGENTS):
            culture_list.append(self.agent_list[idx].culture)
        
        unique_culture_list = []
        for c in culture_list:
            if c not in unique_culture_list:
                unique_culture_list.append(c)
        n_unique_culture = len(unique_culture_list)

        return n_unique_culture

    def get_data(self, t_agent_list, dic, t):
        key = str(t+1)
        dic[key] = [t_agent_list[i].culture for i in range(N_AGENTS)]

        return dic

    def simulate(self):
        list_n_unique_culture = [self.summarize_lattice()] # 初期状態

        for t in tqdm(range(TIME)):
            agent = self.agent_list[random.randint(0, N_AGENTS-1)] # pick agent randomly
            agent.share_culture(self.agent_list)

            key = str(t+1)
            self.dic[key] = [self.agent_list[i].culture for i in range(N_AGENTS)]
 
            list_n_unique_culture.append(self.summarize_lattice())

        df = pd.DataFrame(self.dic)
        df.to_csv('./df.csv')
        
        df = pd.DataFrame({'n_unique_culture': list_n_unique_culture})
        df.to_csv('./df2.csv')


# ------------- #
# simulation
# ------------- # 
model = Model()
print('======================')
print('初期状態')
print('======================')
model.show_lattice()

model.simulate()

print('======================')
print('インタラクション後状態')
print('======================')
model.show_lattice()