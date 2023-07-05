import random
import math

INF = 1e9
INEXPLORADO = 0
VISITADO = 1
EXPLORADO = 2
MIN_DIFF = 0.001


def makeindx(c):
    return ord(c) - ord("A")


def get_indx(i):
    return chr(ord("A") + i)


def calc2(n):
    global g, s, precos, estado, pai, contafinal
    old_estado = estado[n]

    if estado[n] == EXPLORADO:
        return

    if estado[n] == VISITADO:
        estado[n] = EXPLORADO

    if estado[n] == INEXPLORADO:
        estado[n] = VISITADO

    solucao_parcial = None

    for filho, preco_compra in g[n]:
        if estado[filho] == EXPLORADO:
            continue

        # disputa
        c = precos[n] / preco_compra
        if math.fabs(c - precos[filho]) > MIN_DIFF:
            # print(
            #     "comprando de",
            #     get_indx(n),
            #     "para",
            #     get_indx(filho),
            #     "de",
            #     precos[filho],
            #     "para",
            #     c,
            # )
            antigo = precos[filho]
            precos[filho] = c
            if filho != s:
                cs = calc2(filho)
                if cs is not None:
                    # encontrou resultado final no parcial
                    # print(f"achou solucao no {n} com {filho}")
                    solucao_parcial = cs
            else:
                # encontrou resultado final
                # print(f"achou solucao final no {n} com {filho}")
                solucao_parcial = [s]

        elif estado[filho] == INEXPLORADO:
            # print("explora filho", filho)
            if filho != s:
                calc2(filho)

    estado[n] = old_estado
    if estado[n] == INEXPLORADO:
        estado[n] = VISITADO

    if solucao_parcial is None:
        # print(get_indx(n), "return sem solucao ")
        return None
    solucao_parcial = [n] + solucao_parcial
    # print(get_indx(n), "return solucao ", solucao_parcial)
    return solucao_parcial


def call_calc2(vg, vs):
    global g, s, precos, estado, pai

    g = vg
    s = vs
    precos = [-INF for _ in range(len(g))]
    precos[s] = 1
    estado = [INEXPLORADO for _ in range(len(g))]
    pai = [None for _ in range(len(g))]

    sol = calc2(s)
    return precos, sol


def add_arestas(g, size=None, max_size=None):
    if max_size is None:
        max_size = 100
    if size is None:
        size = random.randint(len(g), max_size)
    remains = size - len(g)
    initsz = len(g)

    for k in range(remains):
        i = k + initsz
        arestas = random.randint(2, 5)
        l = []
        v = random.random()
        l.append((random.randint(1, len(g) - 1), v))
        g[random.randint(1, len(g) - 1)].append((i, 1 / v))
        for _ in range(arestas):
            l.append((random.randint(0, len(g) - 1), random.random()))
        g.append(l)

    return g


def calcular_caminho_lucrativo(i_g=None, i_s=None):
    global g, s, precos, estado, pai
    if i_g is None:
        g = [
            [("B", 0.5)],
            [("C", 0.5), ("D", 0.5)],
            [("D", 1), ("E", 2.1)],
            [("C", 1), ("A", 4)],
            [("B", 1)],
        ]
    else:
        g = i_g
    if i_s is None:
        s = 0
    else:
        s = i_s

    for e in range(len(g)):
        for v in range(len(g[e])):
            g[e][v] = (makeindx(g[e][v][0]), 1.0 / g[e][v][1])

    ret, sol = call_calc2(g, s)
    vsol = [get_indx(i) for i in sol]

    print("fator final: ", ret[s])
    print("solucao: ", vsol)

    return ret[s], sol


calcular_caminho_lucrativo()
