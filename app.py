import threading
import os
import random
from os.path import exists
from dotenv import load_dotenv

from src.util import *
from src.gerar_mercado import Mercado, currencies as moedas

load_dotenv()

config = {
    "arquivo_grafo_mercado": "grafo_mercado.json",
    "arquivo_carteira": "carteira.json",
}

random_binario = lambda: random.random() > 0.5


class Edge:
    node_out: "Node"
    node_in: "Node"
    weight: float


class Node:
    name: str
    out_edges: Edge
    in_edges: Edge


class Grafo:
    nodes: dict[str, Node]
    edges: list[Edge]
    __node_names: set[str]

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = []
        self.__node_names = set()

    def add_edge(self, node_in: str, node_out: str, weight: float):
        if node_in not in self.__node_names:
            raise ValueError(f"Node {node_in} not in graph")
        if node_out not in self.__node_names:
            raise ValueError(f"Node {node_out} not in graph")

        e = Edge()
        e.node_in = node_in
        e.node_out = node_out
        e.weight = weight

        return e

    def add_node(self, name: str):
        self.__node_names.add(name)
        n = Node()
        n.name = name
        self.nodes[name] = n
        return n

    def size(self) -> int:
        return len(self.nodes)

    def edges_size(self) -> int:
        return len(self.edges)

    def as_2d_list(self) -> list[list[tuple[int, float]]]:
        g = [[] for _ in range(len(self.nodes))]


def make_grafo_from_mercado(mercado: Mercado) -> Grafo:
    mercado_dict = mercado.get_mercado()
    grafo = Grafo()

    for moeda in moedas:  # USD, EUR, BRL, BTC... todas as moedas também são ativos
        grafo.add_node(moeda)

    for nome, ativo in mercado_dict.items():
        grafo.add_node(nome)

        qtd_moedas = random.randint(1, len(moedas) - 1)
        moedas = random.choices(moedas, k=qtd_moedas)

        for moeda in moedas:
            preco = ativo.unidades_por_moeda
            if random_binario():
                grafo.add_edge(nome, ativo.moeda, preco)
            if random_binario():
                grafo.add_edge(ativo.moeda, nome, 1.0 / preco)

    return grafo


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
    mercado = Mercado()

    # grafo_teste = [
    #     [1, 2, 3, None],
    #     [0.5, 1, 1.2, 1.2],
    #     [0.3333, 0.83333, 1, 1],
    #     [None, 0.83333, 1, 1],
    # ]
    grafo = make_grafo_from_mercado(mercado)

    print(grafo.as_2d_list())

    # grafo_mercado = Grafo(file=config["arquivo_grafo_mercado"])
    # carteira = Carteira(file=config["arquivo_carteira"])


main()
