import os
import queue


file = "cantrbry/alice29.txt"

search_buffer_size = (2**11) #2**16
look_ahead_buffer_size = (2**7) #2**8


#buffer = queue.Queue(search_buffer_size + look_ahead_buffer_size)
#buffer = [None] * (search_buffer_size + look_ahead_buffer_size)

#print(file)

with open(file,"rb") as f:
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

#print(data_array)
#print(data[32])
codeword_array = []
search_index = 0
i = 0
print(len(data_array))
while i < len(data_array): #len(data_array):
    #print("hello this is run nummber : " + str(i))
    #look at symol on pos i, match it to symol to the left (so i - x), where x is capped at the size of the search buffer. (i+y) y = look-ahead size is the cap for lookahead buffer
    #data_array[i]


    #find  one symbol match
    match = ()
    best_match = ()
    l = 0
    j = search_index
    while j > 0:#for j in range(search_index,0,-1): #can I move j -l steps if match was found???
        #print(j)

        if data_array[i] == data_array[i-j]: #if match with ONE symbol is found

            l = 1
            best_match = (abs(i-j), l, data_array[i+1])
            #print("-------------------------------------------")
            #print(data_array[i])
            #print(data_array[i+l])
            #print(data_array[(i-j)+l])

            while data_array[i+l] == data_array[(i-j)+l]: #see how many symbols are matching after the first found symbol match
                
                #match = data_array[i:i+l]
                #print("hej")
                l += 1

            match = (abs(i-j), l, data_array[i+l+1]) # är o = abs(i-j)???? Kan behöva ta -1 till för att indexera på 0. (o,l,symbol), l = l-1 pga loopen
            #print(l)
            #print("-----------------------------")
            #print(match[1])
            #print(best_match[1])
            if match[1] > best_match[1]: # index 1 to compare the match length
                #print(match[1])
                #print(best_match[1])
                best_match = match
                #(o,l,data_array[i+l+1]) #är o abs av i-j ???

        if j == 1 and best_match == (): # if this is true then no matching symbol was found

            codeword_array.append((0,l,data_array[i]))
            #print("den e tom")
            #print((0,l,data_array[i]))
        elif j == 1:
            codeword_array.append(best_match)
            #print("vi hittade match")
            #if best_match[1] > 15:
                #print(best_match[1])

        j -= l+1

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
