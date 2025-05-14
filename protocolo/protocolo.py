import json, socket, struct

STRUCT_FORMAT = "!Q"
PAYLOAD_SIZE = struct.calcsize(STRUCT_FORMAT)

class JsonTSocket:
    """
    Uma JsonTSocket é uma embalagem sobre a classe padrão de socket do
    python. Seus métodos de envio e recebimento consideram que as mensagens
    serão dadas no padrão jsonT™. Toda mensagem nesse formato é um par
    (tamanho, JSON). O tamanho diz o número de bytes que o JSON ocupa e é
    dado com uma quantidade fixa de bytes.
    """

    def __init__(self, sock = None):
        if sock: self.socket = sock; return
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))

    def listen(self):
        self.socket.listen()

    def accept(self):
        sock, addr = self.socket.accept()
        return JsonTSocket(sock), addr
    
    def bind(self, host, port):
        self.socket.bind((host, port))

    # Envia um dicionário qualquer no formato jsonT
    def send_dict(self, data: dict):
        data_bin = json.dumps(data).encode()
        size = struct.pack(STRUCT_FORMAT, len(data_bin))
        self.socket.sendall(size + data_bin)

    # Recebe uma mensagem no format jsonT e retorna o dicionário correspodente
    def recv_dict(self) -> dict:
        msg_size = self.socket.recv(PAYLOAD_SIZE)
        if not msg_size: return {} # resposta vazia
        msg_size = struct.unpack(STRUCT_FORMAT, msg_size)[0]

        data_str = self.socket.recv(msg_size).decode()
        if not data_str: return {} # resposta vazia
        return json.loads(data_str)