import socket
import time
import threading
import os

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20006)
bufferSize  = 1024 #Message Buffer Size
r_time=1
window=256

# Create a UDP socket at reciever side
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

s1.bind((senderIP, senderPort))

f=open('/home/p4/assi2/testFile.jpg', "rb")

size=os.path.getsize('/home/p4/assi2/testFile.jpg')

lis=[]
list_send=[]
data = f.read(1005)

s.sendto('startsending'.encode(), recieverAddressPort)

while(data):
    lis.append(data)
    data=f.read(1005)

for i in range(len(lis)):
    num=i+1
    data1 = num.to_bytes(2, byteorder="big") + lis[i] +' 0'.encode()
    if i==len(lis)-1:
        data1= data1[:-2] +' 1'.encode()

    list_send.append(data1)

def send_window(a, b,k):
    for i in range(a, b+1):
        s.sendto(list_send[i], recieverAddressPort)
        print('sending! ', i, k)


def repit(a, b, i):

    thr = threading.Thread(target=send_window, args=(a,b,i,))
    thr.start()
    thr.join()

    for j in range(a, b+1):
        try:
            s1.settimeout(r_time)
            ack, addr2 = s1.recvfrom(1024)
            print(ack, j)
        except:
            print('no ack recieved')
            ack='--'
        
        if ack==b'no' or ack=='--':
            print(ack,j)
            print('re-sending!')
            repit(a,b, i) 

start=time.time()
for i in range(len(list_send)//window + 1):
    print('sending batch: ', i)
    if i==len(list_send)//window and len(list_send)%window>0:
        a=i*window
        b=len(list_send)-1

    elif len(list_send)%window==0 and i==len(list_send)//window:
        break
    else:
        a=window*i
        b=a+window-1

    repit(a,b,i)
end=time.time()
print(size/(end-start)/1024)    

f.close()
s.close()