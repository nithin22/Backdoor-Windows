import warnings 
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
from cryptography.fernet import Fernet
import sys
#generate the key
# key generation
key = Fernet.generate_key()

with open('mykey.key', 'wb') as mykey:
    mykey.write(key)

with open('mykey.key', 'rb') as mykey:
    key = mykey.read()

# print(key)

f = Fernet(key)

with open('SystemInfo.txt', 'rb') as original_file:
    original = original_file.read()

encrypted = f.encrypt(original)

with open ('SystemInfo.txt', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

print("DONE")