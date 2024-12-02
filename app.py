
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
    cursor.execute('''SELECT f.id, f.name, f.email, f.tel, f.cargo, f.contratado_em, r.name AS recrutador
                   FROM funcionarios f
                   LEFT JOIN recrutadores r ON f.recrutador_id = r.id''')
    funcionarios = cursor.fetchall()
    cursor.execute('SELECT name FROM recrutadores')
    rec = cursor.fetchall()
    conn.close()
    return render_template('index.html', func=funcionarios, rec=rec)

# Rota para adicionar novo usuário
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
        cursor.execute('INSERT INTO funcionarios(name, email, tel, cargo, contratado_em, recrutador_id) VALUES (%s, %s, %s, %s, %s, %s)',
                       (name, email, tel, cargo, contratado_em, recrutador))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_func.html', recrutadores=recrutadores)

# Rota para adicionar novo recrutador
@app.route('/add_recrut', methods=['GET', 'POST'])
def add_recrut():

    cargo_padrao = 'Recrutador'

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO recrutadores (name, email, tel) VALUES (%s, %s, %s)',
                       (name, email, tel))
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