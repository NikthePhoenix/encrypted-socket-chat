# Steps to generate public and private keys and encrypt/decrypt messages

generate private key

```openssl genrsa -out private.pem 2048```

generate public key

```openssl rsa -pubout -in private.pem -out public.pem```

encrypting message using public key

```openssl rsautl -encrypt -pubin -in message.txt -out encrypted_message.bin -inkey public.pem``` 

decrypting encrypted file using private key

```openssl rsautl -decrypt -in encrypted_message.bin -out decrypted_message.txt -inkey private.pem```
