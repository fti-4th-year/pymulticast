import socket
import struct
from threading import Thread
import sys
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

membership = struct.pack( "4sl" , socket.inet_aton( MCAST_GRP ) , socket.INADDR_ANY )
sock = socket.socket( socket.AF_INET , socket.SOCK_DGRAM , socket.IPPROTO_UDP )
sock.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
sock.setsockopt( socket.IPPROTO_IP , socket.IP_ADD_MEMBERSHIP , membership )
#sock.setsockopt( socket.IPPROTO_IP , socket.IP_MULTICAST_TTL , 2 )
sock.bind( ( '0.0.0.0' , MCAST_PORT ) )
sock.settimeout( 0.1 )

working = True
def recieve():
	global working
	while working:
		try:
			msg =  sock.recv( 10240 )
			print "message recieved:" , msg
		except Exception:
			continue

if __name__ == "__main__":
	try:
		thread = Thread( target = recieve )
		thread.start()
		while True:
			msg = raw_input()
			sock.sendto( msg , ( MCAST_GRP , MCAST_PORT ) )
	except KeyboardInterrupt:
		working = False
		thread.join()
		exit()
