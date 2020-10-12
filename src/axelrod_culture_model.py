import pandas as pd
import random
import time
import copy

class Agent(object):
    def __init__(self, place_i, place_j):
        self.culture = [random.randint(0, 9) for _ in range(5)]
        self.place_i = place_i
        self.place_j = place_j

    def return_culture(self):
        return self.culture

    def return_place_i(self):
        return self.place_i

    def return_place_j(self):
        return self.place_j

    def pick_neighbor_agent(self):
        while True:
            i_diff, j_diff = random.choice([1, -1]), random.choice([1, -1])
            i_neighbor = self.place_i+i_diff
            j_neighbor = self.place_j+j_diff
            
            if (0 <= i_neighbor <= 9) and (0 <= j_neighbor <= 9):
                break

        return i_neighbor, j_neighbor
    
    def is_interaction(self, neighbor_agent_culture):
        similarity = 0
        for trait_agent, trait_agent_neighbor in zip(self.culture, neighbor_agent_culture):
            if trait_agent == trait_agent_neighbor:
                similarity += 1
            
        box = [1 for _ in range(similarity)] + [0 for _ in range(5-similarity)]
        if random.choice(box) == 1:
            return True
        else:
            return False

    def interaction(self, neighbor_agent_culture):
        while True:
            pick_trait = random.choice(range(5))
            if not self.culture[pick_trait] == neighbor_agent_culture[pick_trait]:
                break
        self.culture[pick_trait] = neighbor_agent_culture[pick_trait]


class CultureDiffusion(object):
    def __init__(self, time):
        self.time = time
        self.agent_list = [Agent(place_i=i, place_j=j) for i in range(10) for j in range(10)]

    def pick_agent(self):
        idx = random.choice(range(100))
        agent = self.agent_list[idx]

        return agent

    def get_neighbor_agent(self, agent):
        i_neighbor, j_neighbor = agent.pick_neighbor_agent()
        for candidate in self.agent_list:
            if (candidate.return_place_i() == i_neighbor) and (candidate.return_place_j() == j_neighbor):
                neighbor_agent = candidate
                return neighbor_agent
                break

    def diffusion(self):
        for t in range(self.time):
            agent = self.pick_agent()
            neighbor_agent = self.get_neighbor_agent(agent)
            neighbor_agent_culture = neighbor_agent.return_culture()

            if agent.is_interaction(neighbor_agent_culture):
                agent.interaction(neighbor_agent_culture)
    
# main
evolve = CultureDiffusion(time=1000)
evolve.diffusion()



# agent_list = [Agent(place_i=i, place_j=j) for i in range(10) for j in range(10)]
# idx_picked_agent = random.choice(range(100))
# agent = agent_list[idx_picked_agent]
# neighbor_i, neighbor_j = agent.pick_neighbor_agent()

# hoge = agent_list[49]

# def make_agent_culture():
#     return [random.randint(0, 9) for _ in range(5)]

# def make_site():
#     site = pd.DataFrame()
#     for col in range(10):
#         site[col] = [make_agent_culture() for _ in range(10)]
#     return site

# def pick_agent(site):
#     i, j = random.randint(0, 9), random.randint(0, 9)
#     return i, j, site.iloc[i, j]

# def pick_neighbor(i, j, site):
#     while True:
#         i_diff, j_diff = random.choice([1, -1]), random.choice([1, -1])
#         if (0 <= i+i_diff <= 9) and (0 <= j+j_diff <= 9):
#             break
#     return i+i_diff, j+j_diff, site.iloc[i+i_diff, j+j_diff], 

# def is_interaction(agent_selected, agent_neighbor):
#     similarity = 0
#     for trait_agent_selected, trait_agent_neighbor in zip(agent_selected, agent_neighbor):
#         if trait_agent_selected == trait_agent_neighbor:
#             similarity += 1
    
#     box = [1 for _ in range(similarity)] + [0 for _ in range(5-similarity)]
#     if random.choice(box) == 1:
#         return True
#     else:
#         return False

# def interaction(agent_selected, agent_neighbor):
#     while True:
#         pick_trait = random.choice(range(5))
#         if not agent_selected[pick_trait] == agent_neighbor[pick_trait]:
#             break
#     agent_selected[pick_trait] = agent_neighbor[pick_trait]

#     return agent_selected


# # main
# if __name__ == '__main__':
#     site = make_site()
#     print(site)

#     for t in range(10):
#         i, j, agent_selected = pick_agent(site)
#         i_neighbor, j_neighbor, agent_neighbor = pick_neighbor(i, j, site)
#         if is_interaction(agent_selected, agent_neighbor):
#             site.iloc[i, j] = interaction(agent_selected, agent_neighbor)
#             print(f'happen interaction at {i}, {j} !!')
        
#         print(t)
#         time.sleep(0.5)
    
#     print(site)
