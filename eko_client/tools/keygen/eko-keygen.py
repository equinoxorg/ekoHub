import os.path

from Crypto.PublicKey import RSA

from datetime import datetime
import time

import os

import sys

def load_RSA(keypath):
    f = open(keypath, 'r')
    try:
        k = RSA.importKey(f.read())
    except (ValueError, IndexError, TypeError):
        print("Problem importing specified key, delete and recreate please!")
        exit(-1)
    f.close()
    return(k)

def generate_RSA(prikeypath):
    fh = open(prikeypath, 'w')
    
    key = RSA.generate(1024)
    fh.write(key.exportKey('PEM'))
    
    fh.close()

    print('Wrote Private Key to %s' % prikeypath)
    return key

def write_pubkey(key, pubkeypath):
    fh2 = open(pubkeypath, 'w')
    fh2.write(key.publickey().exportKey('PEM'))
    fh2.close()

    print('Wrote Public Key to %s' % pubkeypath)
    print('*'*5 + 'Copy below this line' + '*'*5)
    print(key.publickey().exportKey('PEM'))
    print('*'*5 + 'Copy above this line' + '*'*5)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print ('eko-keygen.py CONFIGPATH')
        exit(-1)
    # Check if RSA Key exists
    configpath = sys.argv[1]
    prikeypath = os.path.join(configpath, 'privatekey.pem')
    pubkeypath = os.path.join(configpath, 'pubkey.pem')
    if (os.path.exists(prikeypath)):
        # load key
        key = load_RSA(prikeypath)
        write_pubkey(key, pubkeypath)
    else:
        # generate key
        key = generate_RSA(prikeypath)
        write_pubkey(key, pubkeypath)

    exit(0)