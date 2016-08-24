import socket
import os


host = '172.24.49.130'

if os.name == "nt":
    socket_protocal = socket.IPPROTO_IP
else:
    socket_protocal = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocal)
sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
    
print sniffer.recvfrom(65535)

if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
