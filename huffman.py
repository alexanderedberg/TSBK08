#import numpy as np
from collections import Counter



file = "cantrbry/alice29.txt"

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
    def __init__(self, proba, sym, left=None, right=None):
        self.right = right
        self.left = left
        self.probability = proba
        self.sym = sym

    #def get_proba(self):
        #return self.probability

    
    def inorderTraversal(self,res):
        
        if self.left:
            res += "0"
            self.left.inorderTraversal(res)
        if self.sym != None:
            codeword_dict[self.sym] = res
            #print(codeword_dict[self.sym])
            #print(res)
        if self.right:
            res += "1"
            self.right.inorderTraversal(res)

        #return res

proba_dict = joint_entropy(0,file) #"cantrbry/alice29.txt"

codeword_dict = proba_dict

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

    
res=""
node.inorderTraversal(res)


#read the file one symbol at a time, use said symbol as key in codeword_dict and write the corresponding value to a new file? "thisfile_huffman.txt"

#encode
with open(file,"rb") as f:

    o = open("demofile2.txt", "w")

    while True:
        char = f.read(1)
        if not char:
            #print("End of file")
            break
            #=codeword_dict[char]
        o.write(codeword_dict[char])
        #file_data = f.read(1)
        #print(f.read(1))
        #o = open("demofile2.txt", "a")
        #o.write(codeword_dict[f.read(1)])
        #o.close()
        #print(file_data)
        #print(codeword_dict[file_data])
    o.close()

"""
    o = open("demofile2.txt", "r")
    st = o.read()
    o.close()

    o = open("demofile2.txt", "w")
    #print(st)    
    o.write(' '.join(format(ord(x), 'b') for x in st))
    o.close()
"""



#decode
file = "demofile2.txt"
with open(file,"r") as o:

    #nr_bits = len(o.read())
    #print(nr_bits)
    for i in o: #range(10): len(o.read()) range(22609)
        #print(i)
        #print()
        print(o.read(2))
        #print(file_data44)






#print(codeword_dict)
#for key in proba_dict:
    #print(len(proba_dict))
    #print(key.probability)
