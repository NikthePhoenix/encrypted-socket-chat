# Import socket module
import socket
import subprocess               

# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 12345               

def encrypt_message(s):
    with open("message.txt", "w") as f:
        f.write(s)
    encrypted_message = subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-in", "message.txt", "-out", "encrypted_message.bin", "-inkey", "public.pem"],capture_output=True, text=True)

    with open("encrypted_message.bin", "rb") as f:
        data = f.read()
    return data

# connect to the server on local computer
s.connect(('127.0.0.1', port))

#receive public key
spubkey=s.recv(2048)
with open("spublic.pem", "wb") as f:
    f.write(spubkey)
# Send data to server 'Hello world'

## s.sendall('Hello World')

input_string = input("Enter data you want to send->")
encrypted = encrypt_message(input_string)

s.sendall(bytes(encrypted))

# receive data from the server
print(s.recv(1024).decode())

# close the connection
s.close()
