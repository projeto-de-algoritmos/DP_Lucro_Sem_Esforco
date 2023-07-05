import math


def get_indx(i):
    return chr(ord("A") + i)


def print_v(v):
    print("--------------------------------")
    print(*[get_indx(i) for i in range(len(v))], sep="\t")
    print(*[round(x, 2) for x in v], sep="\t")


node_to_node = [
    [1, 2, 3],
    [0.5, 1, 1.2],
    [0.3333, 0.83333, 1],
]


v = [10, 0, 0]
convs = [
    [10, 0, 2],
    [None, 2, 1],
    [None, 1, 0],
]


def conv(unit, ca, cb, n2n=node_to_node):
    return unit * n2n[cb][ca]


def apply_convs(v, convs):
    for c in convs:
        unit, ca, cb = c
        if unit is None:
            unit = v[ca]
        if v[ca] < unit:
            print(f"error! not enough {ca} for conversion")
            print(f"       needs {unit} but only has {v[ca]}")
            break
        v[ca] -= unit
        v[cb] += conv(unit, ca, cb)
    return v


min_err = 1e-2


# [TODO] assume que todos os nós podem ser convertidos em todos os outros
def get_new_graph(n2n, s=0):
    sz = len(n2n)
    new_graph = [[1 for _ in range(sz)] for _ in range(sz)]
    initsum = 0
    for i in range(sz):
        initsum += n2n[s][i]
    print(f"initsum: {initsum}")

    for i in range(len(n2n)):
        for j in range(len(n2n)):
            lbl = f"{get_indx(i)} -> {get_indx(j)}"
            convs = [
                [None, i, j],
            ]
            ret = apply_convs([1, 1, 1], convs)
            for k in range(len(n2n)):
                if k == s:
                    continue
                ret = apply_convs(ret, [[None, k, s]])

            diff = ret[s] - initsum
            if math.fabs(diff) > min_err:
                pass
                # if diff > 0:
                #     print(f"gain step {lbl}")
                # else:
                #     print(f"lose step {lbl}")
            else:
                ret[s] = initsum

            print(f"- {lbl}: {round(100*(ret[s]/initsum - 1.0),4)}%")

    return new_graph


get_new_graph(node_to_node)
