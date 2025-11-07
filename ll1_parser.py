# ------------------------------------------------------------
# Importa a gramática e as funções auxiliares (FIRST e FOLLOW)
# ------------------------------------------------------------
from grammar import grammar, first, follow

# ============================================================
# CLASSE: AnalisadorSintaticoLL1
# ============================================================
# Implementa um analisador preditivo descendente baseado em tabela LL(1)
# Ele utiliza os conjuntos FIRST e FOLLOW para construir a tabela de análise
# e percorre a lista de tokens, verificando se a sequência é válida
# conforme a gramática definida.
# ============================================================
class AnalisadorSintaticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.simbolo_inicial = "PROGRAMA_G"  # Símbolo inicial da gramática
        self.analiseTabela = self.construir_tabela_ll1()  # Cria a tabela LL(1)

    # ========================================================
    # CONSTRUÇÃO DA TABELA LL(1)
    # ========================================================
    def construir_tabela_ll1(self):
        tabela = {}

        # Para cada produção A → α da gramática
        for cabeca, producoes in self.gramatica.items():
            for producao in producoes:
                conjPrimeiro = set()     # FIRST(α)
                encontrou_vazio = True   # Indica se ε é possível na produção

                # Percorre cada símbolo da produção (α)
                for simbolo in producao:
                    # Obtém FIRST(simbolo)
                    primeiros = first(simbolo, self.gramatica)

                    # Adiciona tudo que não é ε
                    conjPrimeiro |= (primeiros - {"ε"})

                    # Se o símbolo não gera ε, para a busca
                    if "ε" not in primeiros:
                        encontrou_vazio = False
                        break

                # Se todos os símbolos da produção geram ε, adiciona ε
                if encontrou_vazio:
                    conjPrimeiro.add("ε")

                # Para cada terminal em FIRST(A → α), adiciona A→α na tabela
                for simbolo in conjPrimeiro - {"ε"}:
                    chave = (cabeca, simbolo)
                    tabela[chave] = producao

                # Se a produção pode gerar ε, adiciona também FOLLOW(A)
                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica, self.simbolo_inicial):
                        tabela[(cabeca, simbolo)] = producao

        return tabela


    # ========================================================
    # ANÁLISE SINTÁTICA (Preditiva)
    # ========================================================
    def analisar(self, tokens):
        """
        Executa a análise sintática LL(1) com modo de recuperação de erros.
        tokens: lista de tuplas (tipo_token, valor_token)
        """
        pilha = ["EOF", self.simbolo_inicial]  # Pilha começa com símbolo inicial
        posicao = 0
        ttoken = tokens[posicao][0]  # Tipo do token atual (ex: IDENT, NUMERO_INT, etc.)

        # Loop principal — executa enquanto a pilha não estiver vazia
        while pilha:
            topo = pilha.pop()  # Remove o topo da pilha

            # ------------------------------------------------
            # CASO 1: Topo da pilha é igual ao token atual
            # ------------------------------------------------
            if topo == ttoken:
                # Consome o token
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                continue

            # ------------------------------------------------
            # CASO 2: Topo é um não-terminal
            # ------------------------------------------------
            elif topo in self.gramatica:
                # Busca uma produção A→α na tabela LL(1)
                regra = self.analiseTabela.get((topo, ttoken))

                # Se não há regra para o par (A, token), erro sintático
                if not regra:
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    print(f"[ERRO] Esperado um de {esperados}, mas encontrado '{ttoken}'.")
                    print("→ Recuperando em modo pânico.")

                    # ------------------------------------------------
                    # MODO PÂNICO:
                    # Avança os tokens até encontrar um símbolo do FOLLOW(top)
                    # ------------------------------------------------
                    follow_topo = follow(topo, self.gramatica, self.simbolo_inicial)
                    while ttoken not in follow_topo and ttoken != "EOF":
                        posicao += 1
                        if posicao < len(tokens):
                            ttoken = tokens[posicao][0]
                        else:
                            break
                    continue  # Tenta continuar análise após a recuperação

                # ------------------------------------------------
                # Regra encontrada: empilha a produção (em ordem reversa)
                # ------------------------------------------------
                for simbolo in reversed(regra):
                    if simbolo != "ε":  # Não empilha produções vazias
                        pilha.append(simbolo)

            # ------------------------------------------------
            # CASO 3: Topo é ε (produção vazia) → ignora
            # ------------------------------------------------
            elif topo == "ε":
                continue

            # ------------------------------------------------
            # CASO 4: Erro — terminal inesperado
            # ------------------------------------------------
            else:
                print(f"[ERRO] Token inesperado '{ttoken}', esperado '{topo}'.")
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                else:
                    break
        print("\nAnálise sintática concluída (modo pânico ativo).")
