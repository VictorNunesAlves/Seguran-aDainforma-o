import hashlib
import csv
import random
import time

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()-_+=<>?'
PASSWORD_LENGTH = 5
CHAIN_LENGTH = 1000

def sha512_hash(value):
    return hashlib.sha512(value.encode()).hexdigest()

def generate_random_password():
    return ''.join(random.choices(ALPHABET, k=PASSWORD_LENGTH))

def gerar_senhas(quantidade_de_senhas):
    senhas = []
    for _ in range(quantidade_de_senhas):
        senhas.append(generate_random_password())
    return senhas

def salvar_hashes_no_arquivo(lista_senhas, nome_arquivo='hashes.txt'):
    with open(nome_arquivo, 'w') as f:
        for senha in lista_senhas:
            hash_senha = sha512_hash(senha)
            f.write(hash_senha + '\n')

def reduce_colorful(hash_value, position):
    reduced = ''
    offset = (position * 13) % (len(hash_value) - PASSWORD_LENGTH * 2)
    for i in range(PASSWORD_LENGTH):
        hex_pair = hash_value[offset + i * 2: offset + i * 2 + 2]
        num = int(hex_pair, 16)
        reduced += ALPHABET[num % len(ALPHABET)]
    return reduced

def carregar_rainbow_table(caminho_csv):
    rainbow_dict = {}
    with open(caminho_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rainbow_dict[row['end']] = row['start']
    return rainbow_dict

def quebrar_hash(hash_alvo, rainbow_table):
    for end, start in rainbow_table.items():
        current = start
        for pos in range(CHAIN_LENGTH):
            h = sha512_hash(current)
            if h == hash_alvo:
                return current  
            current = reduce_colorful(h, pos)
    return None  

def procurar_hashes_em_rainbow_table(arquivo_hashes, arquivo_tabela):
    rainbow_table = carregar_rainbow_table(arquivo_tabela)

    with open(arquivo_hashes, 'r') as f:
        hashes = [linha.strip() for linha in f if linha.strip()]

    for h in hashes:
        resultado = quebrar_hash(h, rainbow_table)
        if resultado:
            print(f"Hash encontrado: {h}\nSenha original: {resultado}\n")
        else:
            print(f"Hash nao encontrado: {h}\n")

if __name__ == "__main__":
    quantidade_de_senhas = 10
    senhas = gerar_senhas(quantidade_de_senhas)  
    salvar_hashes_no_arquivo(senhas)

    start_time = time.time()  
    procurar_hashes_em_rainbow_table('hashes.txt', 'rainbow_table_colorida.csv')
    end_time = time.time() 

    tempo_total = end_time - start_time
    print(f"Tempo total para procurar hashes: {tempo_total:.2f} segundos")