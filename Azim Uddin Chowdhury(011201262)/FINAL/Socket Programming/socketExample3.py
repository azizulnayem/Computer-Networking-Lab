import socket   #for sockets
import sys  #for exit
 
#create an AF_INET, STREAM socket (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ('Socket Created')
 
dest_host = 'www.google.com'
dest_port = 80
 
try:
    dest_ip = socket.gethostbyname( dest_host )
 
except socket.gaierror:
    #could not resolve
    print ('Hostname could not be resolved. Exiting')
    sys.exit()
     
print ('Ip address of ' + dest_host + ' is ' + dest_ip)
 
#Connect to remote server
s.connect((dest_ip , dest_port))
 
print ('Socket Connected to ' + dest_host + ' on ip ' + dest_ip)

#============New Code===============================================

#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
 
try :
    #Send the whole string
    s.sendall(message.encode())
except socket.error:
    #Send failed
    print ('Sending failed')
    sys.exit()
 
print ('Message sent successfully')
