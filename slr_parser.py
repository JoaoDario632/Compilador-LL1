from grammar import grammar, follow
from tabulate import tabulate

def Conversao(G):
    nova = {}
    for cab, prods in G.items():
        novas = []
        for p in prods:
            novas.append([] if p == ["ε"] else p)
        nova[cab] = novas
    return nova

def TabelaGramatica(G):
    print("\n=== GRAMÁTICA CONVERTIDA PARA LR(0) ===\n")
    linhas = []
    for cab, prods in G.items():
        bloco = "\n".join(f"• {' '.join(p) if p else 'ε'}" for p in prods)
        linhas.append([cab, bloco])

    print(tabulate(
        linhas,
        headers=["Não-terminal", "Produções"],
        tablefmt="fancy_grid",
        maxcolwidths=[20, 80]
    ))


# ---------------------------------------------------------------------
# 📌  NOVA FUNÇÃO: Tabela de Redução Melhorada
# ---------------------------------------------------------------------
def imprimir_tabela_reducao(passos, ultimos=25):

    print("\n=== TABELA DE REDUÇÃO — ÚLTIMOS PASSOS ===\n")

    # pega só a parte final
    ult = passos[-ultimos:] if len(passos) > ultimos else passos

    linhas = []

    for (num, pilha_est, pilha_simb, entrada, acao) in ult:

        def corta(txt, max_len=35):
            txt = str(txt)
            return txt if len(txt) <= max_len else txt[:max_len] + " ..."

        linhas.append([
            num,
            corta(pilha_est, 30),
            corta(pilha_simb, 30),
            entrada,
            corta(acao, 40)
        ])

    print(tabulate(
        linhas,
        headers=["Passo", "Pilha Estados", "Pilha Símbolos", "Entrada", "Ação"],
        tablefmt="fancy_grid",
        maxcolwidths=[7, 30, 30, 10, 40],
        stralign="center"
    ))

def itens_lr0(G):
    inicial = list(G.keys())[0]
    G2 = {"S'": [[inicial]]}
    G2.update(G)

    def fechamento(itens):
        fecho = set(itens)
        mudou = True
        while mudou:
            mudou = False
            novos = set()
            for (A, prod, ponto) in fecho:
                if ponto < len(prod):
                    X = prod[ponto]
                    if X in G2:
                        for p in G2[X]:
                            item = (X, tuple(p), 0)
                            if item not in fecho:
                                novos.add(item)
            if novos:
                fecho |= novos
                mudou = True
        return frozenset(fecho)

    def GOTO(I, X):
        mov = {(A, prod, ponto + 1)
               for (A, prod, ponto) in I
               if ponto < len(prod) and prod[ponto] == X}
        return fechamento(mov) if mov else frozenset()

    I0 = fechamento({("S'", (inicial,), 0)})
    estados = [I0]
    trans = {}

    mudou = True
    while mudou:
        mudou = False
        for i, estado in enumerate(estados):
            simbolos = set(prod[p] for (A, prod, p) in estado if p < len(prod))
            for X in simbolos:
                dest = GOTO(estado, X)
                if dest and dest not in estados:
                    estados.append(dest)
                    mudou = True
                trans[(i, X)] = estados.index(dest)

    return estados, trans, G2


def ConstrucaoTabelaSLR(G):
    estados, trans, G2 = itens_lr0(G)

    acao = {}
    goto = {}
    start = "PROGRAMA_G"

    for i, estado in enumerate(estados):
        for (A, prod, p) in estado:

            if p < len(prod):
                sym = prod[p]
                if sym not in G:  # terminal
                    j = trans.get((i, sym))
                    if j is not None:
                        acao[(i, sym)] = ("shift", j)

            else:  # REDUCE
                if A == "S'":
                    acao[(i, "EOF")] = ("accept", None)
                else:
                    for t in follow(A, grammar, start):
                        acao[(i, t)] = ("reduce", (A, prod))

        for nt in G.keys():
            j = trans.get((i, nt))
            if j is not None:
                goto[(i, nt)] = j
    return acao, goto, estados

def _formata_pilha_est(pilha, max_len=6):
    if len(pilha) <= max_len:
        return str(pilha)
    return f"... {pilha[-max_len:]}"


def _formata_pilha_simb(pilha, max_len=6):
    if len(pilha) <= max_len:
        return " ".join(pilha)
    return "... " + " ".join(pilha[-max_len:])


def _formata_acao(tipo, valor):
    if tipo == "shift":
        return f"shift {valor}"
    if tipo == "reduce":
        A, prod = valor
        rhs = " ".join(prod) if prod else "ε"
        return f"reduce {A} → {rhs}"
    if tipo == "accept":
        return "accept"
    return str((tipo, valor))


def analisar_slr(tokens, G_original):

    print("\n[SLR] Convertendo gramática...")
    G = Conversao(G_original)

    TabelaGramatica(G)

    acao, goto, estados = ConstrucaoTabelaSLR(G)

    pilha_est = [0]
    pilha_simb = []

    pos = 0
    simbolo = tokens[pos][0]

    passos = []
    n_pass = 1

    while True:
        estado = pilha_est[-1]
        entrada = simbolo
        act = acao.get((estado, entrada))

        if not act:
            print(f"[ERRO] SLR: token '{entrada}' inesperado no estado {estado}")
            return False

        tipo, valor = act

        passos.append([
            n_pass,
            _formata_pilha_est(pilha_est),
            _formata_pilha_simb(pilha_simb),
            entrada,
            _formata_acao(tipo, valor)
        ])

        if tipo == "shift":
            pilha_simb.append(entrada)
            pilha_est.append(valor)
            pos += 1
            simbolo = tokens[pos][0]
            n_pass += 1
            continue

        if tipo == "reduce":
            A, prod = valor
            for _ in prod:
                pilha_est.pop()
                pilha_simb.pop()
            topo = pilha_est[-1]
            pilha_simb.append(A)
            pilha_est.append(goto[(topo, A)])
            n_pass += 1
            continue

        if tipo == "accept":
            break

    imprimir_tabela_reducao(passos)

    print("\nAnálise SLR(1) concluída com sucesso!\n")
