import tkinter as tk
import socket
import threading
import subprocess

global ss
global s, ipa, rport
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rport = 12346
# E2EE encryption/decryption functions
def encrypt_message(s):
    print("entered encrypt_message with message "+ s)
    with open("message.txt", "w") as f:
        f.write(s)
        f.close()
    encrypted_message = subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-in", "message.txt", "-out", "encrypted_message.bin", "-inkey", "spublic.pem"],capture_output=True, text=True)

    with open("encrypted_message.bin", "rb") as f:
        data = f.read()
        f.close()
    print("leaving encrypt_message()")
    return data

def decrypt_message(data):
    with open("encrypted.bin", "wb") as f:
        f.write(data)
        f.close()
    decrypted_message = subprocess.run(["openssl", "rsautl", "-decrypt", "-in", "encrypted.bin", "-out", "decrypted.txt", "-inkey", "mprivate.pem"], capture_output=True, text=True)
    with open("decrypted.txt", "r") as f:
        output=f.read(4096)
        f.close()
    print("leaving decrypt message with output "+output)
    return output


# Handshake functions

def await_handshake():
    s = socket.socket()
    global ss
    port = 12346

    s.bind(('',port))
    print("socket binded to ", port)
    s.listen(5)
    print("socket awaiting handshake... ")

    got_handshake = False

    while not got_handshake:
        c, addr = s.accept()
        ss = c
        print('Received handshake request from ', addr) 
        got_handshake = True

    print("confirming handshake")
    confirm_handshake(c)

def confirm_handshake(c):

    spubkey=c.recv(2048)
    with open("spublic.pem", "wb") as f:
        f.write(spubkey)
        f.close()

    private_key = subprocess.run(["openssl", "genrsa", "-out", "mprivate.pem", "2048"], capture_output=True, text=True)
    public_key = subprocess.run(["openssl", "rsa", "-pubout", "-in", "mprivate.pem", "-out", "mpublic.pem"], capture_output=True, text=True)

    with open("mpublic.pem", "rb") as f:
        data = f.read()
   
    c.sendall(data)

    print("handshake confirmed")

    receive_thread = threading.Thread(target=receive_messages, args=[c])
    receive_thread.start()
    receiver_ip_entry.config(state=tk.DISABLED)
    receiver_ip_button.config(state=tk.DISABLED)
    message_entry.config(state=tk.NORMAL)
    send_button.config(state=tk.NORMAL)
    
def initiate_handshake(ip_address):
    print("handshake initiated")
    s = socket.socket()
    global ss

    rport = 12346

    s.connect((ip_address, rport))
    ss = s
    private_key = subprocess.run(["openssl", "genrsa", "-out", "mprivate.pem", "2048"], capture_output=True, text=True)
    public_key = subprocess.run(["openssl", "rsa", "-pubout", "-in", "mprivate.pem", "-out", "mpublic.pem"], capture_output=True, text=True)

    with open("mpublic.pem", "rb") as f:
        data = f.read()
        f.close()

    s.sendall(data)
    print("sent public key")

    spubkey = s.recv(2048)
    with open("spublic.pem", "wb") as f:
        f.write(spubkey)
        f.close()

    print("handshake initiate successful")

# Thread to handle incoming messages
def receive_messages(s):
    while True:
        print("awaiting messages")
        data = s.recv(4096)
        if(data):
            print("message received")
            decrypted_message = decrypt_message(data)
            messages.insert(tk.END, f"Received: {decrypted_message}")
            messages.see(tk.END)

# Function to send messages
def send_message():
    global ss
    message = message_entry.get()
    print("Message: "+ message)
    if message:
        encrypted_message = encrypt_message(message)
        ss.sendall(encrypted_message)
        messages.insert(tk.END, f"Sent: {message}")
        messages.see(tk.END)
        message_entry.delete(0, tk.END)

# Connect function
def connect(receiver_ip):
    global s, ipa, ss
    ipa=receiver_ip
    initiate_handshake(receiver_ip)
    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=[ss])
    receive_thread.start()
    receiver_ip_entry.config(state=tk.DISABLED)
    receiver_ip_button.config(state=tk.DISABLED)
    message_entry.config(state=tk.NORMAL)
    send_button.config(state=tk.NORMAL)

# Main window
window = tk.Tk()
window.title("c1")

# Receiver IP entry
receiver_ip_label = tk.Label(window, text="Enter Receiver's IP Address:")
receiver_ip_label.pack()
receiver_ip_entry = tk.Entry(window)
receiver_ip_entry.pack()
receiver_ip_button = tk.Button(window, text="Connect", command=lambda: connect(receiver_ip_entry.get()))
receiver_ip_button.pack()
ipa = receiver_ip_entry.get()

# Message window
messages_frame = tk.Frame(window)
messages_frame.pack(fill=tk.BOTH, expand=True)
messages_scrollbar = tk.Scrollbar(messages_frame, orient=tk.VERTICAL)
messages = tk.Listbox(messages_frame, yscrollcommand=messages_scrollbar.set)
messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
messages_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def testfunc():
    print("test func fired")

# Message entry
message_entry = tk.Entry(window)
message_entry.pack()
send_button = tk.Button(window, text="Send", command=send_message,)
send_button.pack() 

hand_thread = threading.Thread(target=await_handshake)
hand_thread.start()
window.mainloop()