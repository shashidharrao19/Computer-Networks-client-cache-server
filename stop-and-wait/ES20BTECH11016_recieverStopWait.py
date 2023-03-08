import socket

recieverIP = "10.0.0.2"
recieverPort   = 20006
bufferSize  = 1024 #Message Buffer Size
senderAd = ("10.0.0.1", 20001)
r_time=0.5

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
s.bind((recieverIP, recieverPort))
ack = ['yes', 'no']

print("UDP socket created successfully....." )

file=input("name: ") 
f = open(file, "wb")

prev_ident=0

data2, addr2 = s.recvfrom(1024)
print(data2.decode())

bio=1

while(True):
    try:
    	s.settimeout(r_time)
    	data, addr= s.recvfrom(1024)
    	s1.sendto(ack[0].encode(), senderAd)
    	bio=1
    except socket.timeout:
    	s1.sendto(ack[1].encode(), senderAd)
    	bio=0
    	continue

    if(bio==1):
    	ident= int.from_bytes(data[:2], "big")
    	data_ac= data[2:-2]
    	flag = data[-1:]
    	print("ident: ", prev_ident)
    	print("recieve: ",int(ident))

    	if ident==prev_ident+1:
    		f.write(data_ac)
    		prev_ident=prev_ident+1
    	else:
    		continue

    	if flag==b'1':
	    	print('file receieved!')
	    	f.close()
	    	s.close()
	    	break
		