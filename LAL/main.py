import graph_disturb
import networkx as nx
import clustering_estimation
import degree_deduction as dd
import numpy as np
import time

print("hello")

# 可调节的参数：
# G和d用facebook或astroph，选用一个注释掉一个
# epsilon，epsilon_0
# 输出：MSE误差


G=nx.read_edgelist("./data/face_seq.txt",nodetype=int)
#G=nx.read_edgelist("./data/astro_seq.txt",nodetype=int)

epsilon=2
epsilon_0=0.29

epsilon_RR = 0.71
degree_lap_dic = graph_disturb.degree_disturb(epsilon_0, G)
degree_dic_naive = dd.degree_estimation(degree_lap_dic)
degree_dic_deduction = dd.degree_deduction(epsilon_0, degree_lap_dic)
RR_G = graph_disturb.RR_sample_G(epsilon_RR, G)
result = clustering_estimation.clustering_coefficient(epsilon_0, epsilon_RR, RR_G, degree_dic_naive,degree_dic_deduction, G)  # 局部聚类系数的估算
print("双任务LF-GDPR", epsilon, "mse:", [clustering_estimation.err(G, i) for i in result])

