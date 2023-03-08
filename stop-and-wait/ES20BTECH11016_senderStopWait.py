import socket
import time

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20006)
bufferSize  = 1024 #Message Buffer Size
r_time=0.5

# Create a UDP socket at reciever side
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

s1.bind((senderIP, senderPort))

f=open('/home/p4/assi2/testFile.jpg', "rb")

lis=[]
num=1
data = f.read(1005)

s.sendto('startsending'.encode(), recieverAddressPort)

while(data):
    lis.append(data)
    data=f.read(1005)

for i in range(len(lis)):
    data1= num.to_bytes(2, byteorder="big") + lis[i] +' 0'.encode()
    if i==len(lis)-1:
        data1= data1[:-2] +' 1'.encode()

        
    s.sendto(data1, recieverAddressPort)
    print('sending! ', num)


    try:
        s1.settimeout(r_time)
        ack, addr2 = s1.recvfrom(1024)
        print(ack)
    except:
        print('no ack recieved')
        ack='--'
    
    while(ack==b'no' or ack=='--'):
        print(ack)
        print('re-sending! ', num)
        s.sendto(data1, recieverAddressPort) 
        try:
            s1.settimeout(r_time)
            ack, addr2 = s1.recvfrom(1024)
            print(ack)
        except:
            print('no ack recieved')
            ack='--'    

    num+=1

f.close()
s.close()