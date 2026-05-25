import os
from sqlalchemy import create_engine, text

_url = os.environ.get('DATABASE_URL', 'sqlite:///ebf.db').strip()

# Normaliza URL para usar psycopg3 no PostgreSQL (suporta Python 3.14)
if _url.startswith('postgresql://') or _url.startswith('postgres://'):
    host_part = _url.split('://', 1)[1]
    _url = 'postgresql+psycopg://' + host_part

engine = create_engine(_url)
_is_postgres = _url.startswith('postgresql')


def criar_tabela():
    with engine.connect() as conn:
        if _is_postgres:
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS criancas (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    responsavel TEXT NOT NULL,
                    idade TEXT NOT NULL,
                    igreja TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )
            '''))
        else:
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS criancas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    responsavel TEXT NOT NULL,
                    idade TEXT NOT NULL,
                    igreja TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )
            '''))
        conn.commit()
