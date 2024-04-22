import networkx as nx
import numpy as np

import alpha_Select as Select

G=nx.read_edgelist("C:/Users/K8/Code/数据处理/face_end.txt")
# G=nx.read_edgelist("C:/Users/K8/Code/数据处理/gplus_end.txt")

epsilon=0.3
epsilon_0=epsilon*0.2
epsilon_1=epsilon*0.8

degree_lap_list=Select.edgeclip(G,epsilon_0)
degree_estimate=Select.degree_bias(degree_lap_list)

err_min=10**31
count_end=1
err_temp=10**31
count_temp=0


for count in range(1,18000):
    #print(count)
    miu=Select.miu_sum(degree_estimate,epsilon_0,count)
    lamda=Select.lamda_cal(degree_lap_list,epsilon_0,epsilon_1,count)
    if Select.err(miu,lamda)<err_min:
        err_min=Select.err(miu,lamda)
        count_end=count
    else:
        print(count_end)
        break