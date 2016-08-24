import socket
import os
import struct
from ctypes import *


host = '172.24.49.130'

class IP(Structure):
    _fields_ = [
        ("ih1",                c_ubyte,4),
        ("version",            c_ubyte,4),
        ("tos",                c_ubyte),
        ("len",                c_ushort),
        ("id",                 c_ushort),
        ("offset",             c_ushort),
        ("ttl",                c_ubyte),
        ("protocol_num",       c_ubyte),
        ("sum",                c_ushort),
        ("src",                c_ulong),
        ("dst",                c_ulong)
    ]
    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self,socket_buffer=None):
        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dsc_address = socket.inet_ntoa(struct.pack("<L",self.dsc))
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
            
            
if os.name == "nt":
    socket_protocal = socket.IPPROTO_IP
else:
    socket_protocal = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocal)
sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
    
try:
    while True:
        raw_buffer = sniffer.recvfrom(65535)[0]
        ip_header = IP(raw_buffer[0:20])
        print "Protocol: %s %s -> %s" % (ip_header.protocol,ip_header.src_address,ip_header.dst_address)
        
     
except KeyboardInterrupt:

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
