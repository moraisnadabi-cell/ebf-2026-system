import sqlite3


def conectar():

    conexao = sqlite3.connect('ebf.db')

    return conexao


def criar_tabela():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS criancas (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            responsavel TEXT NOT NULL,

            idade TEXT NOT NULL,

            igreja TEXT NOT NULL,

            telefone TEXT NOT NULL
        )
    ''')

    conexao.commit()

    conexao.close()