import os
from database import engine, criar_tabela
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ebf2026')

criar_tabela()


@app.route('/ping')
def ping():
    return 'ok', 200


@app.route('/', methods=['GET', 'POST'])
def home():
    mensagem = ''

    if request.method == 'POST':
        nome = request.form['nome'].title().strip()
        responsavel = request.form['responsavel'].title().strip()
        idade = request.form['idade'].strip()
        igreja = request.form['igreja'].title().strip()
        telefone = request.form['telefone'].strip()

        if not all([nome, responsavel, idade, igreja, telefone]):
            mensagem = 'Preencha todos os campos.'
            return render_template('index.html', mensagem=mensagem)

        with engine.connect() as conn:
            resultado = conn.execute(text('''
                SELECT id FROM criancas
                WHERE nome = :nome AND telefone = :telefone
            '''), {'nome': nome, 'telefone': telefone})

            if resultado.fetchone():
                mensagem = 'Essa criança já foi cadastrada.'
                return render_template('index.html', mensagem=mensagem)

            conn.execute(text('''
                INSERT INTO criancas (nome, responsavel, idade, igreja, telefone)
                VALUES (:nome, :responsavel, :idade, :igreja, :telefone)
            '''), {
                'nome': nome,
                'responsavel': responsavel,
                'idade': idade,
                'igreja': igreja,
                'telefone': telefone
            })
            conn.commit()

        mensagem = 'Cadastro realizado com sucesso!'
        return render_template('index.html', mensagem=mensagem)

    return render_template('index.html', mensagem=mensagem)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = ''

    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == 'admin' and senha == '1234':
            session['admin_logado'] = True
            return redirect(url_for('admin'))
        else:
            mensagem = 'Usuário ou senha inválidos.'

    return render_template('login.html', mensagem=mensagem)


@app.route('/admin')
def admin():
    if not session.get('admin_logado'):
        return redirect(url_for('login'))

    with engine.connect() as conn:
        resultado = conn.execute(text('SELECT * FROM criancas ORDER BY nome'))
        criancas = resultado.fetchall()

    total = len(criancas)
    return render_template('admin.html', criancas=criancas, total=total)


@app.route('/remover/<int:id>')
def remover(id):
    if not session.get('admin_logado'):
        return redirect(url_for('login'))

    with engine.connect() as conn:
        conn.execute(text('DELETE FROM criancas WHERE id = :id'), {'id': id})
        conn.commit()

    return redirect(url_for('admin'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('admin_logado'):
        return redirect(url_for('login'))

    with engine.connect() as conn:
        if request.method == 'POST':
            conn.execute(text('''
                UPDATE criancas
                SET nome = :nome,
                    responsavel = :responsavel,
                    idade = :idade,
                    igreja = :igreja,
                    telefone = :telefone
                WHERE id = :id
            '''), {
                'nome': request.form['nome'],
                'responsavel': request.form['responsavel'],
                'idade': request.form['idade'],
                'igreja': request.form['igreja'],
                'telefone': request.form['telefone'],
                'id': id
            })
            conn.commit()
            return redirect(url_for('admin'))

        resultado = conn.execute(
            text('SELECT * FROM criancas WHERE id = :id'), {'id': id}
        )
        crianca = resultado.fetchone()

    return render_template('editar.html', crianca=crianca)


if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
