import numpy as np

def RR_dis(p):
    rd = np.random.uniform(low=0, high=1)
    if rd > p:
        return 1
    else:
        return 0

def KL(lamda,miu):
    a=lamda*miu**2
    b=miu**2
    if a>=1:
        return 100
    result=a*np.log(a/b)+(1-a)*np.log((1-a)/(1-b))
    return result

def clipthreshold(miu,d_i,beta):
    lamda = 1

    while 1>0:
        probility = np.e ** ((-d_i) * KL(lamda,miu))
        if probility <= beta:
            return (lamda * miu**2 * d_i)
        else:
            lamda += 1

def double_cip_triangle(index_dic,degree_dic,G_true,RR_G,sample_p,epsilon_RR,epsilon_triangle):
    p = 1 - 1 / (np.e ** epsilon_RR + 1)
    rou = 1 / (np.e ** epsilon_RR)
    miu_true = (sample_p * p) ** 2


    triangles1=0
    triangles2=0
    triangles3 = 0
    triangles4 = 0
    triangles5 = 0
    triangles6 = 0

    triangles1_true = 0
    triangles2_true = 0
    triangles3_true = 0
    triangles4_true = 0
    triangles5_true = 0
    triangles6_true = 0


    q = 0
    for i in G_true.nodes():
        #print(q)
        q = q + 1
        d_i=degree_dic[i]
        k_i_6=clipthreshold(p * sample_p, d_i, 10 ** (-6))
        k_i_5 = clipthreshold(p * sample_p, d_i, 10 ** (-5))
        k_i_4=clipthreshold(p * sample_p, d_i, 10 ** (-4))
        k_i_3 = clipthreshold(p * sample_p, d_i, 10 ** (-3))
        k_i_2 = clipthreshold(p * sample_p, d_i, 10 ** (-2))
        k_i_1 = clipthreshold(p * sample_p, d_i, 10 ** (-1))

        s = 0

        count_1=0
        count_2=0
        count_3 = 0
        count_4 = 0
        count_5 = 0
        count_6 = 0

        for j in G_true.adj[i]:
            if index_dic[j] < index_dic[i]:
                count_temp1=0
                for k in G_true.adj[i]:
                    if index_dic[k] > index_dic[j] and index_dic[k]<index_dic[i]:
                        s+=1
                        if int(k+j) in RR_G.keys() and int(i+k) in RR_G.keys():
                            count_temp1+=1

                count_6 += min(k_i_6, count_temp1)
                count_5 += min(k_i_5, count_temp1)
                count_4 += min(k_i_4, count_temp1)
                count_3 += min(k_i_3, count_temp1)
                count_2 += min(k_i_2,count_temp1)
                count_1 += min(k_i_1,count_temp1)
                #if count_temp1>=k_i_1:
                    #print("clip")

        result1 = (count_1 - miu_true * rou * s)+np.random.laplace(0,k_i_1/epsilon_triangle)
        result2 = (count_2 - miu_true * rou * s)+np.random.laplace(0,k_i_2/epsilon_triangle)
        result3 = (count_3 - miu_true * rou * s)+np.random.laplace(0,k_i_3/epsilon_triangle)
        result4 = (count_4 - miu_true * rou * s)+np.random.laplace(0,k_i_4/epsilon_triangle)
        result5 = (count_5 - miu_true * rou * s)+np.random.laplace(0,k_i_5/epsilon_triangle)
        result6 = (count_6 - miu_true * rou * s)+np.random.laplace(0,k_i_6/epsilon_triangle)

        result1_true=(count_1-miu_true * rou * s)
        result2_true = (count_2 - miu_true * rou * s)
        result3_true = (count_3 - miu_true * rou * s)
        result4_true = (count_4 - miu_true * rou * s)
        result5_true = (count_5 - miu_true * rou * s)
        result6_true = (count_6 - miu_true * rou * s)

        triangles1+=result1
        triangles2+=result2
        triangles3 += result3
        triangles4 += result4
        triangles5 += result5
        triangles6 += result6

        triangles1_true += result1_true
        triangles2_true += result2_true
        triangles3_true += result3_true
        triangles4_true += result4_true
        triangles5_true += result5_true
        triangles6_true += result6_true


    list_1=[]
    list_1.append(triangles1/(miu_true*(1-rou)))
    list_1.append(triangles2 / (miu_true * (1 - rou)))
    list_1.append(triangles3 / (miu_true * (1 - rou)))
    list_1.append(triangles4 / (miu_true * (1 - rou)))
    list_1.append(triangles5 / (miu_true * (1 - rou)))
    list_1.append(triangles6 / (miu_true * (1 - rou)))

    list_1.append(triangles1_true / (miu_true * (1 - rou)))
    list_1.append(triangles2_true / (miu_true * (1 - rou)))
    list_1.append(triangles3_true / (miu_true * (1 - rou)))
    list_1.append(triangles4_true / (miu_true * (1 - rou)))
    list_1.append(triangles5_true / (miu_true * (1 - rou)))
    list_1.append(triangles6_true / (miu_true * (1 - rou)))

    return (list_1)