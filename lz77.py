import os
#import queue
import time
import math
from collections import Counter

start_time = time.time()
dir = "cantrbry/"
file = "alice29.txt" #alice29.txt #xargs.1

search_buffer_size = (2**10) #2**16 #2**15
look_ahead_buffer_size = (2**6) #2**8 #2**7


#print(file)

with open(dir+file,"rb") as f:
    #data = f.read() #bytearray(f.read())

    data_array = []
    #i = 0
    while True:
        char = f.read(1)
        #print("yeet")
        #data_array.append(char)
        #i += 1
        #print("hello")
        if not char:
            break

        data_array.append(char)


tuple_array = []
search_index = 0
i = 0

print(len(data_array))
print(data_array[0:5])

while i < len(data_array): #len(data_array):
    #print("hello this is run nummber : " + str(i))
    #look at symol on pos i, match it to symol to the left (so i - x), where x is capped at the size of the search buffer. (i+y) y = look-ahead size is the cap for lookahead buffer
    #data_array[i]

    search_buffer = data_array[max(0,i-search_buffer_size):i]
    look_ahead_buffer = data_array[i:i+look_ahead_buffer_size]

    match_buffer = data_array[max(0,i-search_buffer_size):i+look_ahead_buffer_size]


    #find  one symbol match
    #match = ()
    l = 0
    o = 0
    best_match = (0,l,look_ahead_buffer[0])

    #print("i: " + str(i))
    #Go through the search buffer from right to left
    for search_index in range (len(search_buffer)-1,-1,-1): #data_array[]

        #print("Search index: " + str(search_index))
        #if symbols in search and look ahead buffer match, see for how long they match, 
        #but only up until the size of the look ahead buffer.
        while match_buffer[search_index+l] == look_ahead_buffer[l]:
            l += 1
            #lägg till if sats, IF len(look_ahead_buffer) == 1, hur hanterar vi det? sätt l=0?
            if l == max(1,(len(look_ahead_buffer)-2)): #len(look_ahead_buffer)-2: #Behöver jag ta len() här?????, blir det verklingen rätt med max?
                #print("WE BREAK")
                break
            #print("While is true, l = " + str(l))

            try:
                if match_buffer[search_index+l] == look_ahead_buffer[l]:
                    pass
            except IndexError:

                #print(max(1,(len(look_ahead_buffer)-2)))
                if l == max(1,(len(look_ahead_buffer)-2)): #Behöver jag ta len() här?????
                    #print("WE BREAK")
                    break
                #print("While is true, l = qqqq" + str(l))

                #print(look_ahead_buffer)
                #print(len(look_ahead_buffer))

            #IF i+l == len(data_array): , kommer inte detta alltid att bli sant tillslut?
#Ska l vara (l-1)???, nej tror inte det.
        #check if the match length l is larger than the current best match length
        if l >= best_match[1]:

            #print("IF is true, l is: " + str(l) + " ,best_match is : " + str(best_match))
            #print(look_ahead_buffer)
            try:
                best_match = (o,l,look_ahead_buffer[l]) #detta blir fel?? ska nog vara look_ahead_buffer[l+1], nej det blir nog rätt
            except IndexError:
                best_match = (o,l,look_ahead_buffer[l-1]) ## vad ska l vara???
        o += 1
        l = 0

    tuple_array.append(best_match)
    i += best_match[1] + 1

    #print(i)

#print(tuple_array[0:5])
end_time = time.time()
print(end_time-start_time)

    ####################################################################


#bits required
#
search_buffer_bits = int(math.log2(search_buffer_size))
look_ahead_buffer_bits = int(math.log2(look_ahead_buffer_size))

#code_test = tuple_array[0:10]

alphabet_bits = math.ceil(math.log2(len(set(data_array))))

#print(search_buffer_bits)
#print(look_ahead_buffer_bits)
#print(code_test)
#print(alphabet_bits)

#print(code_test)

#Create dict with all of the symbols in alphabet
codeword_dict = Counter(data_array)
#print(len(codeword_dict))

#Give each symbol in alphabet its own codeword
count = 0
for key in codeword_dict:
    codeword_dict[key] = count
    count += 1

