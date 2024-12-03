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

- **Banco de dados**:
  - MySQL.

## Funcionalidades

- **Cadastro de Recrutadores**: Recrutadores podem ser cadastrados criando um nome, um email, um telefone e uma senha.
- **Login de Recrutadores**: Recrutadores podem fazer login com o email e senha cadastrados.
- **Visualização de Funcionários**: Recrutadores e usuários comuns podem ver uma lista de funcionários e seus dados.
- **Gerenciamento de Funcionários**: Recrutadores podem adicionar, editar e deletar funcionários.
- **Criptografia de Senhas**: As senhas dos recrutadores são criptografadas usando a biblioteca `werkzeug.security`.

## Como rodar o projeto

### 1. Requisitos

Certifique-se de ter os seguintes softwares instalados em seu sistema:

- **Python** (versão 3.6 ou superior);
- **MySQL**;
- **XAMPP** (caso deseje usar o MySQL do XAMPP);
- **pip**.

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
```
blinker==1.9.0
click==8.1.7
colorama==0.4.6
Flask==3.1.0
Flask-Login==0.6.3
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
mysql-connector==2.2.9
mysql-connector-python==9.1.0
Werkzeug==3.1.3
```

### 3. Configurando o banco de dados

Crie um banco de dados MySQL. O banco de dados pode ser criado com o seguinte script:

```
CREATE DATABASE seu-banco-de-dados
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE seu-banco-de-dados;

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
        database='seu-banco-de-dados'
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

### 6. Estrutura do projeto
```
/seu-projeto
│
├── .database_mysql       # Pasta com o banco de dados
│   ├── databasedb.sql    # Arquivo que modela o banco de dados usado no projeto
├── app.py                # Arquivo principal que contém o código do Flask
├── requirements.txt      # Arquivo com as dependências do projeto
├── templates/            # Pasta com os templates HTML
│   ├── index.html        # Página inicial
│   ├── login.html        # Página de login
│   ├── add_func.html     # Formulário para adicionar funcionário
│   ├── add_recrut.html   # Formulário para adicionar recrutador
│   ├── show_recrut.html  # Exibição de recrutadores
│   └── edit.html         # Formulário para editar funcionário
├── static/               # Arquivo estático com CSS
│   ├── add.css           # CSS da página para adicionar funcionários
│   ├── edit.css          # CSS da página para editar funcionários
│   ├── index.css         # CSS da página principal
│   ├── login.css         # CSS da página de login
└── README.md             # Este arquivo
