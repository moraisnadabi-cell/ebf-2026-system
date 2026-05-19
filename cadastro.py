import csv
import os 
from utils.validacoes import (
    validar_idade,
    validar_texto,
    validar_telefone
)

ARQUIVO_CSV = 'dados/criancas.csv'

def criar_cabecalho():

    arquivo_existe = os.path.isfile(ARQUIVO_CSV)

    if not arquivo_existe or os.path.getsize(ARQUIVO_CSV) == 0:

        with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as arquivo:

            writer = csv.writer(arquivo)

            writer.writerow([
                'nome',
                'responsavel',
                'idade',
                'igreja',
                'telefone'
            ])

def crianca_ja_cadastrada(nome):

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            for linha in leitor:

                if linha[0].lower() == nome.lower():
                    return True

    except FileNotFoundError:
        return False

    return False


def cadastrar_crianca():

    criar_cabecalho()

    nome = input('Nome da criança: ').title().strip()
    responsavel = input('Nome do responsável: ').title().strip()
    idade = input('Idade da criança: ').strip()
    igreja = input('Denominação/Igreja: ').title().strip()
    telefone = input('Telefone/Whatsapp: ').strip()

    

    if not validar_texto(nome):
        print('Nome inválido.')
        return

    if not validar_texto(responsavel):
        print('Responsável inválido.')
        return

    if not validar_texto(igreja):
        print('Igreja inválida.')
        return

    if not validar_idade(idade):
        print('Idade inválida.')
        return

    if not validar_telefone(telefone):
        print('Telefone inválido.')
        return

    dados = [nome, responsavel, idade, igreja, telefone]

    with open(ARQUIVO_CSV, 'a', newline='', encoding='utf-8') as arquivo:

        writer = csv.writer(arquivo)

        writer.writerow(dados)

    print('Cadastro realizado com sucesso!')


def listar_criancas():

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            print('\n=== CRIANÇAS CADASTRADAS ===')

            for linha in leitor:
                print(f'''
Nome: {linha[0]}
Responsável: {linha[1]}
Idade: {linha[2]}
Igreja: {linha[3]}
Telefone: {linha[4]}
''')

    except FileNotFoundError:
        print('Nenhum cadastro encontrado.')

def total_inscritos():

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            linhas = list(leitor)

            total = len(linhas) - 1

            print(f'\nTotal de crianças cadastradas: {total}')

    except FileNotFoundError:

        print('Nenhum cadastro encontrado.')

def buscar_crianca():

    nome_busca = input('\nDigite o nome da criança: ').title().strip()

    encontrada = False

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            next(leitor)

            for linha in leitor:

                if linha[0] == nome_busca:

                    print(f'''
Nome: {linha[0]}
Responsável: {linha[1]}
Idade: {linha[2]}
Igreja: {linha[3]}
Telefone: {linha[4]}
''')

                    encontrada = True

        if not encontrada:
            print('Criança não encontrada.')

    except FileNotFoundError:
        print('Nenhum cadastro encontrado.')

def filtrar_por_igreja():

    igreja_busca = input(
        '\nDigite o nome da igreja: '
    ).title().strip()

    encontrada = False

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            next(leitor)

            print(f'\n=== Crianças da igreja {igreja_busca} ===')

            for linha in leitor:

                if linha[3] == igreja_busca:

                    print(f'''
Nome: {linha[0]}
Responsável: {linha[1]}
Idade: {linha[2]}
Telefone: {linha[4]}
''')

                    encontrada = True

        if not encontrada:
            print('Nenhuma criança encontrada.')

    except FileNotFoundError:
        print('Nenhum cadastro encontrado.')

def editar_cadastro():

    nome_busca = input(
        '\nDigite o nome da criança que deseja editar: '
    ).title().strip()

    linhas_atualizadas = []

    encontrada = False

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            cabecalho = next(leitor)

            linhas_atualizadas.append(cabecalho)

            for linha in leitor:

                if linha[0] == nome_busca:

                    print('\n=== NOVOS DADOS ===')

                    novo_nome = input(
                        'Novo nome da criança: '
                    ).title().strip()

                    novo_responsavel = input(
                        'Novo responsável: '
                    ).title().strip()

                    nova_idade = input(
                        'Nova idade: '
                    ).strip()

                    nova_igreja = input(
                        'Nova igreja: '
                    ).title().strip()

                    novo_telefone = input(
                        'Novo telefone: '
                    ).strip()

                    linha = [
                        novo_nome,
                        novo_responsavel,
                        nova_idade,
                        nova_igreja,
                        novo_telefone
                    ]

                    encontrada = True

                linhas_atualizadas.append(linha)

        if encontrada:

            with open(
                ARQUIVO_CSV,
                'w',
                newline='',
                encoding='utf-8'
            ) as arquivo:

                writer = csv.writer(arquivo)

                writer.writerows(linhas_atualizadas)

            print('\nCadastro atualizado com sucesso!')

        else:
            print('\nCriança não encontrada.')

    except FileNotFoundError:
        print('\nArquivo não encontrado.')

def remover_cadastro():

    nome_busca = input(
        '\nDigite o nome da criança que deseja remover: '
    ).title().strip()

    linhas_atualizadas = []

    encontrada = False

    try:

        with open(ARQUIVO_CSV, 'r', encoding='utf-8') as arquivo:

            leitor = csv.reader(arquivo)

            cabecalho = next(leitor)

            linhas_atualizadas.append(cabecalho)

            for linha in leitor:

                if linha[0] == nome_busca:

                    encontrada = True

                    continue

                linhas_atualizadas.append(linha)

        if encontrada:

            with open(
                ARQUIVO_CSV,
                'w',
                newline='',
                encoding='utf-8'
            ) as arquivo:

                writer = csv.writer(arquivo)

                writer.writerows(linhas_atualizadas)

            print('\nCadastro removido com sucesso!')

        else:
            print('\nCriança não encontrada.')

    except FileNotFoundError:
        print('\nArquivo não encontrado.')