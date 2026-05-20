from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
import csv
import os

app = Flask(__name__)

app.secret_key = 'ebf2026'

ARQUIVO_CSV = 'dados/criancas.csv'


def criar_cabecalho():

    arquivo_existe = os.path.isfile(ARQUIVO_CSV)

    if not arquivo_existe or os.path.getsize(ARQUIVO_CSV) == 0:

        with open(
            ARQUIVO_CSV,
            'w',
            newline='',
            encoding='utf-8'
        ) as arquivo:

            writer = csv.writer(arquivo)

            writer.writerow([
                'nome',
                'responsavel',
                'idade',
                'igreja',
                'telefone'
            ])


@app.route('/', methods=['GET', 'POST'])
def home():

    mensagem = ''

    return redirect(url_for('home'))

    if request.method == 'POST':

        criar_cabecalho()

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

        dados = [
            nome,
            responsavel,
            idade,
            igreja,
            telefone
        ]

        with open(
            ARQUIVO_CSV,
            'a',
            newline='',
            encoding='utf-8'
        ) as arquivo:

            writer = csv.writer(arquivo)

            writer.writerow(dados)

            mensagem = 'Cadastro realizado com sucesso!'

    return render_template('index.html')


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

    criancas = []

    try:

        with open(
            ARQUIVO_CSV,
            'r',
            encoding='utf-8'
        ) as arquivo:

            leitor = csv.reader(arquivo)

            next(leitor)

            for linha in leitor:

                criancas.append(linha)

    except FileNotFoundError:

        pass

    total = len(criancas)

    return render_template(
        'admin.html',
        criancas=criancas,
        total=total
    )

@app.route('/remover/<nome>')
def remover(nome):

    if not session.get('admin_logado'):

        return redirect(url_for('login'))

    linhas_atualizadas = []

    try:

        with open(
            ARQUIVO_CSV,
            'r',
            encoding='utf-8'
        ) as arquivo:

            leitor = csv.reader(arquivo)

            cabecalho = next(leitor)

            linhas_atualizadas.append(cabecalho)

            for linha in leitor:

                if linha[0] != nome:

                    linhas_atualizadas.append(linha)

        with open(
            ARQUIVO_CSV,
            'w',
            newline='',
            encoding='utf-8'
        ) as arquivo:

            writer = csv.writer(arquivo)

            writer.writerows(linhas_atualizadas)

    except FileNotFoundError:

        pass

    return redirect(url_for('admin'))

@app.route('/editar/<nome>', methods=['GET', 'POST'])
def editar(nome):

    if not session.get('admin_logado'):

        return redirect(url_for('login'))

    crianca_encontrada = None

    linhas_atualizadas = []

    try:

        with open(
            ARQUIVO_CSV,
            'r',
            encoding='utf-8'
        ) as arquivo:

            leitor = csv.reader(arquivo)

            cabecalho = next(leitor)

            for linha in leitor:

                if linha[0] == nome:

                    crianca_encontrada = linha

                linhas_atualizadas.append(linha)

    except FileNotFoundError:

        return redirect(url_for('admin'))

    if request.method == 'POST':

        novo_nome = request.form['nome']

        novo_responsavel = request.form['responsavel']

        nova_idade = request.form['idade']

        nova_igreja = request.form['igreja']

        novo_telefone = request.form['telefone']

        novas_linhas = [cabecalho]

        for linha in linhas_atualizadas:

            if linha[0] == nome:

                linha = [
                    novo_nome,
                    novo_responsavel,
                    nova_idade,
                    nova_igreja,
                    novo_telefone
                ]

            novas_linhas.append(linha)

        with open(
            ARQUIVO_CSV,
            'w',
            newline='',
            encoding='utf-8'
        ) as arquivo:

            writer = csv.writer(arquivo)

            writer.writerows(novas_linhas)

        return redirect(url_for('admin'))

    return render_template(
        'editar.html',
        crianca=crianca_encontrada
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)