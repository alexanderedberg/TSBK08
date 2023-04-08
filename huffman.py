#import numpy as np
from collections import Counter





# Get probability distribution, same method as in entropy.py shouuld be fine
# 
# Sort probabilitys in array (use numpy) (use sort array and look in reverse ???? ([::-1]))
# 
# root node is 1
# 
# create leafs from each probability
# 
# add the sammelst leafs to create a new LEAF NODE/PARENT NODE, only the node with probability 1 is the root node
#
#

#file = "cantrbry/alice29.txt"

"""
with open(file,"rb") as f:

        file_data = f.read()
        print(file_data)
"""

def joint_entropy(mem,file):

    with open(file,"rb") as f:

        file_data = f.read()
        nr_symbols = len(file_data)
        #print(file_data)
        

        list = [] #to store each k-tuple in, k is mem+1 in size

        for i in range(mem,nr_symbols):
            list.append(file_data[i-mem:i+1]) #add each k-tuple to the list


        freq = Counter(list) #count frequecy for each k-tuple
        p = {} #probability

        #Find probability for each k-tuple 
        for key in freq:
            #print(key, '->', freq[key])

            p[key] = freq[key]/(nr_symbols-mem)


        #print(p)
        return p
    #Calculate H(Xn,.......,Xn+k)
    #H = 0
    #for key in p:    
    #    H += p[key]*math.log2(p[key])*-1

    #print(H)
    #return H

class Nodes:
    def __init__(self, proba, right=None, left=None):
        self.right = right
        self.left = left
        self.probability = proba

proba_dict = joint_entropy(0,"cantrbry/alice29.txt")

"""
node = Nodes(0.5)
print(node.probability)

node2 = Nodes(0.2)

node3 = Nodes(node.probability+node.probability, node, node2)

print(node3.right.probability)
"""
list = []
test_dict = {}

for key in proba_dict:
    print(key)
    test_dict[key] = Nodes(proba_dict[key])
    #print(key.probability)

for key in test_dict:
    print(key, "----->" , test_dict[key].probability)


# sort dict???
# 


#for key in proba_dict:
    #print(len(proba_dict))
    #print(key.probability)


