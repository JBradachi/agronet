# agronet

Repositório dedicado ao desenvolvimento do trabalho pratico de sistemas distribuídos

## Table of contents

- [agronet](#agronet)
  - [Table of contents](#table-of-contents)
  - [Execução](#execução)
    - [Com makefile](#com-makefile)
    - [Com docker (descontinuado)](#com-docker-descontinuado)
  - [Organização](#organização)
    - [banco](#banco)
    - [cliente](#cliente)
    - [docs](#docs)
    - [protocolo](#protocolo)
    - [servidor](#servidor)

## Execução

### Com makefile

Agora precisamos rodar apenas o comando:

```bash
make -j 4
```

No diretório raiz do projeto.

### Com docker (descontinuado)

Para executar o sistema distribuído, basta configurar o host da máquina com o seguinte comando:

```bash
xhost +local:*
```

e subir o conteiner docker com o seguinte comando:

```bash
sudo docker compose up
```

fique a vontade para criar um usuário novo no nosso marketpace :)

mas se quiser usar um usuário já cadastrado, segue abaixo alguns:

- **login:** admin **senha:** admin

- **login:** donoDaCeleiro **senha:** celeiro

- **login:** usuarioSemLoja **senha:** semloja

## Organização

Nosso repositório é organizado em 5 pastas principais e um arquivo docker compose que inicia todos os conteiners.

### banco

Diretório dedicado ao desenvolvimento do servidor de dados.

### cliente

Diretório dedicado ao desenvolvimento do backend do cliente e da interface.

### docs

Diretório dedicado para documentações que auxiliarão na construção do relatório.

### protocolo

Diretório dedicado para o desenvolvimento de uma classe que irá gerenciar a comunicação.

### servidor

Diretório dedicado ao desenvolvimento do servidor de dados.

