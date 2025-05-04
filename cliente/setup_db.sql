-- Tabela de usuários: nome, senha
CREATE TABLE IF NOT EXISTS Usuario (
  id INTEGER AUTO_INCREMENT,
  nome TEXT NOT NULL,
  senha TEXT NOT NULL,
  PRIMARY KEY (id)
);

-- Tabela de lojas: nome, data de criação, cidade, UF, descrição
-- Cada loja é propriedade de um único usuário
CREATE TABLE IF NOT EXISTS Loja (
  id INTEGER AUTO_INCREMENT,
  usuario_dono INTEGER NOT NULL,

  nome TEXT NOT NULL,
  dia_criacao INTEGER NOT NULL,
  mes_criacao INTEGER NOT NULL,
  ano_criacao INTEGER NOT NULL,
  cidade TEXT NOT NULL,
  estado TEXT NOT NULL,
  descricao TEXT NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (usuario_dono) REFERENCES Usuario (id)
);

--------------------------------------------------------------------------------

-- Tabela de empresas: apenas o nome
CREATE TABLE IF NOT EXISTS Empresa (
  id INTEGER AUTO_INCREMENT,
  nome TEXT NOT NULL,
  PRIMARY KEY (id)
);

-- Tabela de modelos de máquina: nome, descrição
-- Cada modelo é produzido por uma empresa específica
CREATE TABLE IF NOT EXISTS Modelo (
  id INTEGER AUTO_INCREMENT,
  fabricante INTEGER AUTO_INCREMENT,

  nome TEXT NOT NULL,
  descricao TEXT NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (fabricante) REFERENCES Empresa (id)
);

-- Tabela de máquinas: preço e data de fabricação
-- Cada máquina corresponde a um modelo específico
-- Cada máquina é vendida por uma loja específica
CREATE TABLE IF NOT EXISTS Maquina (
  id INTEGER AUTO_INCREMENT,
  loja INTEGER NOT NULL,
  modelo INTEGER NOT NULL,

  preco REAL NOT NULL,
  mes_fabricacao INTEGER NOT NULL,
  ano_fabricacao INTEGER NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (loja) REFERENCES Loja (id),
  FOREIGN KEY (modelo) REFERENCES Modelo (id)
);
