from threading import Thread 
import socket
import db
import sqlite3

class Connection:

    def __init__(self, conn, addr):
        try:
            self.conn = conn
            self.addr_cliente = addr
            tread = Thread(target=self.run)
            tread.start()
        except:
            print("erro na criação da tread")
            exit(3)

    def run(self):
        try:
            conn_db = sqlite3.connect('./db/agronet.db')
            cursor = conn_db.cursor()
            teste = cursor.execute("SELECT * FROM Usuario").fetchall()
        except:
            print("erro ao criar o cursor")
            exit(4)
        
        try:

            print(f"Conexão recebida de {self.addr_cliente}")

            nome = self.conn.recv(1024).decode()
            
            resposta = f"roi {nome}, né?{teste}"
            self.conn.sendall(resposta.encode())
            cursor.close()
            self.conn.close()
        except:
            print("erro na tread de resposta")
            exit(5)
