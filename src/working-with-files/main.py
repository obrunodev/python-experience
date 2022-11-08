import os

# Verifica se existe e cria estrutura de pastas
dir_path = 'arquivos/texto'
os.makedirs(dir_path, exist_ok=True)
file_name = 'copia.txt'

# Verifica se o arquivo existe na pasta
is_file = os.path.isfile('%s/%s' % (dir_path, file_name))

# Copia o arquivo de texto dentro da estrutura de pastas
if is_file:
    print('Arquivo já existe!')
else:
    with open(f'{dir_path}/{file_name}', 'w') as f:
        arquivo = open('arquivo.txt', 'r')
        f.write(arquivo.read())
