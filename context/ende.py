import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import string
import random

def get_random_password_string(length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(length))
    return password

#Encryption of files
def encrypt(key, filename):
    chunksize =64 * 1024
    outputFile = filename + "e"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk +=b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

#Decryption of files
def decrypt(key, filename):
    chunksize =64 * 1024
    outputFile = filename+'e'

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def Main():
    # choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")
    # if choice == 'E' or choice == 'e':
    #     filename = input("File to encrypt: ")
    #     password = input("Password: ")
    #     encrypt(getKey(password), filename)
    #     print("Done.")
    # elif choice == 'D' or choice == 'd':
    #     filename = input("File to decrypt: ")
    #     password = input("Password: ")
    #     decrypt(getKey(password), filename)
    #     print("Done.")
    # else:
    #     print("No Option selected, closing…")
    encryptmain()

def encryptmains(reslist):
    finalkey = dict()
    k = 0
    for i in reslist:
        password = get_random_password_string(10)
        encrypt(getKey(password),"uploads/"+i)
        finalkey[i] = [password,k]
        k += 1
        os.remove("uploads/"+i)
        os.rename("uploads/"+i+"e","uploads/"+i)
        
    return finalkey

def decryptmains(key):
    k = os.listdir('uploads')
    for i in k:
        password = key[i][0]
        decrypt(getKey(password),"uploads/"+i)
        os.remove("uploads/"+i)
        os.rename("uploads/"+i+"e","uploads/"+i)
    
if __name__ == '__main__':
    Main()
