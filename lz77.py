import os
import time
import math
from collections import Counter

start_time = time.time()
#dir = "cantrbry/"
#file = "alice29.txt" #alice29.txt #xargs.1

search_buffer_size = (2**10) #2**16 #2**15
look_ahead_buffer_size = (2**6) #2**8 #2**7



dir = "large/" #cantrbry/ , large/
#file= "asyoulik.txt"
for file in os.listdir(dir[:-1]): #dir[:-1]


    with open(dir+file,"rb") as f:

        data_array = []
        
        while True:
            char = f.read(1)
            
            if not char:
                break

            data_array.append(char)


    tuple_array = []
    search_index = 0
    i = 0

    print(len(data_array))
    print(data_array[0:5])

    while i < len(data_array):

        search_buffer = data_array[max(0,i-search_buffer_size):i]
        look_ahead_buffer = data_array[i:i+look_ahead_buffer_size]

        match_buffer = data_array[max(0,i-search_buffer_size):i+look_ahead_buffer_size]

        l = 0
        o = 0
        best_match = (0,l,look_ahead_buffer[0])

        #Go through the search buffer from right to left
        for search_index in range (len(search_buffer)-1,-1,-1):

            #if symbols in search and look ahead buffer match, see for how long they match, 
            #but only up until the size of the look ahead buffer.
            while match_buffer[search_index+l] == look_ahead_buffer[l]:
                l += 1
                
                if l == max(1,(len(look_ahead_buffer)-2)):

                    break
                

                try:
                    if match_buffer[search_index+l] == look_ahead_buffer[l]:
                        pass
                except IndexError:

                    if l == max(1,(len(look_ahead_buffer)-2)):
                        
                        break

            #check if the match length l is larger than the current best match length
            if l >= best_match[1]:

                try:
                    best_match = (o,l,look_ahead_buffer[l])
                except IndexError:
                    best_match = (o,0,look_ahead_buffer[l-1])
            o += 1
            l = 0

        tuple_array.append(best_match)
        i += best_match[1] + 1


    #print(tuple_array[0:5])
    end_time = time.time()
    print(end_time-start_time)


    #bits required
    search_buffer_bits = int(math.log2(search_buffer_size))
    look_ahead_buffer_bits = int(math.log2(look_ahead_buffer_size))


    alphabet_bits = math.ceil(math.log2(len(set(data_array))))


    #Create dict with all of the symbols in alphabet
    codeword_dict = Counter(data_array)


    #Give each symbol in alphabet its own codeword
    count = 0
    for key in codeword_dict:
        codeword_dict[key] = count
        count += 1

    #Write the tuples in binary to text file.
    with open("temp","w") as o:

        for i in tuple_array:

            o.write(f'{i[0]:0{search_buffer_bits}b}' + f'{i[1]:0{look_ahead_buffer_bits}b}' + f'{codeword_dict[i[2]]:0{alphabet_bits}b}')

    #pad the file with 0 so that the number of bits are divisible by 8, after that read the file with 8bits at a time, convert the 8bit representation to an int and then
    #convert that to byte and write.
    with open("temp","r+") as o, open("compress_lz77/" + file + "_compressed","wb") as output: 

        bitstream = o.read()
        bitstream_len = len(bitstream)

        #pad with 0's
        pad = 0
        while bitstream_len%8 != 0:
            o.write("0")
            #print("pad")
            pad += 1
            bitstream_len += 1

        #Write another 8-bits to know how much padding was added, when decompressing read the last 8-bits and remove 8+pad bits
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


    ####
    #### decode
    ####


    #Start with going from bytes back to binary
    with open("compress_lz77/" + file + "_compressed","rb") as f , open("binary","w") as o:

        #read each byte, convert to binary and write to new file
        string = ""
        while True:
            char = f.read(1)
            if not char:
                break
                
            string += '{0:08b}'.format(int.from_bytes(char, "big"))
            
        pad_num = int(string[-8:],2) + 8 #Total number of padding "the actual padding" + "8-bits for info about how much padding"
            
        string = string[:-pad_num]
        o.write(string)


    #From binary to tuples

    key_list = list(codeword_dict.keys())
    val_list = list(codeword_dict.values())
    #print(codeword_dict)
    #print(val_list[0:5])

    tuple_array_decode = []

    with open("binary","r") as f:

        while True:
            offset_bin = f.read(search_buffer_bits)
            if not offset_bin:
                break
            
            offset = int(offset_bin,2)
            length = int(f.read(look_ahead_buffer_bits),2)
            dict_index = val_list.index(int(f.read(alphabet_bits),2))
            char = key_list[dict_index]

            tuple_array_decode.append((offset, length, char))

    #print(tuple_array[0:20])
    #print(tuple_array_decode[-5:])


    #decode array of tuples back to original file
    with open("decompress_lz77/" + file + "_decompressed","ab+") as o:


        for tuple in tuple_array_decode:

            if tuple[1] == 0:

                o.write(tuple[2])
                

            else:
                
                o.seek(-(tuple[0]+1),2)

                for i in range(1,tuple[1]+1):
                
                    read = o.read(1)
                    #print(read)
                    o.write(read)
                    o.seek(-(tuple[0]+1),2)


                o.write(tuple[2])


    print("File: " + file)
    print("Original: " + str(os.path.getsize(dir+file)) + " bytes")
    print("Compressed: " + str(os.path.getsize("compress/" + file + "_compressed")) + " bytes")
    ratio = os.path.getsize("compress/" + file + "_compressed")/os.path.getsize(dir+file)
    print("Compression ratio: " + str(ratio))
    print("-----------------------------------------------------------------------------------------")