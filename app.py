import threading
from os.path import exists


config = {
    "arquivo_grafo_mercado": "grafo_mercado.json",
    "arquivo_carteira": "carteira.json",
}


class Grafo:
    class Node:
        pass

    nodes: list[Node]
    file: str

    def __init__(self, file: str):
        self.file = file

        if exists(file):
            with open(file, 'w') as f:
                

    def from_json(self):
        pass

    def to_json(self) -> str:
        pass

    def add_edge(self):
        pass

    def add_node(self):
        pass

    def get_negative_cycles(self):
        pass


class Carteira:
    file: str

    # fração de aposta
    aposta_usd: float

    # banca atual em dólares
    banca_usd: float

    ativos: dict[str, int]

    def __init__(self, file: str):
        self.file = file

    def from_json(self):
        pass

    def to_json(self) -> str:
        pass

    def setup(self, aposta: float, banca: float):
        self.aposta_usd = aposta
        self.banca_usd = banca
        self.ativos = {"USD": banca}


def monitora_carteira():
    pass


def monitora_mercado():
    pass


def main():
    grafo_mercado = Grafo(file=config["arquivo_grafo_mercado"])
    carteira = Carteira(file=config["arquivo_carteira"])

    threading.Thread(
        procedure=monitora_mercado,
        args=(grafo_mercado),
        deamon=True,
    )

    threading.Thread(
        procedure=monitora_carteira,
        args=(carteira),
        deamon=True,
    )
