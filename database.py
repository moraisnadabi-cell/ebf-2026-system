import os
from sqlalchemy import create_engine, text

_url = os.environ.get('DATABASE_URL', 'sqlite:///ebf.db').strip()

# Render fornece 'postgres://', SQLAlchemy exige 'postgresql://'
if _url.startswith('postgres://') and not _url.startswith('postgresql://'):
    _url = 'postgresql://' + _url[len('postgres://'):]

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
