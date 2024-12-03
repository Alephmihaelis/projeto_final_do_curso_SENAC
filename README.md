# Projeto Web - Sistema de Recrutamento

Este é um projeto simples de um sistema de recrutamento que permite o login de recrutadores, visualização de funcionários e gerenciamento de dados no banco de dados. Foi desenvolvido utilizando **HTML**, **CSS**, **JavaScript**, **Python**, **Flask**, **MySQL** e **werkzeug.security**.

## Tecnologias Utilizadas

- **Frontend**:
  - HTML
  - CSS
  - JavaScript

- **Backend**:
  - Python
  - Flask
  - Werkzeug (para criptografia de senhas)

- **Banco de Dados**:
  - MySQL

## Funcionalidades

- **Cadastro de Recrutadores**: Recrutadores podem se cadastrar criando um nome, email, telefone e senha.
- **Login de Recrutadores**: Recrutadores podem fazer login com o email e senha cadastrados.
- **Visualização de Funcionários**: Recrutadores podem ver uma lista de funcionários e seus dados.
- **Gerenciamento de Funcionários**: Adicionar, editar e deletar funcionários associados a um recrutador.
- **Criptografia de Senhas**: As senhas dos recrutadores são criptografadas usando a biblioteca `werkzeug.security`.

## Como Rodar o Projeto

### 1. Requisitos

Certifique-se de ter os seguintes softwares instalados em seu sistema:

- **Python** (versão 3.6 ou superior)
- **MySQL** (instalado e configurado)
- **XAMPP** (caso deseje usar MySQL do XAMPP)
- **pip** (gerenciador de pacotes Python)

### 2. Instalando Dependências

Clone este repositório para o seu computador:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

Instale as dependências necessárias com o `pip`:
```
pip install -r requirements.txt
```
