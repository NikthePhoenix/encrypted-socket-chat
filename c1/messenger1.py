import socket 
import subprocess
import threading

def encrypt_message(s):
    with open("message.txt", "w") as f:
        f.write(s)
        f.close()
    encrypted_message = subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-in", "message.txt", "-out", "encrypted_message.bin", "-inkey", "public.pem"],capture_output=True, text=True)

    with open("encrypted_message.bin", "rb") as f:
        data = f.read()
        f.close()
    return data

def decrypt_message(data):
    with open("encrypted.bin", "wb") as f:
        f.write(data)
        f.close()
    decrypted_message = subprocess.run(["openssl", "rsautl", "-decrypt", "-in", "encrypted.bin", "-out", "decrypted.txt", "-inkey", "private.pem"], capture_output=True, text=True)
    with open("decrypted.txt", "r") as f:
        output=f.read(4096)
        f.close()
    return output

def genhandshake(c):
    private_key = subprocess.run(["openssl", "genrsa", "-out", "mprivate.pem", "2048"], capture_output=True, text=True)
    public_key = subprocess.run(["openssl", "rsa", "-pubout", "-in", "mprivate.pem", "-out", "mpublic.pem"], capture_output=True, text=True)

    with open("mpublic.pem", "rb") as f:
        data = f.read()
   
    c.sendall(data)

def receiver():
    s = socket.socket() 
    port = 12346     

    s.bind(('', port))        
    print("socket binded to",port)

    s.listen(5)     
    print("socket is listening")
 
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

    c.close()

def sender():
    s = socket.socket()   

    port = 12345

    s.connect(('127.0.0.1', port))

    spubkey=s.recv(2048)
    with open("spublic.pem", "wb") as f:
        f.write(spubkey)
        f.close()

    input_string = input("Enter data you want to send->")
    encrypted = encrypt_message(input_string)

    s.sendall(bytes(encrypted))

    s.close()

sender_t = threading.Thread(target=sender)
receiver_t = threading.Thread(target=receiver)

sender_t.start()
receiver_t.start()
