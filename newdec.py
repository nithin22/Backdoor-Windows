from cryptography.fernet import Fernet
import sys

with open('mykey.key', 'rb') as unlock:
     key = unlock.read()
     print(key)

f = Fernet(key)

with open(sys.argv[1], 'rb') as encrypted_file:
    encrypted = encrypted_file.read()

decrypted = f.decrypt(encrypted)

with open(sys.argv[1], 'wb') as decrypted_file:
    decrypted_file.write(decrypted)