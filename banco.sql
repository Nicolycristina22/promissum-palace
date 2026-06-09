
CREATE DATABASE IF NOT EXISTS promissum_palace;
USE promissum_palace;


CREATE TABLE IF NOT EXISTS hospede (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100)  NOT NULL,
    documento       VARCHAR(20)   NOT NULL,
    email           VARCHAR(100),
    telefone        VARCHAR(20),
    endereco        VARCHAR(150),
    cidade          VARCHAR(50),
    estado          VARCHAR(2),
    cep             VARCHAR(10),
    nacionalidade   VARCHAR(50),
    data_nascimento DATE
);


CREATE TABLE IF NOT EXISTS quarto (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    numero       INT            NOT NULL,
    tipo         VARCHAR(20),
    preco        DECIMAL(10,2),
    capacidade   INT,
    descricao    TEXT,
    andar        INT,
    tem_varanda  BOOLEAN,
    tem_banheira BOOLEAN,
    area_m2      DECIMAL(6,2),
    amenidades   TEXT
);


CREATE TABLE IF NOT EXISTS usuario (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nome      VARCHAR(100) NOT NULL,
    documento VARCHAR(20)  NOT NULL,
    email     VARCHAR(100) NOT NULL UNIQUE,
    senha     VARCHAR(255) NOT NULL,
    role      VARCHAR(20)  NOT NULL DEFAULT 'hospede',
    telefone  VARCHAR(20),
    endereco  VARCHAR(150),
    cidade    VARCHAR(50),
    estado    VARCHAR(2),
    cep       VARCHAR(10),
    nacionalidade VARCHAR(50),
    data_nascimento DATE
);

INSERT IGNORE INTO usuario (nome, documento, email, senha, role, telefone, endereco, cidade, estado, cep, nacionalidade)
VALUES
  ('Carlos Mendes', '111.111.111-11', 'gerente@promissum.com',
   '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',
   'gerente', '(11) 91111-1111', 'Av. Paulista, 1000', 'São Paulo', 'SP', '01310-100', 'Brasileiro'),
  ('Ana Souza', '222.222.222-22', 'funcionario@promissum.com',
   '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',
   'funcionario', '(11) 92222-2222', 'Rua Augusta, 500', 'São Paulo', 'SP', '01305-000', 'Brasileira');


CREATE TABLE IF NOT EXISTS reserva (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    hospede_id      INT            NOT NULL,
    quarto_id       INT            NOT NULL,
    check_in        DATE           NOT NULL,
    check_out       DATE           NOT NULL,
    status          VARCHAR(20)    NOT NULL DEFAULT 'Ativo',
    total_diarias   INT            NOT NULL,
    valor_total     DECIMAL(10,2)  NOT NULL,
    observacao      TEXT,
    forma_pagamento VARCHAR(30)    NOT NULL DEFAULT 'PIX',
    FOREIGN KEY (hospede_id) REFERENCES hospede(id),
    FOREIGN KEY (quarto_id)  REFERENCES quarto(id)
);


CREATE TABLE IF NOT EXISTS reserva_servico (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id  INT         NOT NULL,
    servico_key VARCHAR(50) NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES reserva(id) ON DELETE CASCADE
);
