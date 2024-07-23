-- Database: bomprato

-- DROP DATABASE IF EXISTS bomprato;

CREATE DATABASE bomprato
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE Cartao_dependencia (
    id_cartao SERIAL PRIMARY KEY,
    validade DATE NOT NULL,
    pontos INTEGER DEFAULT 0,
    data_emissao DATE NOT NULL
);

CREATE TABLE Cliente (
    id_cliente SERIAL PRIMARY KEY,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    id_cartao INTEGER UNIQUE,
    FOREIGN KEY (id_cartao) REFERENCES Cartao_dependencia(id_cartao) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Prato (
    id_prato SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

CREATE TABLE Pedido (
    id_pedido SERIAL PRIMARY KEY,
    id_prato INTEGER,
    id_cliente INTEGER,
    horario_pedido TIMESTAMP NOT NULL,
    FOREIGN KEY (id_prato) REFERENCES Prato(id_prato) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Ingrediente (
    id_ingrediente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    quantidade INTEGER DEFAULT 0
);

CREATE TABLE Funcionario (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    salario NUMERIC(10, 2) NOT NULL,
    data_nascimento DATE NOT NULL
);

CREATE TABLE Prato_Ingrediente (
    id_prato SERIAL,
    id_ingrediente INTEGER,
    quantidade_utilizada INTEGER NOT NULL,
    PRIMARY KEY (id_prato, id_ingrediente),
    FOREIGN KEY (id_prato) REFERENCES Prato(id_prato) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_ingrediente) REFERENCES Ingrediente(id_ingrediente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Fornecedor (
    id_fornecedor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Telefone (
    id_fornecedor INTEGER,
    numero VARCHAR(15) NOT NULL,
    PRIMARY KEY (id_fornecedor, numero),
    FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id_fornecedor) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Fornecedor_Ingrediente (
    id_fornecedor INTEGER,
    id_ingrediente INTEGER,
    preco_fornecido DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_fornecedor, id_ingrediente),
    FOREIGN KEY (id_fornecedor) REFERENCES Fornecedor(id_fornecedor) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_ingrediente) REFERENCES Ingrediente(id_ingrediente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Login_Funcionario (
    id_login SERIAL PRIMARY KEY,
    id_funcionario INTEGER,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ultimo_login TIMESTAMP,
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE OR REPLACE FUNCTION AtualizaPontos() RETURNS TRIGGER AS $$
BEGIN
    UPDATE Cartao_dependencia
    SET pontos = pontos + 10
    WHERE id_cartao = (SELECT id_cartao FROM Cliente WHERE id_cliente = NEW.id_cliente);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Trigger_AtualizaPontos
AFTER INSERT ON Pedido
FOR EACH ROW
EXECUTE FUNCTION AtualizaPontos();


INSERT INTO Cartao_dependencia (validade, pontos, data_emissao) VALUES
('2025-12-31', 100, '2023-01-01'),
('2026-06-30', 200, '2023-07-01'),
('2024-09-30', 150, '2022-01-15');

INSERT INTO Cliente (cpf, nome, id_cartao) VALUES
('123.456.789-00', 'Alice Silva', 1),
('987.654.321-00', 'Bruno Souza', 2),
('456.789.123-00', 'Carlos Pereira', 3);

INSERT INTO Prato (nome, preco) VALUES
('Lasanha', 25.50),
('Pizza', 30.00),
('Salada', 15.75);

INSERT INTO Ingrediente (nome, preco, quantidade) VALUES
('Queijo', 10.00, 100),
('Tomate', 3.50, 200),
('Alface', 2.00, 150);

INSERT INTO Funcionario (nome, cpf, cargo, turno, salario, data_nascimento) VALUES
('Ana Lima', '11122233344', 'Cozinheiro', 'Manhã', 2500.00, '1985-05-15'),
('Paulo Gonçalves', '55566677788', 'Garçom', 'Tarde', 1800.00, '1990-08-20'),
('Mariana Costa', '99900011122', 'Gerente', 'Noite', 3500.00, '1980-12-30');

INSERT INTO Pedido (id_prato, id_cliente, horario_pedido) VALUES
(1, 1, '2024-07-22 12:00:00'),
(2, 2, '2024-07-22 13:00:00'),
(3, 3, '2024-07-22 14:00:00');

INSERT INTO Prato_Ingrediente (id_prato, id_ingrediente, quantidade_utilizada) VALUES
(1, 1, 2),
(1, 2, 3),
(2, 2, 4),
(2, 3, 1),
(3, 3, 2);

INSERT INTO Fornecedor (nome, cnpj) VALUES
('Fornecedor A', '12.345.678/0001-99'),
('Fornecedor B', '98.765.432/0001-88');

INSERT INTO Telefone (id_fornecedor, numero) VALUES
(1, '1234-5678'),
(2, '8765-4321');

INSERT INTO Fornecedor_Ingrediente (id_fornecedor, id_ingrediente, preco_fornecido) VALUES
(1, 1, 9.00),
(1, 2, 3.20),
(2, 3, 1.80);

INSERT INTO Login_Funcionario (id_funcionario, username, senha, ultimo_login) VALUES
(1, 'ana.lima', 'scrypt:32768:8:1$6qs2hxVpWi4R6uix$8d05ee434d16f24cf26b59dc0c9ead2a074898885993ec69fe7d28feb221b27b49b763bb16121b9e12877335da175d8cbbfdc2835c9ac7170db77ff69d121889', '2024-07-21 10:00:00'),
(2, 'paulo.goncalves', 'scrypt:32768:8:1$w1FbFR8inKTaaQE8$6a51dc806ae727890831100c16eb636c43566ef59d7f514207f556ed17f988882d29944f340e8c7aaceb1232646a6482940363e868d534c54e6949b70bd7d9dc', '2024-07-21 11:00:00'),
(3, 'mariana.costa', 'scrypt:32768:8:1$ODkQ0n7TULBkwB8a$d811da4e5a136a4e1ab9d0cccc314c74324c948b32cc1b04e9525b9df906d0fe792c0c3305c2315522d8e4babaaf89ff8cf35014acf4cad6bf468cb0eec5f4ad', '2024-07-21 12:00:00');
