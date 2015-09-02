from groups import *
from fields import *
import random
import hashlib

def hash(txt):
    m = hashlib.md5()
    m.update(txt)
    return m.digest()

def async_diffy_key(g,bits = 1024):
    a = random.randrange(10,2**bits)
    ga = g
    while ga == g:
        ga = g**a
    return {"private": a, "public": (g,ga)}


def async_diffy_encrypt(pubkey, msg):
    b = random.randrange(10,2**1024)
    g = pubkey[0]
    gb = g
    while gb == g:
        gb = g**b
    gab = pubkey[1]**b

    #very primitive hashing and encryption
    key = hash(str(gab))

    crypt = ""
    for i in range(len(msg)):
        crypt += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return (crypt,gb)


def async_diffy_decrypt(key, crypt):
    gb = crypt[1]
    crypt = crypt[0]
    gab = gb**key["private"]

    #very primitive hashing
    key = hash(str(gab))
    msg = ""
    for i in range(len(crypt)):
        msg += chr(ord(crypt[i]) ^ ord(key[i % len(key)]))
    return msg
    

