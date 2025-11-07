from grammar import grammar, first, follow

# ============================================================
# Função: itens_lr0()
# ============================================================
# Constrói o conjunto de itens LR(0) e as transições entre eles.
# Cada item é uma tupla: (Cabeça, Produção, Posição_do_Ponto)
# Exemplo de item: (E, ["E", "+", "T"], 2)  →  E → E + •T
# ============================================================
def itens_lr0(gramatica):
    # Símbolo inicial da gramática original
    inicial = list(gramatica.keys())[0]

    # Adiciona uma nova produção inicial: S' → S
    novaGramatica = {"S'": [[inicial]]}
    novaGramatica.update(gramatica)

    # ----------------------------------------
    # Função: fechamento(itens)
    # ----------------------------------------
    # Retorna o fechamento LR(0) de um conjunto de itens.
    # Se houver um ponto antes de um não-terminal X,
    # inclui todos os itens X → •α no fecho.
    # ----------------------------------------
    def fechamento(itens):
        fecho = set(itens)
        alterou = True
        while alterou:
            alterou = False
            novos = set()

            for (cabeca, producao, ponto) in fecho:
                # Se o ponto está antes de um símbolo
                if ponto < len(producao):
                    simbolo = producao[ponto]

                    # Se é um não-terminal, adiciona suas produções com ponto no início
                    if simbolo in novaGramatica:
                        for prod in novaGramatica[simbolo]:
                            novo_item = (simbolo, tuple(prod), 0)
                            if novo_item not in fecho:
                                novos.add(novo_item)

            # Atualiza o fecho se houver novos itens
            if novos:
                fecho |= novos
                alterou = True

        # Usa frozenset (imutável) para representar o estado
        return frozenset(fecho)

    # ----------------------------------------
    # Função: ir_para(itens, simbolo)
    # ----------------------------------------
    # Retorna o conjunto de itens resultante de mover o ponto
    # após o símbolo especificado.
    # Exemplo: [A → α •X β] → GOTO(itens, X) = [A → α X• β]
    # ----------------------------------------
    def ir_para(itens, simbolo):
        mov = set()
        for (cabeca, producao, ponto) in itens:
            if ponto < len(producao) and producao[ponto] == simbolo:
                mov.add((cabeca, producao, ponto + 1))
        return fechamento(mov)

    # ----------------------------------------
    # Estado inicial: fecho de S' → •S
    # ----------------------------------------
    itenInicial = fechamento({("S'", (inicial,), 0)})

    estados = [itenInicial]
    transicoes = {}
    alterou = True

    # ----------------------------------------
    # Geração de todos os estados e transições (GOTO)
    # ----------------------------------------
    while alterou:
        alterou = False
        novos_estados = []

        for i, estado in enumerate(estados):
            simbolos = set()

            # Coleta todos os símbolos que aparecem após o ponto
            for (cabeca, prod, ponto) in estado:
                if ponto < len(prod):
                    simbolos.add(prod[ponto])

            # Para cada símbolo, calcula o estado destino
            for simbolo in simbolos:
                destino = ir_para(estado, simbolo)

                # Se o estado destino é novo, adiciona
                if destino and destino not in estados:
                    estados.append(destino)
                    alterou = True

                # Registra transição (estado_atual, símbolo) → índice_estado_destino
                transicoes[(i, simbolo)] = estados.index(destino)

        estados += novos_estados

    # Retorna os conjuntos de itens (estados), as transições e a gramática aumentada
    return estados, transicoes, novaGramatica


# ============================================================
# Função: construir_tabela_slr()
# ============================================================
# Constrói as tabelas ACTION e GOTO para o analisador SLR(1)
# Baseia-se nos estados LR(0) e nos conjuntos FOLLOW
# ============================================================
def construir_tabela_slr(gramatica):
    estados, transicoes, novaGramatica = itens_lr0(gramatica)

    acaoTabela = {}   # ACTION table (ações: shift, reduce, accept)
    TableGoTo = {}    # GOTO table (transições entre não-terminais)
    start_symbol = "PROGRAMA_G"

    # Para cada estado (conjunto de itens LR(0))
    for i, estado in enumerate(estados):
        for (cabeca, prod, ponto) in estado:
            # ----------------------------------------
            # Caso 1: o ponto não está no fim → ação SHIFT
            # ----------------------------------------
            if ponto < len(prod):
                simbolo = prod[ponto]
                # Se o símbolo é terminal (não está na gramática)
                if simbolo not in gramatica:
                    j = transicoes.get((i, simbolo))
                    if j is not None:
                        acaoTabela[(i, simbolo)] = ("shift", j)

            # ----------------------------------------
            # Caso 2: o ponto está no fim → ação REDUCE ou ACCEPT
            # ----------------------------------------
            else:
                if cabeca == "S'":
                    # Se a produção é S' → S• → aceitar
                    acaoTabela[(i, "EOF")] = ("accept", None)
                else:
                    # Para cada símbolo no FOLLOW(A), adiciona reduce(A→α)
                    for a in follow(cabeca, gramatica, start_symbol):
                        acaoTabela[(i, a)] = ("reduce", (cabeca, prod))

        # ----------------------------------------
        # Preenche tabela GOTO (não-terminais)
        # ----------------------------------------
        for simbolo in gramatica.keys():
            j = transicoes.get((i, simbolo))
            if j is not None:
                TableGoTo[(i, simbolo)] = j

    return acaoTabela, TableGoTo, estados


# ============================================================
# Função: analisar_slr()
# ============================================================
# Executa o algoritmo de análise SLR(1) propriamente dito.
# Utiliza as tabelas ACTION e GOTO construídas anteriormente.
# ============================================================
def analisar_slr(tokens, gramatica):
    acaoTabela, TableGoTo, estados = construir_tabela_slr(gramatica)

    statusPilha = [0]   # Pilha de estados
    simbolosPilha = []  # Pilha de símbolos (terminais e não-terminais)
    pos = 0             # Posição atual de leitura no vetor de tokens
    simbolo = tokens[pos][0]  # Tipo do token atual

    # Loop principal da análise
    while True:
        estado = statusPilha[-1]
        acao = acaoTabela.get((estado, simbolo))

        # Caso de erro sintático
        if not acao:
            print(f"[ERRO] Símbolo inesperado '{simbolo}' no estado {estado}.")
            return False

        tipo, valor = acao

        # ----------------------------------------
        # Ação SHIFT → empilha símbolo e novo estado
        # ----------------------------------------
        if tipo == "shift":
            simbolosPilha.append(simbolo)
            statusPilha.append(valor)
            pos += 1
            simbolo = tokens[pos][0]

        # ----------------------------------------
        # Ação REDUCE → aplica produção e volta via GOTO
        # ----------------------------------------
        elif tipo == "reduce":
            cabeca, prod = valor

            # Remove os símbolos da produção da pilha
            for _ in prod:
                statusPilha.pop()
                simbolosPilha.pop()

            # Obtém o estado anterior
            topo = statusPilha[-1]
            simbolosPilha.append(cabeca)

            # Transição via GOTO
            goto = TableGoTo.get((topo, cabeca))
            statusPilha.append(goto)

        elif tipo == "accept":
            print("Análise SLR(1) concluída com sucesso!")
            return True
