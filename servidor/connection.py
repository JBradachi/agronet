from threading import Thread 

class Connection:

    def __init__(self, conn, addr):
        try:
            self.conn = conn
            self.addr_cliente = addr
            tread = Thread(target=self.run)
            tread.start()
        except:
            print("erro na criação da tread")
    
    def run(self):
        try:
            print(f"Conexão recebida de {self.addr_cliente}")

            nome = self.conn.recv(1024).decode()
            
            resposta = f"roi {nome}, né?"
            self.conn.sendall(resposta.encode())

            self.conn.close()
        except:
            print("erro na tread de resposta")
