# agronet

Repositório dedicado ao desenvolvimento do trabalho pratico de sistemas distribuídos

## Table of contents

- [agronet](#agronet)
  - [Table of contents](#table-of-contents)
  - [TODO List](#todo-list)

## TODO List

- [X] Banco de dados (SQLite) *se tiver tempo separar do Servidor (não tivemos mas fizemos)
- [ ] Cliente
  - [X] Estrutura dos arquivos
  - [ ] Pensar na interface gráfica
    - [ ] Tela de login / cadastro usuário (cadastro_usuario)
    - [ ] Cadastro de máquina (cadastro_maquina)
    - [ ] Cadastro de loja (cadastro_loja)
    - [ ] Pagina de loja vendedor (ligar/desligar exposição de anuncio)
    - [ ] Pagina de loja comprador
    - [ ] Pagina principal
    - [ ] Pagina de resultado pesquisa produto
    - [ ] Pagina de resultado pesquisa loja
    - [ ] Pagina do produto (botão de comprar)
    - [ ] Pagina de ajuda (ctt dos devs)
- [ ] Servidor
  - [X] Estrutura dos arquivos
  - [X] Uso de Threads (parcialmente feito)
- [ ] Estrura das mensagens (como acontecerá a conversa)
  - [ ] "Rotas de requisição"
    - [X] login (login)
    - [X] Cadastro de máquina (cadastro_produto) bradas
    - [X] Cadastro de loja (cadastro_loja) dudu
    - [ ] Cadastro usuário (cadastro_usuario) dudu
    - [X] Edita máquina (edita_produto) dudu
    - [ ] Pagina principal
      - [ ] get lojas (tipo pedido mostra_lojas, filtro) bradas
      - [ ] get produtos (tipo pedido mostras_produtos, filtro, opcional loja) dudu
    - [ ] Pagina produto (info_produto/ imagens_produto) bradas
  - [ ] "Rotas de resposta"
- [X] Docker

comando para rodar corretamente no ubuntu

```bash
xhost +local:*
```
