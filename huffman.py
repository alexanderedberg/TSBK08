from collections import Counter
import os


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
        
        with open(bin,"r") as f , open("decompress/" + file + "_decompressed","wb") as o:
            while True:
                char = f.read(1)
                if not char:
                    o.write(self.sym) #needed so that last symbol is written
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

#Loop through all the files, just change to the correct dir
dir = "cantrbry/" #cantrbry/ , large/
for file in os.listdir(dir[:-1]):

    proba_dict = joint_entropy(0,dir+file) 

    codeword_dict = proba_dict
    list = []

    #Create the leafs from the dictionary
    for key in proba_dict:
        node = Nodes(proba_dict[key], key)
        list.append(node)


    list.sort(key=lambda p: p.probability)

    #Create all other nodes from the inital leafs, n leafs = n-1 parent nodes. 
    for x in range(0,len(list)+len(list)-2,2):

        node = Nodes(list[x].probability + list[x+1].probability, None, list[x], list[x+1])

        list.append(node)
        list.sort(key=lambda p: p.probability)


    #Traverse the huffman tree and get the codewords for each symbol
    res=""
    node.inorderTraversal(res) #This is the last node created, so the root node with probability 1


    #encode
    #read each symbol and write it as its' codeword
    with open(dir+file,"rb") as f , open("temp","w") as o:

        while True:
            char = f.read(1)
            if not char:
                break
            
            o.write(codeword_dict[char])

    #print(char)
    #print(codeword_dict[])


    #pad the file with 0 so that the number of bits are divisible by 8, after that read the file with 8bits at a time, convert the 8bit representation to an int and then
    #convert that to byte and write.
    with open("temp","r+") as o, open("compress/" + file + "_compressed","wb") as output: 

        bitstream = o.read()
        bitstream_len = len(bitstream)

        #pad with 0's
        pad = 0
        while bitstream_len%8 != 0:
            o.write("0")
            #print("pad")
            pad += 1
            bitstream_len += 1

        #Write another 8-bits to know how much padding was added, when decompressing read the last 8-bits and remove 8+pad
        o.write('{0:08b}'.format(pad))
                
        #Start reading 8bits at a time
        o.seek(0)
        byte_array = bytearray()
        while True:
            bits_8 = o.read(8)

            if not bits_8:
                break
            
            to_int = int(bits_8,2)
            byte_array.append(to_int)
        
        output.write(byte_array)



    #decode
    with open("compress/" + file + "_compressed","rb") as f , open("binary","w") as o:

        #read each byte, convert to binary and write to new file
        string = ""
        while True:
            char = f.read(1)
            if not char:
                break
            
            string += '{0:08b}'.format(int.from_bytes(char, "big"))
            #o.write('{0:08b}'.format(int.from_bytes(char, "big")))
        
        pad_num = int(string[-8:],2) + 8 #Total number of padding "the actual padding" + "8-bits for info about how much padding"
        
        string = string[:-pad_num]
        o.write(string)
        #o.write('{0:08b}'.format(int.from_bytes(char, "big")))


    node.decode_huffman(node,"binary")

