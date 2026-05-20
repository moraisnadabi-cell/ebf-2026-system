from database import criar_tabela, conectar
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import os

app = Flask(__name__)

criar_tabela()

app.secret_key = 'ebf2026'




@app.route('/', methods=['GET', 'POST'])
def home():

    mensagem = ''


    if request.method == 'POST':

        

        nome = request.form['nome'].title().strip()

        responsavel = request.form[
            'responsavel'
        ].title().strip()

        idade = request.form['idade'].strip()

        igreja = request.form[
            'igreja'
        ].title().strip()

        telefone = request.form[
            'telefone'
        ].strip()

        if (
            nome == '' or
            responsavel == '' or
            idade == '' or
            igreja == '' or
            telefone == ''
        ):

            mensagem = 'Preencha todos os campos.'

            return render_template(
                'index.html',
                mensagem=mensagem
            )

            

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute('''
            SELECT * FROM criancas
            WHERE nome = ?
            AND telefone = ?
        ''', (
            nome,
            telefone
        ))

        crianca_existente = cursor.fetchone()

        if crianca_existente:

            conexao.close()

            mensagem = 'Essa criança já foi cadastrada.'

            return render_template(
                'index.html',
                mensagem=mensagem
            )

        cursor.execute('''
                INSERT INTO criancas (
                nome,
                responsavel,
                idade,
                igreja,
                telefone
            )

            VALUES (?, ?, ?, ?, ?)
        ''', (
            nome,
            responsavel,
            idade,
            igreja,
            telefone
        ))

        conexao.commit()

        conexao.close()

        mensagem = 'Cadastro realizado com sucesso!'

        return render_template(
            'index.html',
            mensagem=mensagem
        )

    return render_template(
        'index.html',
        mensagem=mensagem
    )



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

    return render_template(
        'login.html',
        mensagem=mensagem
    )


@app.route('/admin')
def admin():

    if not session.get('admin_logado'):

        return redirect(url_for('login'))

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM criancas')

    criancas = cursor.fetchall()

    conexao.close()

    total = len(criancas)

    return render_template(
        'admin.html',
        criancas=criancas,
        total=total
    )

@app.route('/remover/<int:id>')
def remover(id):

    if not session.get('admin_logado'):
        return redirect(url_for('login'))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM criancas WHERE id = ?', (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for('admin'))

    

@app.route('/editar/<nome>', methods=['GET', 'POST'])
def editar(nome):

    if not session.get('admin_logado'):

        return redirect(url_for('login'))

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == 'POST':

        novo_nome = request.form['nome']
        novo_responsavel = request.form['responsavel']
        nova_idade = request.form['idade']
        nova_igreja = request.form['igreja']
        novo_telefone = request.form['telefone']

        cursor.execute('''
            UPDATE criancas
            SET nome = ?,
                responsavel = ?,
                idade = ?,
                igreja = ?,
                telefone = ?
            WHERE nome = ?
        ''', (
            novo_nome,
            novo_responsavel,
            nova_idade,
            nova_igreja,
            novo_telefone,
            nome
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for('admin'))

    cursor.execute('''
        SELECT * FROM criancas
        WHERE nome = ?
    ''', (nome,))

    crianca = cursor.fetchone()

    conexao.close()

    return render_template('editar.html', crianca=crianca)
    


if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=porta
    )