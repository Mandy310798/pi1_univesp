CREATE TABLE charity (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    criado_em DATE NOT NULL
);

CREATE TABLE donation (
	id INT AUTO_INCREMENT PRIMARY KEY,
    charity_id INT,
    FOREIGN KEY (charity_id) REFERENCES charity(id),
    agencia_bancaria VARCHAR(20) NOT NULL,
    conta_corrente VARCHAR(20) NOT NULL,
    valor_doacao DECIMAL(10, 2) NOT NULL,
    confirmacao BOOLEAN NOT NULL
);