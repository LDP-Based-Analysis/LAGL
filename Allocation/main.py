import numpy as np
import networkx as nx
import Privacy_Budget_Allocation as Allocation

G1=nx.read_edgelist("data/facebook_combined.txt")
G2=nx.read_edgelist("data/CA-AstroPh.txt")
# G4=nx.read_edgelist("data/gplus_combined.txt")

# for e in range(2,18,2):
#     print(Allocation.epsilon_G(e,G1,10**(-1)))

# print(Allocation.epsilon_G(1,G1,10**(-1)))  #LAG
# print(Allocation.epsilon_L(2,G1))  #LAL

for e in range(2,18,2):
    print(e)
    print(Allocation.epsilon(G2,e,10**(-1)))#三个参数,图数据,总隐私预算,μ取值