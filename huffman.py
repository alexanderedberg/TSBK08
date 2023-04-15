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
    def __init__(self, proba, sym, left=None, right=None, bit=None):
        self.right = right
        self.left = left
        self.probability = proba
        self.sym = sym
        self.bit = bit

    #def get_proba(self):
        #return self.probability

proba_dict = joint_entropy(0,"cantrbry/alice29.txt")


list = []

for key in proba_dict:
    #print(key)
    node = Nodes(proba_dict[key], key)
    #print(key.probability)
    list.append(node)


#print(node.probability)

list.sort(key=lambda p: p.probability)



#create all other nodes from the inital leafs, n leafs = n-1 parent nodes. 
for x in range(0,len(list)+len(list)-2,2): #0,len(list)-1,2

    #print(x)

    node = Nodes(list[x].probability + list[x+1].probability, None, list[x], list[x+1])
    list.append(node)
    list.sort(key=lambda p: p.probability)

    #Give left child 0 bit and right child 1
    list[x].bit = 0 
    list[x+1].bit = 1

    #print(x)
    #print(node.left.sym)
    #print(node.probability)

for i in range(10):
    print(list[i].bit)




#for key in proba_dict:
    #print(len(proba_dict))
    #print(key.probability)




#go throught list of nodes and find the two smallest values, add new node based on those values and append that node to the list

# how do we ignore "used" nodes??? move all used nodes to new list???, put used nodes in the front of the list and push starting index for the for loop each time
