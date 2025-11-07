from grammar import grammar, first, follow

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

    itenInicial = fechamento({("S'", (inicial,), 0)})
    estados = [itenInicial]
    transicoes = {}
    alterou = True

    while alterou:
        alterou = False
        novos_estados = []

        for i, estado in enumerate(estados):
            simbolos = set()

            # Coleta todos os símbolos possíveis após o ponto
            for (cabeca, prod, ponto) in estado:
                if ponto < len(prod):
                    simbolos.add(prod[ponto])

            # Para cada símbolo, calcula o estado de destino (GOTO)
            for simbolo in simbolos:
                destino = ir_para(estado, simbolo)

                # Se é um novo estado, adiciona à lista
                if destino and destino not in estados:
                    estados.append(destino)
                    alterou = True

                # Registra a transição (estado atual, símbolo) → índice do estado destino
                transicoes[(i, simbolo)] = estados.index(destino)

        estados += novos_estados

    # Retorna os estados, transições e a gramática aumentada
    return estados, transicoes, novaGramatica
def construir_tabela_slr(gramatica):
    estados, transicoes, novaGramatica = itens_lr0(gramatica)

    acaoTabela = {}
    TableGoTo = {}
    start_symbol = "PROGRAMA_G"

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
                    for a in follow(cabeca, gramatica, start_symbol):
                        acaoTabela[(i, a)] = ("reduce", (cabeca, prod))

        # Preenche tabela GOTO
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
            print("Análise SLR(1) concluída com sucesso!")
            return True