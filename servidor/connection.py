from threading import Thread 
import socket
import db
import sqlite3

class Connection:

    def __init__(self, conn, addr, conn_db):
        try:
            self.conn = conn
            self.addr_cliente = addr
            self.conn_db = conn_db
            tread = Thread(target=self.run)
            tread.start()
        except:
            print("erro na criação da tread")
            exit(3)

    def run(self):
        try:
            #cursor = self.conn_db.cursor()
            #teste = cursor.execute("SELECT * FROM Usuario").fetchall()
            pass
        except:
            print("erro ao criar o cursor")
            exit(4)
        
        try:

            print(f"Conexão recebida de {self.addr_cliente}")

            nome = self.conn.recv(1024).decode()
            
            resposta = f"roi {nome}, né?"
            self.conn.sendall(resposta.encode())

            self.conn.close()
        except:
            print("erro na tread de resposta")
            exit(5)
