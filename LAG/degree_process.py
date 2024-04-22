import numpy as np
import networkx as nx
import random

def degree_dic_get(epsilon_clip,G_true,number,sen):
    degree_dis_dic={}
    for i in G_true.nodes():
        degree_dis_dic[i]=nx.degree(G_true, i) + number+np.random.laplace(0,sen/epsilon_clip)
        if degree_dis_dic[i]<=0:
            degree_dis_dic[i]=0

    return degree_dis_dic

def graph_projection(G_true,degree_dic):
    for i in G_true.nodes():
        d_i=degree_dic[i]

        if nx.degree(G_true,i)>round(d_i):
            print("clip")
            i_adj=list(G_true.adj[i])
            i_adj_clip=random.sample(i_adj,nx.degree(G_true,i)-round(d_i))
            for q in i_adj_clip:
                print("djlkf")
                G_true.remove_edge(q,i)

    return G_true