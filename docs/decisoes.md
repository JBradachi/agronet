# Decisões importantes

## Table of contents

- [Decisões importantes](#decisões-importantes)
  - [Table of contents](#table-of-contents)
  - [Representação Externa de dados](#representação-externa-de-dados)
  - [Mensagens enviadas ao banco](#mensagens-enviadas-ao-banco)

## Representação Externa de dados

Vamos usar o formato JSON.

## Mensagens enviadas ao banco

O JSON enviado deverá ter dois campos: `consulta` e `parametros`. O campo
`consulta` deverá conter a consulta SQL com quaisquer parâmetros substituídos
por `?`. O atributo `parâmetros` deverá conter a lista de parâmetros, na ordem
em que devem ser substituídos na consulta.

A ideia desse _design_ é previnir injeções de SQL.
