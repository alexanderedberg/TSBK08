#import numpy as np
from collections import Counter



file = "cantrbry/alice29.txt" #asyoulik.txt #cantrbry #bible.txt #E.coli

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
            #print("left")
            res += "0"
            self.left.inorderTraversal(res)
            res = res[:-1]

        if self.sym is not None:
            print(res)
            codeword_dict[self.sym] = res

        if self.right:
            #print("right")
            res += "1"
            self.right.inorderTraversal(res)
            res = res[:-1]





proba_dict = joint_entropy(0,file) #"cantrbry/alice29.txt"

codeword_dict = proba_dict
#print(proba_dict)
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
#print(hubhub)


#encode

#read each symbol and write it as its' codeword
with open(file,"rb") as f , open("demofile2","w") as o:

    while True:
        char = f.read(1)
        if not char:
            #print("End of file")
            break
            #=codeword_dict[char]
        o.write(codeword_dict[char])


#pad the file with 0 so that the number of bits are divisible by 8
with open("demofile2","r+") as o, open("encodetest","wb") as output: 

    bitstream = o.read()
    bitstream_len = len(bitstream)
    #print(bitstream)
    #print(bitstream_len)

    while bitstream_len%8 != 0:
        o.write("0")
        bitstream_len += 1

            
    #print(bitstream_len)
    #bitstream = o.read()
    o.seek(0)
    bytearray = bytearray()
    while True:
        bits_8 = o.read(8)
        #print(char)
        if not bits_8:
            #print("End of file")
            break
            #=codeword_dict[char]
        
        #print(bits_8)
        #print(int(bits_8,2))
        to_int = int(bits_8,2)
        bytearray.append(to_int)
        #to_str = str(to_int)
        #bytes(to_int)
    
    #print(bytearray)
    output.write(bytearray) #bytes(bits_8,'ascii') to_str.encode()

#print(proba_dict)
#print(codeword_dict)





#for i in range (0,bitstream_len,8):

    #print(bitstream[i])

"""
    o = open("demofile2.txt", "r")
    st = o.read()
    o.close()

    o = open("demofile2.txt", "w")
    #print(st)    
    o.write(' '.join(format(ord(x), 'b') for x in st))
    o.close()
"""

#print(bin(to_int))
#print(format(to_int, 'b')) #use this later to convert from int to bin
#print(int(bin(to_int),2))


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
