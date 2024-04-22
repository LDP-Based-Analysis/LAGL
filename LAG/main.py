import os
import time

import graph_disturb
import networkx as nx
import numpy as np
import graph_triangle_count
import pickle
import degree_process as dp


if __name__ == '__main__':

    print("hello")

    str1 = "./data/face_end.txt"
    str2 = "./data/face_end.pkl"
    # str1 = "./data/gplus_end.txt"
    # str2 = "./data/gplus_end.pkl"


    #需要改的参数：
    # 1.数据集的选择
    # 2.epsilon的取值
    # 3.epsilon_clip的取值
    # 4.number_true的取值
    # 5.sample_p的取值
    # 6.degree_dic函数的sen参数
    # 7.count的取值计算，就是LAGL中的alpha


    if os.path.exists(str2):
        st = time.time()
        with open(str2, 'rb') as f:
            G = pickle.load(f)
        print('read pkl', time.time()-st)
    else:
        st = time.time()
        G=nx.read_edgelist(str1)
        print('read txt', time.time()-st)
        with open(str2, 'wb') as f:
            pickle.dump(G, f)

    print(G)
    index_dic={}
    node_list=list(G.nodes())
    for i in range(len(G.nodes())):
        index_dic[node_list[i]]=i


    epsilon=1

    #epsilon_clip = epsilon*0.1
    epsilon_clip = 0.07
    #gplus :  0.18,0.165,0.15,0.14,0.13,sample= -1 -1.5 -2 -2.5 -3
    #face  :  0.245,0.21,0.18,0.16,0.145,sample = 0,-0.5,-1,-1.5,-2

    epsilon_RR = (epsilon-epsilon_clip)/2
    epsilon_triangle = epsilon_RR

    p = np.e ** epsilon_RR / (np.e ** epsilon_RR + 1)


    number_face=1612010
    number_gplus=1073677742

    number_true=number_face

    sample_p = 10**(-2)/p
    Count = -2 * np.log(2 * 1.5 * 1 / (100 * len(G.nodes()))) / epsilon_clip  # 考虑epsilon和节点数目后CETC方法
    #Count=150
    sen=2
    print(Count)
    test_time=1
    for i in range(test_time):
        degree_dic = dp.degree_dic_get(epsilon_clip, G, Count, sen)
        RR_G = graph_disturb.RR_sample_G(epsilon_RR, sample_p, G, index_dic)

        number_1 = graph_triangle_count.double_cip_triangle(index_dic, degree_dic, G, RR_G, sample_p, epsilon_RR,epsilon_triangle)  # 三角形数目的估算
        print([(i-number_true)/number_true for i in number_1])#前六个输出是β从1-的-1到10的-6次方的总误差，后六个输出是没有Laplace噪声的误差


