import numpy as np
import networkx as nx
import math
import βSelect as beta

#G=nx.read_edgelist("facebook_combined.txt")
# G=nx.read_edgelist("CA-AstroPh.txt")
# G=nx.read_edgelist("Email-Enron.txt")
G=nx.read_edgelist("gplus_combined.txt")

degree_list=[j for (i,j) in nx.degree(G)]

#需要的参数有miu，epsilon，epsilon-0

miu=10**(-2)

epsilon=2
epsilon_0=0.24


alpha=-2*np.log(2*1.5/(len(list(G.nodes()))*100))/epsilon_0
print(alpha)

print(beta.beta_select(10**(-1),epsilon-epsilon_0,degree_list,alpha))