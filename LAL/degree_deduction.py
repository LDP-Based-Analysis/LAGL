import numpy as np

def weight_count(x,d,lamda,degree_list):
    P=0.5*np.e**(-(d-0.5-x)/lamda)-0.5*np.e**(-(d+0.5-x)/lamda)
    return P*degree_list.count(d)


def exp_cal(x, lamda, degree_lap):
    num_son = 0
    num_dad = 0
    temp = 0

    temp = 0
    for d in range(1, 2000):
        # print(d)
        weight = weight_count(x, d, lamda, degree_lap)
        #print(weight)
        num_son += weight * d
        num_dad += weight
        if num_son / num_dad - temp < 10 ** (-6):
            break
        else:
            temp = temp = num_son / num_dad
    return num_son / num_dad

def degree_deduction(epsilon_lap,degree_dic):
    lamda=2/epsilon_lap

    degree_lap=[round(i) for i in list(degree_dic.values())]

    clip = round(exp_cal(-4,lamda,degree_lap))

    new_degree_dic = {}
    number = len(degree_lap)

    for node in degree_dic.keys():
        degree = round(degree_dic[node])  # 度的敏感度设置为2可以达到epsilon_lap的效果
        if degree <= 1:
            degree = clip
        elif degree > number:
            degree = number
        new_degree_dic[node] = degree
    return new_degree_dic



def degree_estimation(degree_dic):
    new_degree_dic={}
    number = len(list(degree_dic.keys()))

    for node in degree_dic.keys():
        degree = round(degree_dic[node])  # 度的敏感度设置为2可以达到epsilon_lap的效果
        if degree <= 1:
            degree = 1
        elif degree > number:
            degree = number
        new_degree_dic[node]=degree

    return new_degree_dic