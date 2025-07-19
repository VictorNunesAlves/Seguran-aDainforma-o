import hashlib
import random
import csv

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()-_+=<>?'
PASSWORD_LENGTH = 5
CHAIN_LENGTH = 10000
NUM_CHAINS = 100000

def generate_random_password():
    return ''.join(random.choices(ALPHABET, k=PASSWORD_LENGTH))


def sha512_hash(value):
    return hashlib.sha512(value.encode()).hexdigest()

def reduce_colorful(hash_value, position):
    reduced = ''
    offset = (position * 13) % (len(hash_value) - PASSWORD_LENGTH * 2)
    for i in range(PASSWORD_LENGTH):
        hex_pair = hash_value[offset + i * 2: offset + i * 2 + 2]
        num = int(hex_pair, 16)
        reduced += ALPHABET[num % len(ALPHABET)]
    return reduced


def generate_rainbow_table():
    with open('rainbow_table_colorida.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['start', 'end'])

        for chain_num in range(NUM_CHAINS):
            start = generate_random_password()
            current = start

            for pos in range(CHAIN_LENGTH):
                hashed = sha512_hash(current)
                current = reduce_colorful(hashed, pos)

            writer.writerow([start, current])

            if chain_num % 100 == 0:
                print(f'Gerado: {chain_num}/{NUM_CHAINS}')

    print("Tabela gerada com sucesso!")


generate_rainbow_table()
