import hashlib
import random
import csv

# Alfabeto de 70 caracteres (a-z, A-Z, 0-9 e símbolos)
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()-_+=<>?'
PASSWORD_LENGTH = 5
CHAIN_LENGTH = 10000
NUM_CHAINS = 100000

# Gera uma senha inicial aleatória de 5 caracteres
def generate_random_password():
    return ''.join(random.choices(ALPHABET, k=PASSWORD_LENGTH))

# Função hash SHA-512
def sha512_hash(value):
    return hashlib.sha512(value.encode()).hexdigest()

# Redução colorida: depende da posição (usa diferentes partes do hash e aplica variação)
def reduce_colorful(hash_value, position):
    reduced = ''
    # Começo diferente para cada posição (muda o offset)
    offset = (position * 13) % (len(hash_value) - PASSWORD_LENGTH * 2)
    for i in range(PASSWORD_LENGTH):
        # Pega 2 caracteres hexadecimais e converte para número
        hex_pair = hash_value[offset + i * 2: offset + i * 2 + 2]
        num = int(hex_pair, 16)
        reduced += ALPHABET[num % len(ALPHABET)]
    return reduced

# Geração da rainbow table
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

# Executa
generate_rainbow_table()
