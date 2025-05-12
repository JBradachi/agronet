-- Tabela de lojas: nome, data de criação, cidade, UF, descrição
CREATE TABLE IF NOT EXISTS Loja (
  id INTEGER AUTO_INCREMENT,

  nome TEXT NOT NULL,
  dia_criacao INTEGER NOT NULL,
  mes_criacao INTEGER NOT NULL,
  ano_criacao INTEGER NOT NULL,
  cidade TEXT NOT NULL,
  estado TEXT NOT NULL,
  descricao TEXT NOT NULL,

  PRIMARY KEY (id)
);

-- Tabela de usuários: nome, senha, loja
CREATE TABLE IF NOT EXISTS Usuario (
  id INTEGER AUTO_INCREMENT,
  nome TEXT NOT NULL,
  senha TEXT NOT NULL,
  loja INTEGER, -- pode ser nulo; usuário pode não ter uma loja ainda
  PRIMARY KEY (id),
  FOREIGN KEY (loja) REFERENCES Loja (id)
);

--------------------------------------------------------------------------------

-- Tabela de empresas: apenas o nome
CREATE TABLE IF NOT EXISTS Empresa (
  nome TEXT NOT NULL,
  PRIMARY KEY (nome)
);

-- Tabela de modelos de máquina: nome, descrição
-- Cada modelo é produzido por uma empresa específica
CREATE TABLE IF NOT EXISTS Modelo (
  id INTEGER AUTO_INCREMENT,
  fabricante INTEGER AUTO_INCREMENT,

  nome TEXT NOT NULL,
  descricao TEXT NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (fabricante) REFERENCES Empresa (nome)
);

-- Tabela de máquinas: preço e data de fabricação
-- Cada máquina corresponde a um modelo específico
-- Cada máquina é vendida por uma loja específica
CREATE TABLE IF NOT EXISTS Maquina (
  id INTEGER AUTO_INCREMENT,
  loja INTEGER NOT NULL,
  modelo INTEGER NOT NULL,
  imagem TEXT NOT NULL,
  preco REAL NOT NULL,
  mes_fabricacao INTEGER NOT NULL,
  ano_fabricacao INTEGER NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (loja) REFERENCES Loja (id),
  FOREIGN KEY (modelo) REFERENCES Modelo (id)
);

INSERT INTO `Loja` (`id`, `nome`, `dia_criacao`, `mes_criacao`, `ano_criacao`, `cidade`, `estado`, `descricao`) VALUES
  (1, 'adminStore', 12, 2, 2004, 'Fernandópolis', 'SP', 'Loja de colheitadeiras de café');

INSERT INTO `Usuario` (`nome`, `senha`, `loja` ) VALUES
  ('admin', 'admin', 1 );

INSERT INTO `Empresa` (`nome`) VALUES
  ('CAT');

INSERT INTO `Modelo` (`fabricante`, `nome`, `descricao`) VALUES
  ('CAT', 'Challenger MT525D 4WD', 'Linha de produto:	tratores agrícolas, Número de série	D049045, Número de catálogo	473575');

INSERT INTO `Maquina` (`loja`, `modelo`, `imagem`, `preco`, `mes_fabricacao`, `ano_fabricacao`) VALUES
  (1, 1, 'static/CAT1.png', 394.23, 2, 2013);

  -- Horas de utilização	5.200 h 
  -- Localização da máquina	Mexicali, Mexico
