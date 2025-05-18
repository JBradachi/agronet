-- Tabela de lojas: nome, data de criação, cidade, UF, descrição
CREATE TABLE IF NOT EXISTS Loja (
  nome TEXT NOT NULL,
  dia_criacao INTEGER NOT NULL,
  mes_criacao INTEGER NOT NULL,
  ano_criacao INTEGER NOT NULL,
  cidade TEXT NOT NULL,
  estado TEXT NOT NULL,
  descricao TEXT NOT NULL,
  PRIMARY KEY (nome)
);

-- Tabela de usuários: nome, senha, loja
CREATE TABLE IF NOT EXISTS Usuario (
  nome TEXT NOT NULL,
  senha TEXT NOT NULL,
  loja TEXT, -- opcional
  PRIMARY KEY (nome),
  FOREIGN KEY (loja) REFERENCES Loja (nome)
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
  fabricante TEXT NOT NULL,
  nome TEXT NOT NULL,
  descricao TEXT NOT NULL,

  PRIMARY KEY (nome),
  FOREIGN KEY (fabricante) REFERENCES Empresa (nome)
);

-- Tabela de máquinas: preço e data de fabricação
-- Cada máquina corresponde a um modelo específico
-- Cada máquina é vendida por uma loja específica
CREATE TABLE IF NOT EXISTS Maquina (
  id INTEGER PRIMARY KEY, -- AUTO_INCREMENT por padrão
  loja TEXT NOT NULL,
  modelo TEXT NOT NULL,
  imagem TEXT NOT NULL,
  preco REAL NOT NULL,
  mes_fabricacao INTEGER NOT NULL,
  ano_fabricacao INTEGER NOT NULL,
  visivel INTEGER DEFAULT 1 NOT NULL,
  quantidade INTEGER NOT NULL,

  FOREIGN KEY (loja) REFERENCES Loja (nome),
  FOREIGN KEY (modelo) REFERENCES Modelo (nome)
);

INSERT INTO Loja (nome, dia_criacao, mes_criacao, ano_criacao,
  cidade, estado, descricao) VALUES
  ('adminStore', 12, 2, 2004,
    'Fernandópolis', 'SP', 'Loja de colheitadeiras de café'),
  ('Celeiro', 21, 7, 1994,
    'Florestal', 'MG', 'Loja de tratores'),
  ('Damasco', 21, 7, 1500,
    'Florestal', 'MG', 'Loja de plantadeiras');

INSERT INTO Usuario (nome, senha, loja ) VALUES
  ('admin', 'admin', 'adminStore' ),
  ('donoDaCeleiro', 'celeiro', 'Celeiro' ),
  ('usuarioSemLoja', 'semloja', NULL);

INSERT INTO Empresa (nome) VALUES
  ('CAT'),
  ('Baldan'),
  ('CaseIH');

INSERT INTO Modelo (fabricante, nome, descricao) VALUES
  ('CAT', 'Challenger MT525D 4WD',
    'Linha de produto:	tratores agrícolas, Número de série	D049045, Número de catálogo	473575'),
  ('CAT', 'Escavadeira Hidráulica de Mineração 6015',
    'A Escavadeira Hidráulica de Mineração Cat® 6015 permite que você movimente mais material por um custo mais baixo, para que você possa atingir as metas de produção, cumprir os compromissos e prazos e maximizar a lucratividade. Com capacidade de carregamento de ferramentas líder da categoria, durabilidade aprimorada e o motor mais potente da categoria, a Cat 6015 gera mais produtividade e eficiência de combustível do que outras escavadeiras. E é oferecida com mais e melhores opções que permitem que você combine a máquina com sua operação – desde acesso e pacotes de clima frio até várias opções de braço e trackpad. Além disso, uma grande variedade de caçambas está disponível, proporcionando carga útil ideal e eficiência da máquina para sua operação. E a alta capacidade de carga da 6015 permite que você use caçambas grandes e movimente mais em menos ciclos.'),
  ('Baldan', 'Semeadora Linha PLB',
    'A Semeadora de Linhas PLB possui chassi de viga tubular, discos duplos ou sulcador-riscador no adubo e discos duplos na semente. Distribuicao de adubo por rosca helicoidal, semeia com precisao as culturas de verao. Possui tambem um sistema de roda compactadora individual para cobertura da semente.'),
  ('CaseIH', 'Coffee Express Multi',
    'A colhedora Coffee Express 200 Multi é equipada com o motor FPT, com controle eletrônico de malha fechada dos circuitos de agitação e freio. As rotações de agitação e agressão se mantêm constantes durante todo o tempo, devido ao acréscimo de potência, aliada à maior precisão do controle.');

INSERT INTO Maquina (loja, modelo, imagem, preco, mes_fabricacao, ano_fabricacao, quantidade) VALUES
  ("adminStore", "Challenger MT525D 4WD", 'CAT1.png', 394.23, 2, 2013, 2),
  ("adminStore", "Coffee Express Multi", 'CaseIH1.png', 550000.00, 12, 2023, 4),
  ("adminStore", "Escavadeira Hidráulica de Mineração 6015", 'CAT2.png', 1550000.00, 5, 2025, 1),
  ("Damasco", "Coffee Express Multi", 'CaseIH1.png', 550000.00, 12, 2023, 4),
  ("Damasco", "Semeadora Linha PLB", 'CAT2.png', 38025.00, 2, 2015, 6),
  ("Celeiro", "Coffee Express Multi", 'CaseIH1.png', 550000.00, 12, 2023, 3),
  ("Celeiro", "Escavadeira Hidráulica de Mineração 6015", 'CAT2.png', 1550000.00, 5, 2025, 2);
