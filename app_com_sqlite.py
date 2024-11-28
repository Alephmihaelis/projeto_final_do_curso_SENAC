from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conecta com o banco de dados SQLite
def db_connection():
    conn = sqlite3.connect('databasedb.sqlite')  # Nome do arquivo SQLite
    conn.row_factory = sqlite3.Row  # Permite acessar os resultados como dicionários
    return conn

# Rota inicial em que são exibidos todos os usuários
@app.route('/')
def index():
    conn = db_connection()
    cursor = conn.cursor()
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
        cursor.execute('''
            INSERT INTO Funcionarios (name, email, tel, cargo, contratado_em)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, tel, cargo, contratado_em))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Rota para editar um usuário
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Funcionarios WHERE id = ?', (id,))
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
            SET name = ?, email = ?, tel = ?, cargo = ?, contratado_em = ?
            WHERE id = ?
        ''', (name, email, tel, cargo, contratado_em, id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', funcionario=funcionario)

# Rota para excluir um usuário
@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Funcionarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
