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
  imagem TEXT NOT NULL,
  preco REAL NOT NULL,
  mes_fabricacao INTEGER NOT NULL,
  ano_fabricacao INTEGER NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (loja) REFERENCES Loja (id),
  FOREIGN KEY (modelo) REFERENCES Modelo (id)
);

INSERT IGNORE INTO `Usuario` (`nome`, `senha`) VALUES
  ('admin', 'admin')

INSERT IGNORE INTO `Loja` (`usuario_dono`, `nome`, `dia_criacao`, `mes_criacao`, `ano_criacao`, `cidade`, `estado`, `descricao`) VALUES
  ('admin', 'adminStore', 12, 2, 2004, 'Fernandópolis', 'SP', 'Loja de colheitadeiras de café')

INSERT IGNORE INTO `Empresa` (`nome`) VALUES
  ('CAT')

INSERT IGNORE INTO `Modelo` (`fabricante`, `nome`, `descricao`) VALUES
  (1, 'Challenger MT525D 4WD', 'Linha de produto:	tratores agrícolas, Número de série	D049045, Número de catálogo	473575')

INSERT IGNORE INTO `Maquina` (`loja`, `modelo`, `imagem`, `preco`, `mes_fabricacao`, `ano_fabricacao`) VALUES
  (1, 1, 'static/CAT1.png', 394.23, 2, 2013)

  -- Horas de utilização	5.200 h 
  -- Localização da máquina	Mexicali, Mexico