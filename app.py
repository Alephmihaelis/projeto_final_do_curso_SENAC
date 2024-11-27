
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conecta com o banco de dados
def db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='databasedb')
    return conn

# Rota inicial em que são exibidos todos os usuários
@app.route('/')
def index():

    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Funcionarios')
    funcionarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', func=funcionarios)

# Rota para adicionar novo usuário
@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        cargo = request.form['cargo']
        contratado_em = request.form['contratado_em']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Funcionarios (name, email, tel, cargo, contratado_em ) VALUES (%s, %s, %s, %s, %s)', (name, email, tel, cargo, contratado_em))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):

        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM Funcionarios WHERE id = %s', (id,))
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
            UPDATE Funcionarios
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

    cursor.execute('DELETE FROM Funcionarios WHERE id = %s', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)