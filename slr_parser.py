from grammar import grammar, first, follow
# ================================
# Geração dos itens LR(0)
# ================================
def itens_lr0(gramatica):
    """
    Calcula a coleção de itens LR(0) e as transições (GOTO) para a gramática.
    """
    # Cria uma nova gramática adicionando o símbolo inicial S'
    inicial = list(gramatica.keys())[0]  # pega o símbolo inicial da gramática
    novaGramatica = {"S'": [[inicial]]}
    novaGramatica.update(gramatica)

    # ================================
    # Função de fechamento (closure)
    # ================================
    def fechamento(itens):
        """
        Recebe um conjunto de itens e retorna seu fechamento LR(0).
        """
        fecho = set(itens)
        alterou = True
        while alterou:
            alterou = False
            novos = set()
            for (cabeca, producao, ponto) in fecho:
                # Se o ponto não chegou ao final da produção
                if ponto < len(producao):
                    simbolo = producao[ponto]
                    # Se o símbolo é um não-terminal
                    if simbolo in novaGramatica:
                        # Adiciona todos os itens correspondentes ao não-terminal
                        for prod in novaGramatica[simbolo]:
                            novo_item = (simbolo, tuple(prod), 0)
                            if novo_item not in fecho:
                                novos.add(novo_item)
            if novos:
                fecho |= novos
                alterou = True
        return frozenset(fecho)  # retorna um conjunto imutável

    # ================================
    # Função de transição GOTO (ir_para)
    # ================================
    def ir_para(itens, simbolo):
        """
        Calcula o conjunto de itens ao mover o ponto sobre o símbolo.
        """
        mov = set()
        for (cabeca, producao, ponto) in itens:
            if ponto < len(producao) and producao[ponto] == simbolo:
                mov.add((cabeca, producao, ponto + 1))
        return fechamento(mov)

    # Estado inicial (fechamento do item inicial)
    inicial_item = fechamento({("S'", (inicial,), 0)})
    estados = [inicial_item]
    transicoes = {}

    # Construção dos estados e transições
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
                # Salva a transição (estado atual, símbolo) -> estado destino
                transicoes[(i, simbolo)] = estados.index(destino)
        estados += novos_estados

    return estados, transicoes, novaGramatica

# ================================
# Construção da tabela SLR
# ================================
def construir_tabela_slr(gramatica):
    """
    Constrói a tabela SLR(1) a partir dos itens LR(0).
    """
    estados, transicoes, novaGramatica = itens_lr0(gramatica)
    acaoTabela = {}  # tabela ACTION (shift, reduce, accept)
    TableGoTo = {}   # tabela GOTO (não-terminais)

    for i, estado in enumerate(estados):
        for (cabeca, prod, ponto) in estado:
            if ponto < len(prod):
                simbolo = prod[ponto]
                # Se for terminal, cria ação shift
                if simbolo not in gramatica:
                    j = transicoes.get((i, simbolo))
                    if j is not None:
                        acaoTabela[(i, simbolo)] = ("shift", j)
            else:
                # Item completo
                if cabeca == "S'":
                    # Aceitação da análise
                    acaoTabela[(i, "EOF")] = ("accept", None)
                else:
                    # Redução pelo símbolo não-terminal cabeca
                    for a in follow(cabeca, gramatica):
                        acaoTabela[(i, a)] = ("reduce", (cabeca, prod))

        # Preenchimento da tabela GOTO para não-terminais
        for simbolo in gramatica.keys():
            j = transicoes.get((i, simbolo))
            if j is not None:
                TableGoTo[(i, simbolo)] = j

    return acaoTabela, TableGoTo, estados

# ================================
# Algoritmo de análise SLR(1)
# ================================
def analisar_slr(tokens, gramatica):
    """
    Analisa uma sequência de tokens usando a tabela SLR(1).
    """
    acaoTabela, TableGoTo, estados = construir_tabela_slr(gramatica)
    statusPilha = [0]  # pilha de estados
    simbolosPilha = [] # pilha de símbolos
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
            # Shift: empilha o símbolo e o estado destino
            simbolosPilha.append(simbolo)
            statusPilha.append(valor)
            pos += 1
            simbolo = tokens[pos][0]

        elif tipo == "reduce":
            # Reduce: desempilha símbolos da produção
            cabeca, prod = valor
            for _ in prod:
                statusPilha.pop()
                simbolosPilha.pop()
            topo = statusPilha[-1]
            simbolosPilha.append(cabeca)
            goto = TableGoTo.get((topo, cabeca))
            statusPilha.append(goto)

        elif tipo == "accept":
            print("Análise SLR(1) concluída com êxito")
            return True
