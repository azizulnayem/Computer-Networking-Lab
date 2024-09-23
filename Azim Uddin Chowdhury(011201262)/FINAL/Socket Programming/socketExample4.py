import socket   #for sockets
import sys  #for exit
 
#create an AF_INET, STREAM socket (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 
print ('Socket Created\n')
 
dest_host = 'www.google.com'
dest_port = 80
 
try:
    dest_ip = socket.gethostbyname( dest_host )
 
except socket.gaierror:
    #could not resolve
    print ('Hostname could not be resolved. Exiting\n')
    sys.exit()
     
print ('Ip address of ' + dest_host + ' is ' + dest_ip+'\n')
 
#Connect to remote server
s.connect((dest_ip , dest_port))
 
print ('Socket Connected to ' + dest_host + ' on ip ' + dest_ip+'\n')


#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
 
try :
    #Set the whole string
    s.sendall(message.encode())
except socket.error:
    #Send failed
    print ('Send failed')
    sys.exit()
 
print ('Message sent successfully')

#==========New Code================================ 

#Now receive data
reply = s.recv(200)
 
print (reply)

#close the socket
s.close()
