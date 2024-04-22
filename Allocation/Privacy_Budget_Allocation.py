import Err_Analysis as Err

def epsilon_G(epsilon,G,miu):#LAGL下的隐私预算分配
    epsilon_0 = 0.01
    epsilon_0end = 0.01
    err_min = 10 ** 31
    while epsilon_0 <= 2:
        err_temp = Err.Err_G(epsilon, epsilon_0, miu, G)
        if err_temp < err_min:
            epsilon_0end = epsilon_0
            err_min = err_temp
        epsilon_0 += 0.01
    return(epsilon_0end)

def epsilon_L(epsilon,G):#LAGL下的隐私预算分配
    err_min = 10 ** (31)
    alfa_end = 0.001#epsilon_0/epsilon
    alfa = 0.001
    while alfa <= 0.999:
        err_temp = Err.Err_L(epsilon, epsilon * alfa, G)
        if err_temp <= err_min:
            err_min = err_temp
            alfa_end = alfa
        else:
            return alfa_end*epsilon
        alfa += 0.001


def epsilon(G, epsilon_sum, miu):

    t = 0.01

    num_123 = 0

    err_1_min = 10 ** 31

    err_2_min = 10 ** 31

    while t <= epsilon_sum / 2:
        t_temp = t + 0.01
        t_temp_2 = t + 0.02

        t1_now = Err.Err_L(epsilon_sum, t, G)
        t1_next = Err.Err_L(epsilon_sum, t_temp, G)
        t1_next_2 = Err.Err_L(epsilon_sum, t_temp_2, G)

        t2_now = Err.Err_G(epsilon_sum, t, miu, G)
        t2_next = Err.Err_G(epsilon_sum, t_temp, miu, G)
        t2_next_2 = Err.Err_G(epsilon_sum, t_temp_2, miu, G)

        temp = (t1_next - t1_now) / t1_now
        temp_next = (t1_next_2 - t1_next) / t1_next


        temp_2 = (t2_next - t2_now) / t2_now
        temp_2_next = (t2_next_2 - t2_next) / t2_next

        if num_123 == 0 and t2_now <= t2_next and t1_now >= t1_next and (temp + temp_2) * (temp_next + temp_2_next) <= 0:
            epsilon_end_1 = t
            num_123 = 1

        if num_123 == 0 and t2_now >= t2_next and t1_now <= t1_next and (temp + temp_2) * (temp_next + temp_2_next) <= 0:
            epsilon_end_1 = t
            num_123 = 1

        if t1_now < err_1_min:
            epsilon_end_2 = t
            err_1_min = t1_now
        if t2_now < err_2_min:
            epsilon_end_3 = t
            err_2_min = t2_now

        t += 0.01

    if abs(epsilon_end_2-epsilon_end_3)<=0.5:
        epsilon_end_1=0.5*(epsilon_end_2+epsilon_end_3)
    return ((epsilon_end_1+epsilon_end_3)/2,epsilon_end_2, epsilon_end_3)