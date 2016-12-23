from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from app import app

key = app.config['URL_KEY']
key = b''.join(key)

def encrypt(text):

    iv = Random.new().read(AES.block_size)

    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(b''.join(text))

    return msg.encode('hex')

def decrypt(cypher_text):

    try:

        enc_msg = cypher_text.decode('hex')
        iv = enc_msg[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CFB, iv)

        dec_msg = cipher.decrypt(enc_msg)

    except Exception:
        return 'invalid'

    return dec_msg[AES.block_size:]

# msg = encrypt('10301681000181')
# print msg
# print decrypt(msg)
