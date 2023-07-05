import threading
import os
from os.path import exists
from dotenv import load_dotenv

from src.util import *
from src.gerar_mercado import Mercado, currencies as moedas

load_dotenv()

config = {
    "arquivo_grafo_mercado": "grafo_mercado.json",
    "arquivo_carteira": "carteira.json",
}


class Grafo:


    class Edge:
        node_out: Node
        node_in: Node

    class Node:
        name: str
        out_edges: Edge

    nodes: list[Node]

    def add_edge(self):
        pass

    def add_node(self, name: str):
        pass

    def get_negative_cycles(self, s, t):
        # Push-Based-Shortest-Path(G, s, t)
        inf = 1e10
        m = [    inf for _ in range(len(self.nodes))]
        sucessor = [    inf for _ in range(len(self.nodes))]
        m[t] = 0
        for i in range(1,len(self.node)):
            foreach node v V {
                foreach node w such that (v, w) E {
                    if (M[v] > M[w] + cvw) {
                        M[v] M[w] + cvw
                        successor[v] w
                    }
                }
            }
            foreach node v V {
                foreach node w such that (v, w) E {
                if (M[v] > M[w] + cvw) {   
                    Return ‘there is a negative cycle’
                }
            }


def make_grafo_from_mercado(mercado: Mercado) -> Grafo:
    mercado_dict = mercado.get_mercado()
    grafo = Grafo()

    for moeda in moedas:  # USD, EUR, BRL, BTC... todas as moedas também são ativos
        grafo.add_node(moeda)

    for nome, ativo in mercado_dict.items():
        grafo.add_node(nome)
        grafo.add_edge(ativo, ativo.moeda, ativo.unidades_por_moeda)
        grafo.add_edge(ativo, ativo.unidades_por_moeda, ativo.moeda)

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
