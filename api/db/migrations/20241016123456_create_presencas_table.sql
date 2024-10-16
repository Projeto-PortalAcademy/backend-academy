-- db/migrations/20241016123456_create_presencas_table.sql

-- migrate:up
-- Criação da tabela presencas
CREATE TABLE presencas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    data_para_presenca DATE NOT NULL,
    presenca BOOLEAN DEFAULT NULL,
    comentario VARCHAR(100) NOT NULL
);

-- Criação da tabela tokens
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(100) NOT NULL
);

-- Criação da tabela words
CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL
);

-- Criação da tabela date_presence
CREATE TABLE date_presence (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    data_inicial DATE NOT NULL,
    data_final DATE NOT NULL
);

-- -- migrate:down
-- -- Exclusão da tabela presencas
-- DROP TABLE IF EXISTS presencas;

-- -- Exclusão da tabela tokens
-- DROP TABLE IF EXISTS tokens;

-- -- Exclusão da tabela words
-- DROP TABLE IF EXISTS words;

-- -- Exclusão da tabela date_presence
-- DROP TABLE IF EXISTS date_presence;
