# Decisões importantes

## Table of contents

- [Decisões importantes](#decisões-importantes)
  - [Table of contents](#table-of-contents)
  - [Representação Externa de dados](#representação-externa-de-dados)
  - [Mensagens enviadas ao banco](#mensagens-enviadas-ao-banco)
  - [Mensagens de resposta do servidor](#mensagens-de-resposta-do-servidor)
    - [Resposta login](#resposta-login)
  - [Mensagens de requisição do cliente](#mensagens-de-requisição-do-cliente)
    - [Requisição login](#requisição-login)

## Representação Externa de dados

Vamos usar o formato JSON.

## Mensagens enviadas ao banco

O JSON enviado deverá ter dois campos: `consulta` e `parametros`. O campo
`consulta` deverá conter a consulta SQL com quaisquer parâmetros substituídos
por `?`. O atributo `parâmetros` deverá conter a lista de parâmetros, na ordem
em que devem ser substituídos na consulta.

A ideia desse _design_ é previnir injeções de SQL.

## Mensagens de resposta do servidor

### Resposta login

O JSON enviado como resposta consiste em um unico campo `token`.
Esse campo será preenchido ou com um token URL de 32 caracteres,
ou false se não foi possível validar a requisição.

## Mensagens de requisição do cliente

Todas as mesagens de requisição do cliente deverão possuir o campo
`tipo_pedido` com seu devido valor como documentado a seguir.

### Requisição login

O JSON enviado para a requisição de login é composto por três campos:
`tipo_pedido`, `nome` e `senha`.

- `tipo_pedido` para essa requisição será _"login"_
- `nome` e `senha` são os valores passados para a validação.
