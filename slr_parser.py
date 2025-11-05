from grammar import grammar, first, follow
# Gera os *itens LR(0)*, ou seja, os estados e transições do autômato LR(0)
# Cada item tem a forma (Cabeça, Produção, Posição_do_Ponto)
def itens_lr0(gramatica):

    # Pega o símbolo inicial da gramática (a primeira chave do dicionário)
    inicial = list(gramatica.keys())[0]

    # Cria uma nova gramática com símbolo inicial aumentado S' -> S
    novaGramatica = {"S'": [[inicial]]}
    novaGramatica.update(gramatica)

    # ---------------------------
    # Função interna: fechamento()
    # ---------------------------
    # Dado um conjunto de itens, adiciona todos os itens que podem ser "alcançados"
    # a partir de não-terminais logo após o ponto.
    def fechamento(itens):
        fecho = set(itens)
        alterou = True

        # Continua expandindo enquanto houver novos itens a adicionar
        while alterou:
            alterou = False
            novos = set()

            for (cabeca, producao, ponto) in fecho:
                # Se o ponto não está no fim da produção
                if ponto < len(producao):
                    simbolo = producao[ponto]

                    # Se o símbolo é um não-terminal (está na gramática)
                    if simbolo in novaGramatica:
                        # Para cada produção desse não-terminal,
                        # adiciona o item com ponto no início
                        for prod in novaGramatica[simbolo]:
                            novo_item = (simbolo, tuple(prod), 0)
                            if novo_item not in fecho:
                                novos.add(novo_item)

            # Se novos itens foram adicionados, o fecho precisa ser reavaliado
            if novos:
                fecho |= novos
                alterou = True

        # Retorna o conjunto final imutável (para ser usado como chave em dicionários)
        return frozenset(fecho)

    # Move o ponto sobre um símbolo específico e retorna o fechamento resultante
    def ir_para(itens, simbolo):
        mov = set()
        for (cabeca, producao, ponto) in itens:
            # Se o ponto está antes do símbolo desejado, move-o uma posição à frente
            if ponto < len(producao) and producao[ponto] == simbolo:
                mov.add((cabeca, producao, ponto + 1))
        return fechamento(mov)


    # Cria o primeiro item inicial: S' -> .S
    inicial_item = fechamento({("S'", (inicial,), 0)})

    # Lista de estados (cada estado é um conjunto de itens LR(0))
    estados = [inicial_item]

    # Dicionário de transições: (estado_atual, símbolo) -> estado_destino
    transicoes = {}
    # Loop principal: constrói todos os estados LR
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
# A partir dos itens LR(0), constrói as tabelas ACTION e GOTO usadas no parser SLR(1)
def construir_tabela_slr(gramatica):
    estados, transicoes, novaGramatica = itens_lr0(gramatica)

    # Tabelas principais do analisador SLR
    acaoTabela = {}  # Tabela ACTION: shift, reduce, accept
    TableGoTo = {}   # Tabela GOTO: transições com não-terminais

    # Percorre todos os estados do autômato LR(0)
    for i, estado in enumerate(estados):
        for (cabeca, prod, ponto) in estado:

            # Caso 1: ponto não está no fim → ação de deslocamento (shift)
            if ponto < len(prod):
                simbolo = prod[ponto]

                # Se é um terminal (não está na gramática), faz "shift"
                if simbolo not in gramatica:
                    j = transicoes.get((i, simbolo))
                    if j is not None:
                        acaoTabela[(i, simbolo)] = ("shift", j)

            # Caso 2: ponto no fim → ação de redução (reduce)
            else:
                # Se é o item final de S' → ação de "accept"
                if cabeca == "S'":
                    acaoTabela[(i, "EOF")] = ("accept", None)
                else:
                    # Para cada símbolo no FOLLOW da cabeça, adiciona ação de redução
                    for a in follow(cabeca, gramatica):
                        acaoTabela[(i, a)] = ("reduce", (cabeca, prod))

        # Cria as entradas da tabela GOTO para não-terminais
        for simbolo in gramatica.keys():
            j = transicoes.get((i, simbolo))
            if j is not None:
                TableGoTo[(i, simbolo)] = j

    # Retorna as tabelas ACTION e GOTO, além dos estados
    return acaoTabela, TableGoTo, estados
# Simula o processo de análise sintática SLR(1) usando as tabelas ACTION e GOTO
def analisar_slr(tokens, gramatica):
    acaoTabela, TableGoTo, estados = construir_tabela_slr(gramatica)

    statusPilha = [0]   # Pilha de estados
    simbolosPilha = []  # Pilha de símbolos
    pos = 0             # Posição atual no vetor de tokens
    simbolo = tokens[pos][0]  # Primeiro token (ex: 'id', '+', etc.)

    # Loop principal da análise
    while True:
        estado = statusPilha[-1]  # Estado atual
        acao = acaoTabela.get((estado, simbolo))  # Consulta na tabela ACTION

        # Caso não exista ação válida → erro sintático
        if not acao:
            print(f"[ERRO] Símbolo inesperado '{simbolo}' no estado {estado}.")
            return False

        tipo, valor = acao
        # Ação SHIFT (deslocamento)
        if tipo == "shift":
            simbolosPilha.append(simbolo)  # Empilha símbolo
            statusPilha.append(valor)      # Empilha novo estado
            pos += 1                       # Avança para o próximo token
            simbolo = tokens[pos][0]       # Lê o próximo símbolo
        # Ação REDUCE (redução)
        elif tipo == "reduce":
            cabeca, prod = valor

            # Remove da pilha tantos símbolos/estados quanto o tamanho da produção
            for _ in prod:
                statusPilha.pop()
                simbolosPilha.pop()

            topo = statusPilha[-1]  # Estado no topo após a redução

            # Empilha o não-terminal reduzido
            simbolosPilha.append(cabeca)

            # Consulta a tabela GOTO para saber o novo estado
            goto = TableGoTo.get((topo, cabeca))
            statusPilha.append(goto)
        # Ação ACCEPT (aceitação)
        elif tipo == "accept":
            print("Análise SLR(1) concluída com sucesso!")
            return True
