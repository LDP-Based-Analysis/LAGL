from itertools import combinations
import networkx as nx
import numpy as np
import graph_disturb as gd
import math

def edge_count(G,RR_G):

    RR=RR_G
    num_list=[0,0,0,0]

    node_combination=combinations(G.nodes(),3)
    #print(math.comb(4039,3)/(10**6))

    tag_0=0
    for combination in node_combination:
        if tag_0%(10**6)==0:
            print(tag_0/(10**6))
        tag_0+=1
        num=RR[combination[0]][combination[1]]+RR[combination[0]][combination[2]]+RR[combination[1]][combination[2]]
        num_list[num]+=1

    return (num_list)


def num_count(G,RR_G,epsilon_RR):

    Count_1=np.e**epsilon_RR
    Count_2=(np.e**epsilon_RR-1)

    num_list=edge_count(G,RR_G)

    print(num_list)

    sum_triangle=1/(Count_2**3)*(-num_list[0]+num_list[1]*Count_1-num_list[2]*Count_1**2+num_list[3]*Count_1**3)

    return sum_triangle


G=nx.read_edgelist("./data/face_seq.txt",nodetype=int)
num=1612010

epsilon_RR=2
RR_G=gd.RR_sample_G(epsilon_RR,G)

#print(RR_G)
#RR_G=G
#print(RR_G)

print((num_count(G,RR_G,epsilon_RR)-num)/num)