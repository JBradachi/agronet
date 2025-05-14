import json, socket, struct

STRUCT_FORMAT = "!Q"
PAYLOAD_SIZE = struct.calcsize(STRUCT_FORMAT)

class JsonTSocket(socket.socket):
    """
    Uma JsonTSocket é uma embalagem sobre a classe padrão de socket do
    python. Seus métodos de envio e recebimento consideram que as mensagens
    serão dadas no padrão jsonT™. Toda mensagem nesse formato é um par
    (tamanho, JSON). O tamanho diz o número de bytes que o JSON ocupa e é
    dado com uma quantidade fixa de bytes.
    """

    # Envia um dicionário qualquer no formato jsonT
    def send_dict(self, data: dict) -> bytes:
        data_bin = json.dumps(data).encode()
        size = struct.pack(STRUCT_FORMAT, len(data_bin))
        return size + data_bin

    # Recebe uma mensagem no format jsonT e retorna o dicionário correspodente
    def recv_dict(self) -> dict:
        msg_size = self.socket.recv(PAYLOAD_SIZE)
        if not msg_size: return {} # resposta vazia
        msg_size = struct.unpack(STRUCT_FORMAT, msg_size)[0]

        data_str = self.recv(msg_size).decode()
        if not data_str: return {} # resposta vazia
        return json.loads(data_str)
