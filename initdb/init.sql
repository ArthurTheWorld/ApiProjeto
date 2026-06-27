-- ==============================================
-- Banco de dados: appdb
-- Aplicação: API Flask com cadastro de usuários
-- ==============================================

CREATE DATABASE IF NOT EXISTS appdb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE appdb;

-- Tabela principal de usuários
CREATE TABLE IF NOT EXISTS users (
    id         INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    nome       VARCHAR(120)    NOT NULL,
    email      VARCHAR(160)    NOT NULL UNIQUE,
    criado_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- Dados de exemplo (opcional — remova se não quiser)
INSERT INTO users (nome, email) VALUES
    ('Alice Silva',  'alice@example.com'),
    ('Bruno Costa',  'bruno@example.com');
