import argparse
import json
from Crypto.Cipher import AES
from Crypto.Util.number import getStrongPrime
from Crypto.Random import get_random_bytes


def encrypt(message: bytes, num_squarings: int, prime_bits=1024):
    p = getStrongPrime(prime_bits)
    q = getStrongPrime(prime_bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    key = get_random_bytes(16)
    nonce = get_random_bytes(12)

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    encrypted_message = cipher.encrypt(message)

    a = 2

    key = int.from_bytes(key, 'big')

    e = pow(2, num_squarings, phi)
    b = pow(a, e, n)
    encrypted_key = key + b

    return {
        'n': n,
        'a': a,
        'num_squarings': num_squarings,
        'encrypted_key': encrypted_key,
        'nonce': nonce.hex(),
        'encrypted_message': encrypted_message.hex()
    }


def decrypt(message):
    n = message['n']
    a = message['a']
    num_squarings = message['num_squarings']
    encrypted_key = message['encrypted_key']
    nonce = bytes.fromhex(message['nonce'])
    encrypted_message = bytes.fromhex(message['encrypted_message'])

    for _ in range(num_squarings):
        a = pow(a, 2, n)

    key = encrypted_key - a
    key = key.to_bytes(16, 'big')

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    decrypted_message = cipher.decrypt(encrypted_message)

    return decrypted_message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['encrypt', 'decrypt'])
    parser.add_argument('file', type=argparse.FileType('rb'))
    parser.add_argument('--num-squarings', type=int, default=10 ** 6,
                        help='Number of squarings that should be required to decrypt the message. This is proportional to the time required to decrypt. This option is only relevant when encrypting.')
    args = parser.parse_args()

    if args.type == 'encrypt':
        message = args.file.read()
        encrypted_message = encrypt(message, args.num_squarings)
        print(json.dumps(encrypted_message))
    elif args.type == 'decrypt':
        encrypted_message = json.load(args.file)
        message = decrypt(encrypted_message)
        print(message)


if __name__ == '__main__':
    main()
