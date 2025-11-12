from grammar import grammar, follow

def converter_gramatica_para_lr0(G):
    nova = {}
    for cab, prods in G.items():
        novas_prods = []
        for p in prods:
            if p == ["ε"]:
                novas_prods.append([])   # produção realmente vazia
            else:
                novas_prods.append(p)
        nova[cab] = novas_prods
    return nova

def mostrar_gramatica_lr0(G):
    print("\n===== Conversão gramática para a LR0 =====\n")
    for cab, prods in G.items():
        print(f"{cab} → ", end="")
        regras = []
        for p in prods:
            if p == []:
                regras.append("ε")
            else:
                regras.append(" ".join(p))
        print(" | ".join(regras))
    print("\n===========================================\n")

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

            for (cabeca, producao, ponto) in fecho:
                if ponto < len(producao):
                    simbolo = producao[ponto]

                    if simbolo in novaGramatica:
                        for prod in novaGramatica[simbolo]:
                            novo_item = (simbolo, tuple(prod), 0)
                            if novo_item not in fecho:
                                novos.add(novo_item)

            if novos:
                fecho |= novos
                alterou = True

        return frozenset(fecho)

    def ir_para(itens, simbolo):
        mov = set()
        for (cabeca, producao, ponto) in itens:
            if ponto < len(producao) and producao[ponto] == simbolo:
                mov.add((cabeca, producao, ponto + 1))
        return fechamento(mov)

    estado0 = fechamento({("S'", (inicial,), 0)})

    estados = [estado0]
    transicoes = {}
    alterou = True

    while alterou:
        alterou = False

        for i, estado in enumerate(estados):
            simbolos = set()

            for (cabeca, prod, ponto) in estado:
                if ponto < len(prod):
                    simbolos.add(prod[ponto])

            for simbolo in simbolos:
                destino = ir_para(estado, simbolo)

                if destino and destino not in estados:
                    estados.append(destino)
                    alterou = True

                transicoes[(i, simbolo)] = estados.index(destino)

    return estados, transicoes, novaGramatica

def construir_tabela_slr(gramatica):
    estados, transicoes, nova = itens_lr0(gramatica)

    acaoTabela = {}
    TableGoTo = {}
    start_symbol = "PROGRAMA_G"

    for i, estado in enumerate(estados):
        for (cabeca, prod, ponto) in estado:

            # SHIFT
            if ponto < len(prod):
                simbolo = prod[ponto]
                if simbolo not in gramatica:
                    j = transicoes.get((i, simbolo))
                    if j is not None:
                        acaoTabela[(i, simbolo)] = ("shift", j)

            # REDUCE / ACCEPT
            else:
                if cabeca == "S'":
                    acaoTabela[(i, "EOF")] = ("accept", None)
                else:
                    for a in follow(cabeca, grammar, start_symbol):
                        acaoTabela[(i, a)] = ("reduce", (cabeca, prod))

        # GOTO
        for simbolo in gramatica.keys():
            j = transicoes.get((i, simbolo))
            if j is not None:
                TableGoTo[(i, simbolo)] = j

    return acaoTabela, TableGoTo, estados

def analisar_slr(tokens, gramatica_original):
    print("\n[SLR] Convertendo gramática para formato LR(0)...")

    # 1) Converte ε → []
    gram_lr0 = converter_gramatica_para_lr0(gramatica_original)

    # 2) Mostra a gramática convertida
    mostrar_gramatica_lr0(gram_lr0)

    # 3) Constrói ACTION e GOTO
    acaoTabela, TableGoTo, estados = construir_tabela_slr(gram_lr0)

    pilha_estados = [0]
    pilha_simbolos = []

    pos = 0
    simbolo = tokens[pos][0]

    while True:
        estado = pilha_estados[-1]
        acao = acaoTabela.get((estado, simbolo))

        if not acao:
            print(f"[ERRO] SLR: símbolo inesperado '{simbolo}' no estado {estado}.")
            return False

        tipo, valor = acao

        # SHIFT
        if tipo == "shift":
            pilha_simbolos.append(simbolo)
            pilha_estados.append(valor)
            pos += 1
            simbolo = tokens[pos][0]
            continue

        # REDUCE
        if tipo == "reduce":
            cabeca, prod = valor

            # Produção vazia não desempilha
            if len(prod) > 0:
                for _ in prod:
                    pilha_estados.pop()
                    pilha_simbolos.pop()

            topo = pilha_estados[-1]
            pilha_simbolos.append(cabeca)

            goto = TableGoTo.get((topo, cabeca))

            if goto is None:
                print(f"[ERRO] SLR: GOTO inválido após reduzir {cabeca} → {prod}")
                return False

            pilha_estados.append(goto)
            continue

        # ACCEPT
        if tipo == "accept":
            print("Análise SLR(1) concluída com sucesso")
            return True
