import numpy as np
import networkx as nx


def KL(lamda, miu):
    a = lamda * miu ** 2
    b = miu ** 2
    if a >= 1:
        return 100
    result = a * np.log(a / b) + (1 - a) * np.log((1 - a) / (1 - b))
    return result


def clip_one_six(miu, d_i):
    lamda = 1
    k_i = [0 for i in range(6)]

    while 1 > 0:
        probility = np.e ** ((-d_i) * KL(lamda, miu))

        if probility <= 10 ** (-1) and k_i[0] == 0:
            k_i[0] = lamda * miu ** 2 * d_i
        if probility <= 10 ** (-2) and k_i[1] == 0:
            k_i[1] = lamda * miu ** 2 * d_i
        if probility <= 10 ** (-3) and k_i[2] == 0:
            k_i[2] = lamda * miu ** 2 * d_i
        if probility <= 10 ** (-4) and k_i[3] == 0:
            k_i[3] = lamda * miu ** 2 * d_i
        if probility <= 10 ** (-5) and k_i[4] == 0:
            k_i[4] = lamda * miu ** 2 * d_i
        if probility <= 10 ** (-6) and k_i[5] == 0:
            k_i[5] = lamda * miu ** 2 * d_i
            # print(k_i[5])
            return k_i
        lamda += 1


def k_i_list(miu, degree, Count):
    k_i_list = [[] for i in range(6)]

    num = 0
    for d in degree:
        #print(num)
        num += 1
        Q = clip_one_six(miu, d + Count)
        for t in range(6):
            k_i_list[t].append(Q[t])
    return k_i_list

def err_laplace(epsilon,epsilon_RR,miu,k_i_list):
    err_sum=0
    epsilon_tri=epsilon-epsilon_RR
    for k in k_i_list:
        err_sum+=k**2
    return 2*err_sum/(epsilon_tri**2)/(miu**4*(1-1/(np.e**epsilon_RR))**2)

def miu_err(list_1,list_2,num):
    beta=10**(-num-1)
    miu_sum=0
    for i in range(len(list_1)):
        miu_sum+=(list_1[i]-list_2[i])#list_1是beta更小的
    return miu_sum*beta

def err(miu,lamda):
    return (miu**2+2*lamda**2)

def err_sum(number,D_x,miu,epsilon):
    return (err(number/(miu**2*(1-np.e**(-epsilon/2))),(D_x/2)**0.5))


def beta_select(miu, epsilon, degree, Count):
    k_i_one_six = k_i_list(miu, degree, Count)

    err_min = 10 ** (30)
    i_temp = 0

    for i in range(0, 6):
        D_temp = err_laplace(epsilon, epsilon / 2, miu, k_i_one_six[i])
        miu_temp = miu_err(k_i_one_six[5], k_i_one_six[i], i + 1)

        err_temp = err_sum(miu_temp, D_temp, miu, epsilon)
        #print(i + 1, err_temp)
        if err_temp <= err_min:
            err_min = err_temp
            i_temp = i
    return 10 ** (-i_temp - 1)
