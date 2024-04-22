import numpy as np
import networkx as nx

def edgeclip(G,epsilon_0):
    degree_lap_list=[(j+np.random.laplace(0,2/epsilon_0)) for (i,j) in nx.degree(G)]
    return degree_lap_list

def degree_bias(degree_lap):
    degree_estimate=[]
    for i in degree_lap:
        if i<=1:
            degree_estimate.append(1)
        else:
            degree_estimate.append(i)
    return degree_estimate


def miu_sum(degree_estimate, epsilon_0, count):
    sum_1 = 0
    sum_partion = 0
    lamda = 2 / epsilon_0
    for d in degree_estimate:
        # num=(2*d*lamda-lamda**2+lamda)/2
        sum_partion += d
    sum_1 = lamda * sum_partion - lamda ** 2 / 2 * len(degree_estimate) - lamda / 2 * len(degree_estimate)
    p = 0.5 * np.e ** (-count * epsilon_0 / 2)

    return sum_1 * p

def lamda_cal(degree_lap_list,epsilon_0,epsilon_1,count):
    sum_1=0
    for i in degree_lap_list:
        sum_1+=(i+count)**2
    return sum_1**0.5

def err(miu,lamda):
    return (miu**2+2*lamda**2)

