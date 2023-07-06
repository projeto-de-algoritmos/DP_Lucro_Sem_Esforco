import threading
import os
import random
from os.path import exists
from dotenv import load_dotenv
import http.server

from src.util import *
from src.gerar_mercado import Mercado, currencies as std_moedas
from src.grafo import calcular_caminho_lucrativo

load_dotenv()

config = {
    "arquivo_grafo_mercado": "sample_reqs/polygon-tickers.json",
}

random_binario = lambda: random.random() > 0.5


class Edge:
    node_out: "Node"
    node_in: "Node"
    weight: float


class Node:
    id: int
    name: str
    out_edges: Edge
    in_edges: Edge


class Grafo:
    nodes: dict[str, Node]
    edges: list[Edge]
    __node_names: set[str]
    __node_id: dict[str, int]
    __node_id_inv: dict[int, str]
    __last_id: int

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = []
        self.__node_names = set()
        self.__node_id = {}
        self.__node_id_inv = {}
        self.__last_id = 0

    def add_edge(self, node_in: str, node_out: str, weight: float):
        if node_in not in self.__node_names:
            raise ValueError(f"Node {node_in} not in graph")
        if node_out not in self.__node_names:
            raise ValueError(f"Node {node_out} not in graph")

        e = Edge()
        e.node_in = node_in
        e.node_out = node_out
        e.weight = weight

        self.edges.append(e)

        return e

    def add_node(self, name: str):
        self.__node_names.add(name)
        n = Node()
        n.name = name
        self.nodes[name] = n

        self.__last_id += 1
        n.id = self.__last_id - 1

        self.__node_id[name] = n.id
        self.__node_id_inv[n.id] = name

        return n

    def size(self) -> int:
        return len(self.nodes)

    def edges_size(self) -> int:
        return len(self.edges)

    def get_node_name(self, id: int) -> str:
        return self.__node_id_inv[id]

    def as_2d_list(self) -> list[list[tuple[int, float]]]:
        g = [[] for _ in range(len(self.nodes))]

        for e in self.edges:
            nid = self.__node_id[e.node_in]
            o_nid = self.__node_id[e.node_out]
            g[nid].append((o_nid, e.weight))

        return g


def make_grafo_from_mercado(mercado: Mercado, max_size: int = None) -> Grafo:
    mercado_dict = mercado.get_mercado()
    grafo = Grafo()

    for moeda in std_moedas:  # USD, EUR, BRL, BTC... todas as moedas também são ativos
        grafo.add_node(moeda)

    for m1 in std_moedas:
        for m2 in std_moedas:
            if random_binario():
                v = random.random() * 2
                grafo.add_edge(m1, m2, v)
                grafo.add_edge(m2, m1, 1 / v)

    if max_size is None:
        max_size = len(mercado_dict)

    sz = 0

    for nome, ativo in mercado_dict.items():
        sz += 1
        if sz > max_size:
            break
        grafo.add_node(nome)

        qtd_moedas = random.randint(4, len(std_moedas) - 1)
        moedas = random.choices(std_moedas, k=qtd_moedas)

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


def test():
    grafo = Grafo()
    for n in ["A", "B", "C", "D", "E"]:
        grafo.add_node(n)

    grafo.add_edge("A", "B", 2)
    grafo.add_edge("B", "C", 2)
    grafo.add_edge("B", "D", 2)
    grafo.add_edge("C", "D", 1)
    grafo.add_edge("C", "E", 1 / 2.1)
    grafo.add_edge("D", "A", 1 / 4)
    grafo.add_edge("D", "C", 1)
    grafo.add_edge("E", "B", 1)

    g = grafo.as_2d_list()

    lucro, sol = calcular_caminho_lucrativo(i_g=g, i_s=0, should_print=False)
    sol = [grafo.get_node_name(i) for i in sol]

    assert lucro - 1.05 < 0.0001
    assert len(sol) >= 7 and len(sol) <= 8

    print(lucro, sol)


def init():
    global mercado, grafo
    mercado = Mercado(arquivo=config["arquivo_grafo_mercado"])
    grafo = make_grafo_from_mercado(mercado, max_size=0)


def make_grafo():
    global mercado, grafo

    mercado.novo_dia()
    grafo = make_grafo_from_mercado(mercado, max_size=0)

    g = grafo.as_2d_list()

    print(*g, sep="\n")

    lucro, sol = calcular_caminho_lucrativo(i_g=g, i_s=0, should_print=False)
    sol = [grafo.get_node_name(i) for i in sol]

    print(lucro, sol)

    return lucro, sol, g


class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, content_type="text/plain", status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_GET(self):
        if self.path == "/new":
            self._set_response("application/json")
            lucro, sol, g = make_grafo()
            data = {"lucro": lucro, "sol": sol, "g": g}
            response = json.dumps(data)
            self.wfile.write(response.encode("utf-8"))
        else:
            self._set_response()
            self.wfile.write(b"Hello, world!")


def main():
    init()

    server_address = ("0.0.0.0", 8000)
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    httpd.serve_forever()


main()
# test()
