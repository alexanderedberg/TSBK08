import os
import queue


file = "cantrbry/alice29.txt"

search_buffer_size = (2**16)
look_ahead_buffer_size = (2**8)


#buffer = queue.Queue(search_buffer_size + look_ahead_buffer_size)
buffer = [None] * (search_buffer_size + look_ahead_buffer_size)

#print(file)

with open(file,"rb") as f:
    #data = f.read() #bytearray(f.read())

    data_array = []
    #i = 0
    while True:
        char = f.read(1)
        #print("yeet")
        data_array.append(char)
        #i += 1
        #print("hello")
        if not char:
            break

    #print(data_array[::-1])    
    #fill look-ahead buffer

    buffer[0:look_ahead_buffer_size] = data_array[0:look_ahead_buffer_size][::-1]

    


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

print(data_array[0:11])
print(buffer[245:256])