#Write the tuples in binary to text file.
with open("temp","w") as o:

    for i in tuple_array: #tuple_array
        #print(f'{i[0]:0{search_buffer_bits}b}')
        #print(f'{i[1]:0{look_ahead_buffer_bits}b}')
        #print(f'{codeword_dict[i[2]]:0{alphabet_bits}b}')

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

#
#decode
#


#Start with going from bytes back to binary
with open("compress_lz77/" + file + "_compressed","rb") as f , open("binary","w") as o:

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
        
        #print("HELLLLOOO")
        offset = int(offset_bin,2)
        length = int(f.read(look_ahead_buffer_bits),2)
        #char = f.read(alphabet_bits)
        dict_index = val_list.index(int(f.read(alphabet_bits),2))
        char = key_list[dict_index]

        tuple_array_decode.append((offset, length, char))

#print(tuple_array[0:20])
print(tuple_array_decode[0:20])



with open("decompress_lz77/" + file + "_decompressed","ab+") as o:


    for tuple in tuple_array_decode:

        if tuple[1] == 0:

            o.write(tuple[2])
            

        else:
            
            o.seek(-(tuple[0]+1),2)

            for i in range(1,tuple[1]+1):

                
                read = o.read(1)

                #read = o.read(1)
                #print(str(read) + " " +str(i))

                #print(read)
                o.write(read)
                o.seek(-(tuple[0]+1),2)




            #print(test)


            #o.write(tuple[2])
            #tuple[1]
            #tuple[2]
            #print(tuple[0])
            #o.seek(0,2)
            o.write(tuple[2])  #o.write(test + tuple[2]) 


    



"""
    while search_index > 0:#for j in range(search_index,0,-1): #can I move j -l steps if match was found???
        #print(j)

        if data_array[i] == data_array[i-search_index]: #if match with ONE symbol is found

            l = 1
            best_match = (abs(i-search_index), l, data_array[i+1])
            #print("-------------------------------------------")
            #print(data_array[i])
            #print(data_array[i+l])
            #print(data_array[(i-j)+l])

            while data_array[i+l] == data_array[(i-search_index)+l]: #see how many symbols are matching after the first found symbol match
                
                #match = data_array[i:i+l]
                #print("hej")
                l += 1

            match = (abs(i-search_index), l, data_array[i+l+1]) # är o = abs(i-j)???? Kan behöva ta -1 till för att indexera på 0. (o,l,symbol), l = l-1 pga loopen
            #print(l)
            #print("-----------------------------")
            #print(match[1])
            #print(best_match[1])
            if match[1] > best_match[1]: # index 1 to compare the match length
                #print(match[1])
                #print(best_match[1])
                best_match = match
                #(o,l,data_array[i+l+1]) #är o abs av i-j ???

        if search_index == 1 and best_match == (): # if this is true then no matching symbol was found

            codeword_array.append((0,l,data_array[i]))
            #print("den e tom")
            #print((0,l,data_array[i]))
        elif search_index == 1:
            codeword_array.append(best_match)
            #print("vi hittade match")
            #if best_match[1] > 15:
                #print(best_match[1])

        search_index -= l+1

        #UPDATE SEARCH INDEX WHERE??? searcg_index = l, ty allt kommer med i loopen


        #data_array[]

    search_index += l+1

    if search_index > search_buffer_size:
        search_index = search_buffer_size

    #print(search_index)

    #if #matched symbols is 0, i += 1

    #else # i = matched symbols (l) + 1
    i += l+1

#print(codeword_array)
#fill look-ahead buffer

#for i in range (0,look_ahead_buffer_size):

#    buffer.put(data_array[i])




#buffer[0:look_ahead_buffer_size-1] = data_array[0:look_ahead_buffer_size-1][::-1]

#print(data_array[0:10])
#print(buffer[245:256])

#print(buffer.queue[0])
#print(buffer.get())
#print(buffer.queue)
#data_array_index = look_ahead_buffer_size-1



#print(buffer[245:256])

#while index < len(data_array): #kanske =

    

    


        #for i in range (0,look_ahead_buffer_size):
        #if 
        #    buffer.put(char)
        #    print()


        #print(buffer)    

    #for i in range (0, len(byte_array)):
        #char = f.read(1)
        #print(i)
        

        #if i <= look_ahead_buffer_size:
            #buffer.put(char)
            #buffer.get()

        

    #print(buffer.get())
    #
    
    #print(byte_array[32])
"""