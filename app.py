
from flask import Flask, flash, render_template, request, redirect, session, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Cria o app Flask
app = Flask(__name__)

# Define a chave secreta para sessões
app.secret_key = os.urandom(24)

def db_connection():

    """
    Conecta ao banco de dados e retorna o objeto da conexão.
    """

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='databasedb')

    return conn

# Função de `login`
@app.route('/login', methods=['GET', 'POST'])
def login():

    """
    Rota de login.
    """

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recrutadores WHERE email = %s", (email,))
        recrutador = cursor.fetchone()
        conn.close()

        if recrutador and check_password_hash(recrutador['password'], password):
            session['recrutador_id'] = recrutador['id']
            session['recrutador_name'] = recrutador['name']
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('index'))
        
        else:
            flash("Credenciais inválidas!")
            return redirect(url_for('login'))
        

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''SELECT f.id, f.name, f.email, f.tel, f.cargo, f.contratado_em, r.name AS recrutador
                   FROM funcionarios f
                   LEFT JOIN recrutadores r ON f.recrutador_id = r.id''')
    funcionarios = cursor.fetchall()
    cursor.execute('SELECT name FROM recrutadores')
    rec = cursor.fetchall()
    conn.close()

    return render_template('index.html', func=funcionarios, rec=rec)

@app.route('/show_recrut')
def show_recrut():

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM recrutadores')
    recrutadores = cursor.fetchall()

    cursor.execute('SELECT * FROM recrutadores_com_funcionarios')
    recs = cursor.fetchall()
    conn.close()

    return render_template('show_recrut.html', recs=recs, recrutadores=recrutadores)

@app.route('/add_func', methods=['GET', 'POST'])
def add_func():

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name FROM recrutadores')
    recrutadores = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        cargo = request.form['cargo']
        contratado_em = request.form['contratado_em']
        recrutador = request.form['recrutador']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO funcionarios(name, email, tel, cargo, contratado_em, recrutador_id)
                       VALUES
                       (%s, %s, %s, %s, %s, %s)''',
                       (name, email, tel, cargo, contratado_em, recrutador))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_func.html', recrutadores=recrutadores)

@app.route('/add_recrut', methods=['GET', 'POST'])
def add_recrut():

    cargo_padrao = 'Recrutador'

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO recrutadores (name, email, tel, password) VALUES (%s, %s, %s, %s)',
                        (name, email, tel, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_recrut.html', cargo_padrao=cargo_padrao)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM funcionarios WHERE id = %s', (id,))
        funcionario = cursor.fetchone()

        if not funcionario:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            tel = request.form['tel']
            cargo = request.form['cargo']
            contratado_em = request.form['contratado_em']

            cursor.execute('''
            UPDATE funcionarios
            SET name = %s, email = %s, tel = %s, cargo = %s, contratado_em = %s
            WHERE id = %s
            ''', (name, email, tel, cargo, contratado_em, id))
            
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        
        conn.close()
        return render_template('edit.html', funcionario=funcionario)


@app.route('/delete/<id>', methods=['POST'])
def delete(id):

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM funcionarios WHERE id = %s', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
