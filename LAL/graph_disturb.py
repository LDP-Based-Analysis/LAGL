import itertools as itt
import random
import numpy as np
import networkx as nx

def degree_disturb(epsilon_lap,G):
    degree_dic = {}

    for i in G.nodes():
        degree = nx.degree(G, i) + np.random.laplace(0, 2 / epsilon_lap)  # 度的敏感度设置为2可以达到epsilon_lap的效果
        degree_dic[i] = degree
    return degree_dic

def RR_dis(p):
    rd = np.random.uniform(low=0, high=1)
    if rd > p:
        return 1
    else:
        return 0

def RR_sample_G(epsilon_RR,G):
    number = len(G.nodes())

    RR_G = np.zeros((number,number), dtype=float)

    p = np.e ** epsilon_RR / (np.e ** epsilon_RR + 1)

    miu1 = (1 - p)
    miu2 = p

    for i in G.nodes():
        if i < int(number / 2):
            for t in range(1, int(number / 2) + 1):
                if RR_dis(miu1) == 0 and (i+t)%number not in G.adj[i] :
                    RR_G[i][(i + t) % number] = 1
                    RR_G[(i + t) % number][i] = 1
                elif RR_dis(miu2)==0 and (i + t) % number in G.adj[i]:
                    RR_G[i][(i + t) % number] = 1
                    RR_G[(i + t) % number][i] = 1
        else:
            for t in range(1, int((number - 1) / 2) + 1):
                if RR_dis(miu1) ==0 and (i+t)%number not in G.adj[i]:
                    RR_G[i][(i + t) % number] = 1
                    RR_G[(i + t) % number][i] = 1
                elif RR_dis(miu2)==0 and (i + t) % number in G.adj[i]:
                    RR_G[i][(i + t) % number] = 1
                    RR_G[(i + t) % number][i] = 1
    return RR_G