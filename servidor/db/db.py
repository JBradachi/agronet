import sqlite3

def execute_sql_file(db_cursor: sqlite3.Cursor, path: str):
    with open(path, "r") as sql_file:
        script = sql_file.read()
        db_cursor.executescript(script)

# Cria as tabelas previstas no projeto de banco de dados, com seus devidos
# atributos, caso ainda não existam. Usa o script setup_db.sql
def setup_database(db_cursor: sqlite3.Cursor):
    execute_sql_file(db_cursor, "./db/setup_db.sql")

