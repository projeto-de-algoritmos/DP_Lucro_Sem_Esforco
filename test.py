import math


def get_indx(i):
    return chr(ord("A") + i)


def print_v(v):
    print("--------------------------------")
    print(*[get_indx(i) for i in range(len(v))], sep="\t")
    print(*[round(x, 2) for x in v], sep="\t")


inf = 1e9


def limpa_dataset(n2n):
    for s in range(len(n2n)):
        for i in range(len(n2n)):
            if n2n[i][s] is not None:
                continue
            n2n[i][s] = inf
            n2n[s][i] = inf
            print("trying", s, i)
            for j in range(len(n2n)):
                if (
                    s == j
                    or n2n[s][j] is None
                    or n2n[j][s] is None
                    or n2n[i][j] is None
                    or n2n[j][i] is None
                ):
                    continue
                n2n[s][i] = min(n2n[s][i], n2n[s][j] * n2n[j][i])
                n2n[i][s] = min(n2n[i][s], n2n[i][j] * n2n[j][s])
                print("with node", j, "new price is", n2n[s][i], n2n[i][s])
    print(n2n)
    return n2n


def limpa_dataset2(i_n2n):
    n2n = [i_n2n[i].copy() for i in range(len(i_n2n))]
    for s in range(len(n2n)):
        for i in range(len(n2n)):
            for j in range(len(n2n)):
                if (
                    i == j
                    or j == s
                    or i == s
                    or n2n[s][j] is None
                    or n2n[j][s] is None
                    or n2n[i][j] is None
                    or n2n[j][i] is None
                    or n2n[s][i] is not None
                    or n2n[i][s] is not None
                ):
                    continue
                print(f"trying s={s}, i={i}, j={j}")
                n2n[i][s] = inf
                n2n[s][i] = inf
                newv = n2n[s][j] * n2n[j][i]
                newiv = n2n[i][j] * n2n[j][s]
                print(f"newv={newv}, newiv={newiv}")
                if newv < n2n[s][i]:
                    print(
                        f"price of {s} -> {j} is {n2n[s][j]}, {j} -> {i} is {n2n[j][i]}, thus {s} -> {i} is {newv}"
                    )
                    n2n[s][i] = newv
                if newiv < n2n[i][s]:
                    print(
                        f"price of {s} -> {j} is {n2n[s][j]}, {j} -> {i} is {n2n[j][i]}, thus {s} -> {i} is {newv}"
                    )
                    n2n[i][s] = newiv
                # n2n[s][i] = min(n2n[s][i], n2n[s][j] * n2n[j][i])
                # n2n[i][s] = min(n2n[i][s], n2n[i][j] * n2n[j][s])
                # print("with node", j, "new price is", n2n[s][i], n2n[i][s])
    print(n2n)
    return n2n


def conv(unit, ca, cb, n2n):
    return unit * n2n[cb][ca]


def apply_convs(v, convs, n2n):
    for c in convs:
        unit, ca, cb = c
        if unit is None:
            unit = v[ca]
        if v[ca] < unit:
            print(f"error! not enough {ca} for conversion")
            print(f"       needs {unit} but only has {v[ca]}")
            break
        v[ca] -= unit
        v[cb] += conv(unit, ca, cb, n2n)
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
            ret = apply_convs([1 for _ in range(sz)], convs, n2n)
            for k in range(len(n2n)):
                if k == s:
                    continue
                ret = apply_convs(ret, [[None, k, s]], n2n)

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


n2n = [
    [1, 2, None],
    [0.5, 1, 2],
    [None, 0.5, 1],
]
nds = limpa_dataset2(n2n)
print("\n------\n")
print(*n2n, sep="\n")
print("\n------\n")
print(*nds, sep="\n")
print("\n------\n")
get_new_graph(nds)
