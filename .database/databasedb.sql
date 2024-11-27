
DROP DATABASE IF EXISTS databasedb;

CREATE DATABASE databasedb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE databasedb;

CREATE TABLE Funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    tel VARCHAR(15) NOT NULL,
    cargo VARCHAR(127) NOT NULL,
    contratado_em DATE DEFAULT CURRENT_TIMESTAMP
);