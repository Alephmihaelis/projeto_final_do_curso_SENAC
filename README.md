# Projeto final do curso SENAC: Projeto Web: Gerenciamento de funcionários

Este é um projeto simples de um sistema de gerenciamento de funcionários, que permite o login de recrutadores, visualização de funcionários e gerenciamento de dados no banco de dados. Este projeto foi desenvolvido utilizando **HTML**, **CSS**, **JavaScript**, **Python**, **Flask**, **MySQL** e **werkzeug.security**.

## Tecnologias utilizadas

- **Frontend**:
  - HTML;
  - CSS;
  - JavaScript.

- **Backend**:
  - Python;
  - Flask;
  - Werkzeug.

- **Banco de Dados**:
  - MySQL.

## Funcionalidades

- **Cadastro de Recrutadores**: Recrutadores podem se cadastrar criando um nome, email, telefone e senha.
- **Login de Recrutadores**: Recrutadores podem fazer login com o email e senha cadastrados.
- **Visualização de Funcionários**: Recrutadores e usuários comuns podem ver uma lista de funcionários e seus dados.
- **Gerenciamento de Funcionários**: Adicionar, editar e deletar funcionários associados a um recrutador.
- **Criptografia de Senhas**: As senhas dos recrutadores são criptografadas usando a biblioteca `werkzeug.security`.

## Como Rodar o Projeto

### 1. Requisitos

Certifique-se de ter os seguintes softwares instalados em seu sistema:

- **Python** (versão 3.6 ou superior)
- **MySQL** (instalado e configurado)
- **XAMPP** (caso deseje usar MySQL do XAMPP)
- **pip** (gerenciador de pacotes Python)

### 2. Instalando dependências

Clone este repositório para o seu computador:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

Instale as dependências necessárias com o `pip`:
```
pip install -r requirements.txt
```
O arquivo `requeriments.txt` deve conter as bibliotecas necessárias para o funcionamento do projeto:
<br>Flask==2.2.2<br>
mysql-connector-python==8.0.33<br>
werkzeug==2.2.3

### 3. Configurando o banco de dados

Crie um banco de dados MySQL. O banco de dados pode ser criado com o seguinte script:

```
DROP DATABASE IF EXISTS databasedb;

CREATE DATABASE databasedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE databasedb;

CREATE TABLE recrutadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    tel VARCHAR(15) NOT NULL,
    cargo VARCHAR(127) DEFAULT 'Recrutador',
    password VARCHAR(255)
);

CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    tel VARCHAR(15) NOT NULL,
    cargo VARCHAR(127) NOT NULL,
    contratado_em DATE DEFAULT CURRENT_TIMESTAMP,
    recrutador_id INT,
    FOREIGN KEY (recrutador_id) REFERENCES recrutadores(id)
);

CREATE VIEW recrutadores_com_funcionarios AS
SELECT r.id AS recrutador_id, r.name AS recrutador_name, r.email AS recrutador_email, 
       GROUP_CONCAT(f.id ORDER BY f.id) AS funcionarios_ids
FROM recrutadores r
LEFT JOIN funcionarios f ON f.recrutador_id = r.id
GROUP BY r.id;
```

Atualize as configurações de conexão do banco de dados no seu código Python:
```
def db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='databasedb'
    )
    return conn
```

### 4. Rode o servidor Flask
Após configurar o banco de dados, você pode rodar o servidor Flask. No terminal, execute:
```
python app.py
```
Por padrão, o aplicativo estará disponível em http://127.0.0.1:5000.

### 5. Usando o sistema
1. **ATENÇÃO:** O recrutador deve ser criado diretamente no aplicativo, e não previamente no banco de dados.
2. Use as funcionalidades para visualizar funcionários, adicionar novos e gerenciar os recrutadores.
