from grammar import grammar, follow
from tabulate import tabulate

def Conversao(G):
    nova = {}
    for cab, prods in G.items():
        novas = []
        for p in prods:
            if p == ["ε"]:
                novas.append([])
            else:
                novas.append(p)
        nova[cab] = novas
    return nova
def TabelaGramatica(G):
    print("\n=== GRAMÁTICA CONVERTIDA PARA LR(0) ===\n")

    linhas = []

    for cab, prods in G.items():
        bloco = []
        for p in prods:
            if p == []:
                prod_texto = "ε"
            else:
                prod_texto = " ".join(p)

            bloco.append(f"  • {prod_texto}")

        linhas.append([cab, "\n".join(bloco)])

    print(tabulate(
        linhas,
        headers=["Não-terminal", "Produções"],
        tablefmt="fancy_grid",
        maxcolwidths=[20, 80],
        stralign="left"
    ))
def itens_lr0(gramatica):

    inicial = list(gramatica.keys())[0]

    novaGramatica = {"S'": [[inicial]]}
    novaGramatica.update(gramatica)

    def fechamento(itens):
        fecho = set(itens)
        alterou = True
        while alterou:
            alterou = False
            novos = set()

            for (cab, prod, ponto) in fecho:
                if ponto < len(prod):
                    simbolo = prod[ponto]

                    if simbolo in novaGramatica:
                        for p in novaGramatica[simbolo]:
                            item = (simbolo, tuple(p), 0)
                            if item not in fecho:
                                novos.add(item)

            if novos:
                fecho |= novos
                alterou = True

        return frozenset(fecho)


    def GOTO(itens, simbolo):
        mov = set()
        for (cab, prod, ponto) in itens:
            if ponto < len(prod) and prod[ponto] == simbolo:
                mov.add((cab, prod, ponto+1))
        return fechamento(mov)


    estado0 = fechamento({("S'", (inicial,), 0)})
    estados = [estado0]
    trans = {}
    alterou = True

    while alterou:
        alterou = False
        for i, estado in enumerate(estados):

            simbolos = set()
            for (cab, prod, ponto) in estado:
                if ponto < len(prod):
                    simbolos.add(prod[ponto])

            for s in simbolos:
                destino = GOTO(estado, s)

                if destino not in estados:
                    estados.append(destino)
                    alterou = True

                trans[(i, s)] = estados.index(destino)

    return estados, trans, novaGramatica

def ConstrucaoTabelaSLR(gramatica):
    estados, trans, nova = itens_lr0(gramatica)

    acao = {}
    goto = {}
    start = "PROGRAMA_G"

    for i, estado in enumerate(estados):
        for (cab, prod, ponto) in estado:

            if ponto < len(prod):
                simbolo = prod[ponto]
                if simbolo not in gramatica:
                    j = trans.get((i, simbolo))
                    if j is not None:
                        acao[(i, simbolo)] = ("shift", j)

            else:
                if cab == "S'":
                    acao[(i, "EOF")] = ("accept", None)
                else:
                    for a in follow(cab, grammar, start):
                        acao[(i, a)] = ("reduce", (cab, prod))
        for s in gramatica.keys():
            j = trans.get((i, s))
            if j is not None:
                goto[(i, s)] = j

    return acao, goto, estados
def analisar_slr(tokens, gramatica_original):
    print("\n[SLR] Convertendo gramática para formato LR(0)...")
    gram_lr0 = Conversao(gramatica_original)
    TabelaGramatica(gram_lr0)
    acao, goto, estados = ConstrucaoTabelaSLR(gram_lr0)

    pilha_est = [0]
    pilha_simb = []

    pos = 0
    simbolo = tokens[pos][0]

    while True:
        estado = pilha_est[-1]
        entrada = simbolo

        act = acao.get((estado, entrada))

        if not act:
            print(f"[ERRO] SLR: símbolo inesperado '{entrada}' no estado {estado}.")
            return False

        tipo, valor = act

        # SHIFT
        if tipo == "shift":
            pilha_simb.append(entrada)
            pilha_est.append(valor)
            pos += 1
            simbolo = tokens[pos][0]
            continue

        # REDUCE
        if tipo == "reduce":
            cab, prod = valor

            if len(prod) > 0:
                for _ in prod:
                    pilha_est.pop()
                    pilha_simb.pop()

            topo = pilha_est[-1]
            pilha_simb.append(cab)

            g = goto.get((topo, cab))
            if g is None:
                print(f"[ERRO] SLR: goto inválido após reduzir {cab} → {prod}")
                return False

            pilha_est.append(g)
            continue
        if tipo == "accept":
            print("Análise SLR(1) concluída com sucesso!")
            return True
