# first of all import the socket library
import socket               
import subprocess

# private_key = subprocess.run(["openssl", "genrsa", "-out", "private.pem", "2048"], capture_output=True, text=True)

# public_key = subprocess.run(["openssl", "rsa", "-pubout", "-in", "private.pem", "-out", "public.pem"], capture_output=True, text=True)

# message = input("Enter your message\n")

# with open("message.txt", "w") as f:
#     f.write(message)

# encrypted_message = subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-in", "message.txt", "-out", "encrypted_message.bin", "-inkey", "public.pem"],capture_output=True, text=True)

# with open("encrypted_message.bin", "rb") as f:
#     data = f.read()

# decrypted_message = subprocess.run(["openssl", "rsautl", "-decrypt", "-in", "encrypted_message.bin", "-out", "decrypted_message.txt", "-inkey", "private.pem"], capture_output=True, text=True)


def genhandshake(c):
   private_key = subprocess.run(["openssl", "genrsa", "-out", "mprivate.pem", "2048"], capture_output=True, text=True)
   public_key = subprocess.run(["openssl", "rsa", "-pubout", "-in", "mprivate.pem", "-out", "mpublic.pem"], capture_output=True, text=True)

   with open("mpublic.pem", "rb") as f:
      data = f.read()
   
   c.sendall(data)

def decrypt_message(data):
   with open("encrypted.bin", "wb") as f:
      f.write(data)
      f.close()
   decrypted_message = subprocess.run(["openssl", "rsautl", "-decrypt", "-in", "encrypted.bin", "-out", "decrypted.txt", "-inkey", "private.pem"], capture_output=True, text=True)
   with open("decrypted.txt", "r") as f:
      output=f.read(4096)
   return output

# next create a socket object
s = socket.socket()         
print("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('', port))        
print("socket binded to",port)
 
# put the socket into listening mode
s.listen(5)     
print("socket is listening")
 
# a forever loop until we interrupt it or 
# an error occurs
while True:
 
   # Establish connection with client.
   c, addr = s.accept()     
   print('Got connection from', addr)

   genhandshake(c=c)

   # Get data from client
   data=c.recv(4096)
   print(decrypt_message(data=data))
 
   

   if not data:
      break
   
   # Send back reversed data to client   
   # c.sendall(bytes(data,'utf-8'))


   # send a thank you message to the client. 
   #c.send('\n Thank you for sending message!!!!')
 
   # Close the connection with the client
   c.close()
