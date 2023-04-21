from collections import Counter


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


        return p


class Nodes:
    def __init__(self, proba, sym, left=None, right=None):
        self.right = right
        self.left = left
        self.probability = proba
        self.sym = sym


    def inorderTraversal(self,res):

        if self.left:
            #print("left")
            res += "0"
            self.left.inorderTraversal(res)
            res = res[:-1]

        if self.sym is not None:
            #print(res)
            codeword_dict[self.sym] = res

        if self.right:
            #print("right")
            res += "1"
            self.right.inorderTraversal(res)
            res = res[:-1]

    def decode_huffman(self, root, bin):
        #file = file[:-5]
        with open(bin,"r") as f , open(file + "_decompressed","wb") as o:
            #f = f[:-5]
            while True:
                char = f.read(1)
                #print(char)
                if not char:
                    break

                if self.sym is not None:
                    #write symbol to file
                    #start over at the root
                    o.write(self.sym)
                    self = root

                if char == "0":
                    self = self.left
                    

                if char == "1":
                    self = self.right


file = "cantrbry/alice29.txt" #asyoulik.txt #cantrbry #bible.txt #E.coli #alice29.txt

proba_dict = joint_entropy(0,file) #"cantrbry/alice29.txt"

codeword_dict = proba_dict
list = []

#Create the leafs from the dictionary
for key in proba_dict:
    node = Nodes(proba_dict[key], key)
    list.append(node)


list.sort(key=lambda p: p.probability)

#Create all other nodes from the inital leafs, n leafs = n-1 parent nodes. 
for x in range(0,len(list)+len(list)-2,2): #0,len(list)-1,2

    node = Nodes(list[x].probability + list[x+1].probability, None, list[x], list[x+1])

    list.append(node)
    list.sort(key=lambda p: p.probability)


#print(node.probability)

#Traverse the huffman tree and get the codewords for each symbol
res=""
node.inorderTraversal(res) #This is the last node created, so the root node with probability 1

#print(proba_dict)

#encode

#read each symbol and write it as its' codeword
with open(file,"rb") as f , open("temp","w") as o:

    while True:
        char = f.read(1)
        #print(char)
        if not char:
            #print("End of file")
            #print(char)
            break
        
        o.write(codeword_dict[char])

#print(char)
#print(codeword_dict[])


#pad the file with 0 so that the number of bits are divisible by 8, after that read the file with 8bits at a time, convert the 8bit representation to an int and then
#convert that to byte and write.
with open("temp","r+") as o, open(file + "_compressed","wb") as output: 

    bitstream = o.read()
    bitstream_len = len(bitstream)

    #pad with 0's
    while bitstream_len%8 != 0:
        o.write("0")
        print("pad")
        bitstream_len += 1

            
    #Start reading 8bits at a time
    o.seek(0)
    bytearray = bytearray()
    while True:
        bits_8 = o.read(8)

        if not bits_8:
            break
        
        to_int = int(bits_8,2)
        #print()
        bytearray.append(to_int)
    
    #print(bytearray)
    output.write(bytearray)
#print(to_int)
#print(proba_dict)
#print(codeword_dict)






#decode
#file = "encodetest"
with open(file + "_compressed","rb") as f , open("binary","w") as o:

    #read each byte, convert to binary and write to new file
    string = ""
    while True:
        char = f.read(1)
        if not char:
            break
        
        string += '{0:08b}'.format(int.from_bytes(char, "big"))
        #o.write('{0:08b}'.format(int.from_bytes(char, "big")))
    #print(string)
    #string = string[:-5]
    o.write(string)
    #o.write('{0:08b}'.format(int.from_bytes(char, "big")))




node.decode_huffman(node,"binary")


#print('{0:08b}'.format(int.from_bytes(char, "big"))) #do this in loop and write to a file, then remove the padding (how do we know how much padding there is?), 
                                                     #then read and use the dict in reverse??


        
