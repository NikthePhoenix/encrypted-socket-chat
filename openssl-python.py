import subprocess

private_key = subprocess.run(["openssl", "genrsa", "-out", "private.pem", "2048"], capture_output=True, text=True)

public_key = subprocess.run(["openssl", "rsa", "-pubout", "-in", "private.pem", "-out", "public.pem"], capture_output=True, text=True)

with open("public.pem", "rb") as f:
    pubkey=f.read()

print(pubkey)

# message = input("Enter your message\n")

# with open("message.txt", "w") as f:
#     f.write(message)

# encrypted_message = subprocess.run(["openssl", "rsautl", "-encrypt", "-pubin", "-in", "message.txt", "-out", "encrypted_message.bin", "-inkey", "public.pem"],capture_output=True, text=True)

# with open("encrypted_message.bin", "rb") as f:
#     data = f.read()


# decrypted_message = subprocess.run(["openssl", "rsautl", "-decrypt", "-in", "encrypted_message.bin", "-out", "decrypted_message.txt", "-inkey", "private.pem"], capture_output=True, text=True)

nclients = 0

