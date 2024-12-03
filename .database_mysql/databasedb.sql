DROP DATABASE IF EXISTS databasedb;

CREATE DATABASE databasedb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

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
