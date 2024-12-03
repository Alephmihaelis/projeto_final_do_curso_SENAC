
from flask import Flask, flash, render_template, request, redirect, session, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Cria o app Flask
app = Flask(__name__)

# Define a chave secreta para sessões
app.secret_key = os.urandom(24)

def db_connection():

    '''
    Conecta ao banco de dados e retorna o objeto da conexão.
    '''

    # Estabelece a conexã com o MySQL
    conn = mysql.connector.connect(
        host='localhost', # Host do banco de dados
        user='root', # Usuário do banco de dados
        password='', # Senha do banco de dados
        database='databasedb' # Nome do banco de dados
        )

    return conn # Retorna a conexão feita com o banco de dados

# Função da rota login
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Verifica se o método da requisição é `POST`
    if request.method == 'POST':
        # Obtém os valores dos campos `email` e `password` do formulário
        email = request.form['email']
        password = request.form['password']

        # Abre a conexão com o banco de dados
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        # Faz a consulta para verificar se o e-mail fornecido existe no banco de dados
        cursor.execute("SELECT * FROM recrutadores WHERE email = %s", (email,))
        recrutador = cursor.fetchone() # Retorna o primeiro recrutador encontrado
        conn.close() # Fecha a conexão com o banco de dados

        # Verifica se o recrutador foi encontrado e se a senha dele é válida
        if recrutador and check_password_hash(recrutador['password'], password):
            # Armazena as informações do recrutador na sessão
            session['recrutador_id'] = recrutador['id']
            session['recrutador_name'] = recrutador['name']
            # Mostra mensagem de sucesso no login
            flash("Login realizado com sucesso!", "success")
            # Linha que redireciona o recrutador para a página inicial após o login
            return redirect(url_for('index'))
        
        else:
            # Mostra uma mensagem de erro se as credenciais informadas estiverem erradas
            flash("Credenciais inválidas!")
            # Redireciona para a página de login
            return redirect(url_for('login'))

    # Verifica se o método é `GET`. Se sim, renderiza a página de login    
    return render_template('login.html')

# Função de logout
@app.route('/logout')
def logout():

    # Limpa todas as informações da sessão
    session.clear()

    # Redireciona para a página inicial
    return redirect(url_for('index'))

# Rota da página inicial
@app.route('/')
def index():

    # Abre a conexão com o banco de dados
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Busca todos os funcionários e seus recrutadores
    cursor.execute('''
                   SELECT f.id, f.name, f.email, f.tel, f.cargo, f.contratado_em, r.name AS recrutador
                   FROM funcionarios f
                   LEFT JOIN recrutadores r ON f.recrutador_id = r.id
                   ''')
    
    # Obtém os resultados da consulta
    funcionarios = cursor.fetchall()

    # Consulta em que se obtém todos os nomes dos recrutadores
    cursor.execute('SELECT name FROM recrutadores')

    # Retorna o resultado da consulta
    rec = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conn.close()

    # Renderiza a página `index` e passa os dados dos funcionários e dos recrutadores para ela
    return render_template('index.html', func=funcionarios, rec=rec)

# Rota que exibe os recrutadores
@app.route('/show_recrut')
def show_recrut():

    # Abre a conexão com o banco de dados
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Consulta todos os recrutadores
    cursor.execute('SELECT * FROM recrutadores')
    recrutadores = cursor.fetchall()

    # Consulta todos os recrutadores com funcionários
    cursor.execute('SELECT * FROM recrutadores_com_funcionarios')

    # Obtém o resultado da consulta
    recs = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conn.close()

    # Renderiza `show_recrut` e passa as informações de `recs` e `recrutadores` para ela
    return render_template('show_recrut.html', recs=recs, recrutadores=recrutadores)

