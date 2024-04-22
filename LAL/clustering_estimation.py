import networkx as nx
import numpy as np
import math

def path_2(RR_G,G,triangle_dic):
    path_dic={}
    result=np.dot(RR_G,RR_G)


    for i in G.nodes():
        num_i=np.sum(result[:,i])-result[i][i]-2*triangle_dic[i]
        path_dic[i]=num_i

    return path_dic

def triangle_dic_cal(RR_G,G):
    result=np.linalg.matrix_power(RR_G,3)
    triangle_dic={}
    for i in G.nodes():
        triangle_dic[i]=result[i][i]/2
    return triangle_dic


def cc_par(number,degree):
    if number >= 1:
        return (degree**(-0.132)+1)/2
    elif number <= 0:
        return (degree**(-0.132)+0)/2
    else:
        return (number+degree**(-0.132))/2

def cc_par_naive(number):
    if number >= 1:
        return 0.5
    elif number <= 0:
        return 0
    else:
        return number

def lcc_triangle(number,degree,t2,p,n,gama,Count1,Count2):

    if degree>=2:
        true_number1 = 1 / (p ** 2 * (2 * p - 1)) * (number - (degree * (degree - 1) * p ** 2 * (1 - p)) / 2 - (
                degree * (n - degree - 1) * p * (1 - p) * gama) - (n - degree - 1) * (n - degree - 2) * (
                                                             1 - p) ** 2 * gama / 2)

        true_number3 = 1 / (Count1 * (2 * p - 1)) * (
                    number / (p * (1 - p)) - t2 / (2 * p * p - 2 * p + 1) - Count1 * degree*(degree-1)/2 * (
                        1 - p) - Count2 * (n - degree - 1)*(n-degree-2)/2 * gama)

        cc_par1 = 2 * true_number1 / (degree * (degree - 1))
        cc_par2 = 2*true_number3/(degree*(degree-1))

        lcc_naive=cc_par_naive(cc_par1)
        lcc_1 = cc_par_naive(cc_par2)
        lcc_2 = cc_par(cc_par2, degree)

    else:
        true_number1 = 0
        true_number3 = 0
        lcc_naive=0
        lcc_1 = 0
        lcc_2=0


    return ([true_number1,true_number3,lcc_naive,lcc_1,lcc_2])


def clustering_coefficient(epsilon_lap,epsilon_RR,RR_G,degree_dic_naive,degree_dic_deduction,G):

    p=1-1/(np.e**epsilon_RR+1)

    degree_sum = sum(degree_dic_naive.values())

    n = len(G.nodes())
    gama_temp = degree_sum / (n * (n - 1))
    gama = gama_temp * p + (1 - gama_temp) * (1 - p)

    Count1=p/(1-p)-2*p*(1-p)/(1-2*p+2*p*p)
    Count2=(1-p)/p-2*p*(1-p)/(1-2*p+2*p*p)

    coefficient_dic1_lap = {}
    coefficient_dic2_lap = {}
    coefficient_dic3_lap = {}
    coefficient_dic4_lap = {}

    triangle_dic_true=nx.triangles(G)
    triangle_dic=triangle_dic_cal(RR_G,G)
    path_dic=path_2(RR_G,G,triangle_dic)

    num_1_lap=0
    num_3_lap=0

    mean_err1 = 0
    mean_err2 = 0

    for i in G.nodes():
        number = triangle_dic[i]
        degree_lap = degree_dic_naive[i]
        degree_deduction=degree_dic_deduction[i]

        t2=path_dic[i]

        result_lap=lcc_triangle(number,degree_lap,t2,p,n,gama,Count1,Count2)
        result_deduction=lcc_triangle(number,degree_deduction,t2,p,n,gama,Count1,Count2)

        # mean_err1 += abs(result_lap[0] - triangle_dic_true[i])
        # mean_err2 += abs(result_lap[1] - triangle_dic_true[i])
        mean_err1 += (result_lap[0] - triangle_dic_true[i])**2
        mean_err2 += (result_lap[1] - triangle_dic_true[i])**2

        coefficient_dic1_lap[i]=result_lap[2]
        coefficient_dic2_lap[i]=result_lap[3]
        coefficient_dic3_lap[i]=result_lap[4]
        coefficient_dic4_lap[i]=result_deduction[4]


        num_1_lap+=result_lap[0]/3
        num_3_lap+=result_lap[1]/3

    #T_T=1612010
    #T_T=1351441

    #print(abs(num_1_lap-T_T)/T_T)
    #print(abs(num_3_lap-T_T)/T_T)

    #print((num_1_lap-T_T)/T_T,(num_3_lap-T_T)/T_T)

    return([coefficient_dic1_lap,coefficient_dic2_lap,coefficient_dic3_lap,coefficient_dic4_lap])

def err(G_true,clustering_coefficient):

    f=open("result.txt","w")

    mse_sum = 0
    cc_true_dic=nx.clustering(G_true)

    for i in G_true.nodes():
        if i in clustering_coefficient.keys():
            mse_sum += (cc_true_dic[i] - clustering_coefficient[i]) ** 2
            f.write(str(cc_true_dic[i])+" "+str(clustering_coefficient[i])+"\n")
        else:
            mse_sum += cc_true_dic[i] ** 2
            f.write(str(cc_true_dic[i])+ " "+str(0)+"\n")

    f.close()

    return (mse_sum / len(G_true.nodes))
