import numpy as np

from statistics import mode
import networkx as nx

def Err_L(epsilon_sum, epsilon_lap, G):
    n = len(G.nodes())
    d = mode([j for (i, j) in nx.degree(G)])
    if d==1:
        d=2

    num_4 = 1

    num_5 = (n - d - 1) ** 2 * (n - d - 2) ** 2 / 2 / (n - 1) / (n - 2)
    num_2 = 8 * (10 * d ** 2 - 10 * d + 3)

    num_0 = np.e ** ((epsilon_sum - epsilon_lap) / 2)#LAGL的限制条件
    num_1 = (num_0 + 2) / (num_0 ** 3 * (num_0 - 1) ** 2)
    num_3 = d ** 2 * (d - 1) ** 2 * epsilon_lap ** 2

    err = (num_4 ** 2 + num_5 * num_1) * (1 + num_2 / num_3)

    return err

def KL(lamda,miu):
    a=lamda*miu**2
    b=miu**2
    if a>=1:
        return 100
    result=a*np.log(a/b)+(1-a)*np.log((1-a)/(1-b))
    return result

def clip_one_six(miu,d_i):
    lamda = 1
    while 1>0:
        probility = np.e ** ((-d_i) * KL(lamda,miu))
        if probility <= 10**(-6):
            k_i=lamda*miu**2*d_i
            return k_i
        lamda+=0.01#此步长可以设置的更小以使差异更明显

def k_i_list(miu,d,epsilon_clip,number):
    p=1.5*1/(number*100)
    alpha=-2*np.log(2*p)/epsilon_clip#已经包含了alpha的计算
    Q=clip_one_six(miu,d+alpha)
    return Q


def Err_G(epsilon, epsilon_clip, miu, G):
    n = len(G.nodes())
    degree_list = [j for (i, j) in nx.degree(G)]
    d = sum(degree_list) / n

    e_1 = epsilon_clip
    e_2 = (epsilon - epsilon_clip) / 2#LAGL的限制条件
    k_i = k_i_list(miu, d, e_1, n)
    return (k_i ** 2 / ((1 - np.e ** (-e_2)) ** 2) / (e_2 ** 2))