# Rota para adicionar novo funcionário
@app.route('/add_func', methods=['GET', 'POST'])
def add_func():

    # Conecta com o banco de dados
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Primeiro, obtém `id` e `name` de todos os recrutadores
    cursor.execute('SELECT id, name FROM recrutadores')

    # Retorna o resultado da consulta
    recrutadores = cursor.fetchall()

    # Fecha a conexã com o banco de dados
    conn.close()

    # Verifica se o método da requisição é `POST`
    if request.method == 'POST':
        # Se sim, obtém os seguintes dados do formulário:
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        cargo = request.form['cargo']
        contratado_em = request.form['contratado_em']
        recrutador = request.form['recrutador']

        # Abre a conexão outra vez para inserir o novo funcionário
        conn = db_connection()
        cursor = conn.cursor()
        
        # Insere o novo funcionário
        cursor.execute('''
                       INSERT INTO funcionarios(name, email, tel, cargo, contratado_em, recrutador_id)
                       VALUES
                       (%s, %s, %s, %s, %s, %s)
                       ''',
                       (name, email, tel, cargo, contratado_em, recrutador))
        
        # Confirma a inserção
        conn.commit()
        
        # Fecha o banco de dados
        conn.close()

        # Redireciona para a página inicial
        return redirect(url_for('index'))

    # Renderiza `add_func` com as informações de `recrutadores`
    return render_template('add_func.html', recrutadores=recrutadores)

# Rota que adiciona novos recrutadores
@app.route('/add_recrut', methods=['GET', 'POST'])
def add_recrut():

    # Cargo padrão para todo recrutador
    cargo_padrao = 'Recrutador'

    # Verifica se o método da requisição é `POST`
    if request.method == 'POST':
        # Se sim, obtém os seguintes dados do formulário:
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        password = request.form['password']

        # Criptografa a senha criada pelo recrutador
        hashed_password = generate_password_hash(password)

        # Abre a conexão com o banco de dados
        conn = db_connection()
        cursor = conn.cursor()

        # Insere o novo recrutador
        cursor.execute('''
                       INSERT INTO recrutadores (name, email, tel, password)
                       VALUES
                       (%s, %s, %s, %s)
                       ''',
                        (name, email, tel, hashed_password))
        
        # Confirma a inserção
        conn.commit()

        # Fecha a conexão
        conn.close()

        # Redireciona para a página inicial
        return redirect(url_for('index'))

    # Renderiza `add_recrut` com a informação de `cargo_padrao`
    return render_template('add_recrut.html', cargo_padrao=cargo_padrao)

# Rota para editar as informações de um funcionário
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

        # Conecta ao banco de dados
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        # Busca os dados do funcionário a partir do `id` atribuído a ele
        cursor.execute('SELECT * FROM funcionarios WHERE id = %s', (id,))
        funcionario = cursor.fetchone()

        # Se o funcionário não for encontrado, redireciona para a página inicial
        if not funcionario:
            return redirect(url_for('index'))

        # Verifica se o método da requisição é `POST`        
        if request.method == 'POST':
            # Se sim, obtém os dados que foram passados no formulário:
            name = request.form['name']
            email = request.form['email']
            tel = request.form['tel']
            cargo = request.form['cargo']
            contratado_em = request.form['contratado_em']

            # Atualiza os dados do funcionário
            cursor.execute('''
            UPDATE funcionarios
            SET name = %s, email = %s, tel = %s, cargo = %s, contratado_em = %s
            WHERE id = %s
            ''',
            (name, email, tel, cargo, contratado_em, id))
            
            # Confirma a atualização
            conn.commit()

            # Fecha a conexão com o banco de dados
            conn.close()

            return redirect(url_for('index'))
        
        # Fecha a conexão com o banco de dados
        conn.close()

        # Renderiza `edit` com os dados de `funcionario`
        return render_template('edit.html', funcionario=funcionario)

# Rota para deletar funcionários
@app.route('/delete/<id>', methods=['POST'])
def delete(id):

    # Abre a conexão com o banco de dados
    conn = db_connection()
    cursor = conn.cursor()

    # Deleta o funcionário de acordo com o `id` capturado
    cursor.execute('DELETE FROM funcionarios WHERE id = %s', (id,))
    conn.commit() # Confirma a exclusão
    conn.close() # Fecha a conexão com o banco de dados

    # Redireciona para `index`
    return redirect(url_for('index'))

# Inicia a app Flask em modo de depuração
if __name__ == '__main__':
    app.run(debug=True)
