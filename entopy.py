import os
from collections import Counter
import math


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



    #Calculate H(Xn,.......,Xn+k)
    H = 0
    for key in p:    
        H += p[key]*math.log2(p[key])*-1

    #print(H)
    return H


def calc(mem,filename):
    Entropy_joint = []
    for mem in range (0,mem+1):
        Entropy_joint.append(joint_entropy(mem,filename))

    Entropy_conditional = []
    for i in range (0,mem): #for i in range (0,mem-1)
        Entropy_conditional.append(Entropy_joint[i+1]-Entropy_joint[i])


    print(filename)
    size = os.path.getsize(filename)
    size_bits = size*8
    #size_compressed = size*Entropy_joint[i]
    print("Memory (i) \t", "Entropy H(X_n, X_n+1,.....,X_n+i) \t", "Entropy H(X_n|X_n-1,.....,X_n-i) \t", "Max Compression Ratio")
    #print("")
    for i in range(0,mem+1):
        size_compressed = size*(Entropy_conditional[i-1] if i>0  else Entropy_joint[i])
        print("\t{} \t {} \t \t \t {} \t \t \t {}".format(i, Entropy_joint[i], Entropy_conditional[i-1] if i>0  else Entropy_joint[i], size_compressed/size_bits))
        #print(i, Entropy_joint[i], Entropy_conditional[i-1])
    #print("")
    print("------------------------------------------------------------------------------------------------------------------------------------------------")

#----------------------------------------------------

mem = 3 #Choose memory for the entropy

#loop runt alla filer
for filename in os.listdir("cantrbry"):
    calc(mem,"cantrbry/" + filename)

for filename in os.listdir("large"):
    calc(mem,"large/" + filename)

