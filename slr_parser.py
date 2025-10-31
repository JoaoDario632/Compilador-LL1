from grammar import grammar, first, follow

def itens_lr0(gramatica):

    inicial = list(gramatica.keys())[0]
    novaGramatica = {"S'": [[inicial]]}
    novaGramatica.update(gramatica)

    def fechamento(itens):
        """Calcula o fechamento de um conjunto de itens."""
        fecho = set(itens)
        alterou = True
        while alterou:
            alterou = False
            novos = set()
            for (cabeca, producao, ponto) in fecho:
                if ponto < len(producao):
                    simbolo = producao[ponto]
                    if simbolo in novaGramatica:  # é não-terminal
                        for prod in novaGramatica[simbolo]:
                            novo_item = (simbolo, tuple(prod), 0)
                            if novo_item not in fecho:
                                novos.add(novo_item)
            if novos:
                fecho |= novos
                alterou = True
        return frozenset(fecho)

    def ir_para(itens, simbolo):
        """Transição GOTO (itens, símbolo)."""
        mov = set()
        for (cabeca, producao, ponto) in itens:
            if ponto < len(producao) and producao[ponto] == simbolo:
                mov.add((cabeca, producao, ponto + 1))
        return fechamento(mov)

    # Estado inicial
    inicial_item = fechamento({("S'", (inicial,), 0)})
    estados = [inicial_item]
    transicoes = {}

    alterou = True
    while alterou:
        alterou = False
        novos_estados = []
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
        estados += novos_estados

    return estados, transicoes, novaGramatica

def construir_tabela_slr(gramatica):
    estados, transicoes, novaGramatica = itens_lr0(gramatica)
    acaoTabela = {}
    TableGoTo = {}

    for i, estado in enumerate(estados):
        for (cabeca, prod, ponto) in estado:
            if ponto < len(prod):
                simbolo = prod[ponto]
                if simbolo not in gramatica:
                    j = transicoes.get((i, simbolo))
                    if j is not None:
                        acaoTabela[(i, simbolo)] = ("shift", j)
            else:

                if cabeca == "S'":
                    acaoTabela[(i, "EOF")] = ("accept", None)
                else:
                    for a in follow(cabeca, gramatica):
                        acaoTabela[(i, a)] = ("reduce", (cabeca, prod))

        for simbolo in gramatica.keys():
            j = transicoes.get((i, simbolo))
            if j is not None:
                TableGoTo[(i, simbolo)] = j

    return acaoTabela, TableGoTo, estados

def analisar_slr(tokens, gramatica):
    acaoTabela, TableGoTo, estados = construir_tabela_slr(gramatica)
    statusPilha = [0]
    simbolosPilha = []
    pos = 0
    simbolo = tokens[pos][0]

    while True:
        estado = statusPilha[-1]
        acao = acaoTabela.get((estado, simbolo))

        if not acao:
            print(f"[ERRO] Símbolo inesperado '{simbolo}' no estado {estado}.")
            return False

        tipo, valor = acao

        if tipo == "shift":
            simbolosPilha.append(simbolo)
            statusPilha.append(valor)
            pos += 1
            simbolo = tokens[pos][0]

        elif tipo == "reduce":
            cabeca, prod = valor
            for _ in prod:
                statusPilha.pop()
                simbolosPilha.pop()
            topo = statusPilha[-1]
            simbolosPilha.append(cabeca)
            goto = TableGoTo.get((topo, cabeca))
            statusPilha.append(goto)

        elif tipo == "accept":
            print("Análise SLR(1) concluída com exito")
            return True