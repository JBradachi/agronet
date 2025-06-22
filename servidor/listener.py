import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging as log
import Pyro5.api
from aplication_server import ServidorSD

HOST = "127.0.0.1"
PORT = 6000
log.basicConfig(level=log.INFO)

def main():
    try:
        daemon = Pyro5.server.Daemon()
        ns = Pyro5.api.locate_ns()
        uri = daemon.register(ServidorSD)
        ns.register("agronet.aplicacao", uri)
        log.info("Servidor de aplicação Pyro iniciado e registrado no NameServer.")
        daemon.requestLoop()
    except Exception as e:
        log.error("Erro ao iniciar o listener Pyro")
        log.error(e)

if __name__ == "__main__":
    main()
