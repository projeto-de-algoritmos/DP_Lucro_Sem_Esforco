import os
from dotenv import load_dotenv
import random
import math

from src.util import *

load_dotenv()

currencies = ["USD", "AUD", "BTC", "EUR", "GBP", "JPY", "BRL", "ETH"]


class Ativo:
    nome: str
    moeda: str
    unidades_por_moeda: str

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"Ativo<{self.nome}, custa {round(self.unidades_por_moeda,2)} de {self.moeda}>"


class Mercado:
    original: dict
    ativos: dict[str, Ativo]

    def __init__(self, arquivo: str = None):
        if arquivo is None:
            arquivo = os.getenv("TICKERS_FILE")
        self.original = read_json(arquivo)
        self.ativos = {}

        for item in self.original["results"]:
            name = item["ticker"]
            currency = random.choice(currencies)
            preco = random.random() * 10 ** random.randint(0, 3)

            ativo = Ativo()
            ativo.moeda = currency
            ativo.nome = name
            ativo.unidades_por_moeda = preco

            self.ativos[name] = ativo

    def novo_dia(self, min_variacao=0, max_variacao=0.01):
        for ativo in self.ativos.values():
            preco = ativo.unidades_por_moeda
            dt = max_variacao - min_variacao
            rand_val = 2.0 * random.random() - 1.0
            variacao_final = rand_val * dt * preco
            ativo.unidades_por_moeda = preco + variacao_final
            # print(
            #     f"variando por {variacao_final} ({round(math.fabs(variacao_final)/preco,4)} %), dt={dt} rand={rand_val} preco={preco}"
            # )

    # gera novos valores de mercado
    def get_mercado(self) -> dict[str, Ativo]:
        return self.ativos.copy()


if __name__ == "__main__":
    mercado = Mercado()
    print(list(mercado.get_mercado().values())[0:3])
    mercado.novo_dia()
    print(list(mercado.get_mercado().values())[0:3])
