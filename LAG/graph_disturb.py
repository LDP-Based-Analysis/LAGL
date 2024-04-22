import numpy as np

def RR_dis(p):
    rd = np.random.uniform(low=0, high=1)
    if rd > p:
        return 1
    else:
        return 0

def RR_sample_G(epsilon_RR,sample_p,G,index_dic):

    RR_G_dic={}
    node_list = list(G.nodes())
    number = len(node_list)

    p = np.e ** epsilon_RR / (np.e ** epsilon_RR + 1)

    miu1 = (1 - p) * sample_p
    miu2 = p * sample_p

    for i in range(len(node_list)):
        if i < int(number / 2):
            for t in range(1, int(number / 2) + 1):
                if RR_dis(miu1) == 0 and node_list[(i + t) % number] not in G.adj[node_list[i]] :
                    if index_dic[node_list[i]] > index_dic[node_list[(i + t) % number]]:
                        RR_G_dic[int(node_list[i]+node_list[(i + t) % number])]=1
                    else:
                        RR_G_dic[int( node_list[(i + t) % number]+node_list[i])] = 1
                elif RR_dis(miu2)==0 and node_list[(i + t) % number] in G.adj[node_list[i]]:
                    if index_dic[node_list[i]] > index_dic[node_list[(i + t) % number]]:
                        RR_G_dic[int(node_list[i] + node_list[(i + t) % number])] = 1
                    else:
                        RR_G_dic[int( node_list[(i + t) % number]+node_list[i])] = 1
        else:
            for t in range(1, int((number - 1) / 2) + 1):
                if RR_dis(miu1) ==0 and node_list[(i + t) % number] not in G.adj[node_list[i]]:
                    if index_dic[node_list[i]] > index_dic[node_list[(i + t) % number]]:
                        RR_G_dic[int(node_list[i] + node_list[(i + t) % number])] = 1
                    else:
                        RR_G_dic[int( node_list[(i + t) % number]+node_list[i])] = 1
                elif RR_dis(miu2)==0 and node_list[(i + t) % number] in G.adj[node_list[i]]:
                    if index_dic[node_list[i]] > index_dic[node_list[(i + t) % number]]:
                        RR_G_dic[int(node_list[i] + node_list[(i + t) % number])] = 1
                    else:
                        RR_G_dic[int( node_list[(i + t) % number]+node_list[i])] = 1
    return RR_G_dic