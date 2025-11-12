# -------------------------------------------------------------
# grammar.py — Definição da gramática e funções FIRST / FOLLOW
# -------------------------------------------------------------

from collections import defaultdict, deque

# -------------------------
# DEFINIÇÃO DA GRAMÁTICA
# -------------------------
# Cada não-terminal (como "PROGRAMA_G") possui uma lista de produções.
# Cada produção é uma lista de símbolos (terminais ou não-terminais).
# O símbolo "ε" (epsilon) representa produção vazia.

grammar = {
    # Programa principal = conjunto de funções + função principal
    "PROGRAMA_G": [["DECL_FUNCOES_G", "PRINCIPAL_G"]],

    # Declaração de funções (recursiva)
    "DECL_FUNCOES_G": [
        ["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE", "DECL_FUNCOES_G"],
        ["ε"]
    ],
    "CHAM_FUNCOES_G": [["IDENT", "LPAREN", "ARGUMENTOS_G", "RPAREN"]],

    # Função principal obrigatória
    "PRINCIPAL_G": [["PRINCIPAL", "LCHAVE", "COMANDOS_G", "RCHAVE"]],

    # Declaração de parâmetros formais de funções
    "PARAMS_G": [["TIPO_VAR", "IDENT", "PARAMS_RESTO_G"], ["ε"]],
    "PARAMS_RESTO_G": [["VIRGULA", "TIPO_VAR", "IDENT", "PARAMS_RESTO_G"], ["ε"]],

    # Lista de comandos (sequência de comandos)
    "COMANDOS_G": [["COMANDO_G", "COMANDOS_G"], ["ε"]],

    # Definição dos comandos disponíveis
    "COMANDO_G": [
        # Declaração de variável
        ["DECLARACOES_G", "PONTOVIRG"],
        # Elemento com identificador
        ["IDENT", "ELEMENTO_IDENT_G", "PONTOVIRG"],
        # Estrutura condicional SE/SENÃO
        ["SE", "LPAREN", "EXPRESSAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE", "SENAO_G"],
        # Estrutura de repetição ENQUANTO
        ["ENQUANTO", "LPAREN", "EXPRESSAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE"],
        # Estrutura de repetição FAÇA ENQUANTO
        ["FACA", "LCHAVE", "COMANDOS_G", "RCHAVE", "ENQUANTO", "LPAREN", "EXPRESSAO_G", "RPAREN", "PONTOVIRG"],
        # Estrutura de repetição PARA
        ["PARA", "LPAREN", "DECL_OU_ATRIB_G", "PONTOVIRG", "EXPRESSAO_G", "PONTOVIRG", "ATRIBUICAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE"],
        # Retorno de função
        ["RETORNO", "EXPRESSAO_G", "PONTOVIRG"]
    ],

    # Declaração ou Atribuição
    "DECL_OU_ATRIB_G": [["DECLARACOES_G"], ["ATRIBUICAO_G"]],

    # Declarações de variáveis locais
    "DECLARACOES_G": [
        ["TIPO_VAR", "IDENT", "DECLARACOES_ATRIB_G", "DECLARACOES_RESTO_G"]
    ],
    "DECLARACOES_RESTO_G": [["VIRGULA", "IDENT", "DECLARACOES_ATRIB_G", "DECLARACOES_RESTO_G"], ["ε"]],
    "DECLARACOES_ATRIB_G": [["ATRIB", "EXPRESSAO_G"], ["ε"]],

    # Atribuição de variável
    "ATRIBUICAO_G": [["IDENT", "ATRIB", "EXPRESSAO_G"]],

    # Elemento com identificador
    "ELEMENTO_IDENT_G": [
        ["ATRIB", "EXPRESSAO_G"],               # Atribuição de variável
        ["LPAREN", "ARGUMENTOS_G", "RPAREN"]    # Chamada de função
    ],

    # Bloco opcional SENÃO
    "SENAO_G": [["SENAO", "LCHAVE", "COMANDOS_G", "RCHAVE"], ["ε"]],

    # Argumentos de uma função (chamada)
    "ARGUMENTOS_G": [["EXPRESSAO_G", "ARGUMENTOS_RESTO_G"], ["ε"]],
    "ARGUMENTOS_RESTO_G": [["VIRGULA", "EXPRESSAO_G", "ARGUMENTOS_RESTO_G"], ["ε"]],

    # Expressões
    "EXPRESSAO_G": [["EXPR_LOGICA_G"]],

    # Lógicas Binárias
    "EXPR_LOGICA_G": [["EXPR_COMPAR_G", "EXPR_LOGICA_RESTO_G"]],
    "EXPR_LOGICA_RESTO_G": [["OPER_LOGI_BIN", "EXPR_COMPAR_G", "EXPR_LOGICA_RESTO_G"], ["ε"]],

    # Comparativas
    "EXPR_COMPAR_G": [["EXPR_ARITMETICA_G", "EXPR_COMPAR_RESTO_G"]],
    "EXPR_COMPAR_RESTO_G": [["COMPAR", "EXPR_ARITMETICA_G", "EXPR_COMPAR_RESTO_G"], ["ε"]],

    # Aritméticas
    "EXPR_ARITMETICA_G": [["TERMO_G", "EXPR_ARITMETICA_RESTO_G"]],
    "EXPR_ARITMETICA_RESTO_G": [["OPER_ARIT", "TERMO_G", "EXPR_ARITMETICA_RESTO_G"], ["ε"]],

    # Termos
    "TERMO_G": [["FATOR_G", "TERMO_RESTO_G"]],
    "TERMO_RESTO_G": [["OPER_ARIT", "FATOR_G", "TERMO_RESTO_G"], ["ε"]],

    # Fatores podem ser números, variáveis, strings, booleanos, etc.
    "FATOR_G": [
        ["LPAREN", "EXPRESSAO_G", "RPAREN"],  # Expressão entre parênteses
        ["OPER_LOGI_UN", "FATOR_G"],          # Operador lógico unário (not)
        ["IDENT", "FATOR_IDENT_G"],           # Identificador
        ["NUMERO_INT"],                       # Inteiro
        ["NUMERO_REAL"],                      # Real
        ["PALAVRA"],                          # String/palavra
        ["CARACTERE"],                        # Caractere
        ["BOOLEANO"]                          # Booleano (true/false)
    ],
    "FATOR_IDENT_G": [
        ["LPAREN", "ARGUMENTOS_G", "RPAREN"], # Função
        ["ε"],                                # Variável
    ],
}

# Símbolo que representa produção vazia
EPS = "ε"

# ------------------------------------------------------------
# FUNÇÕES AUXILIARES — Cálculo dos conjuntos FIRST e FOLLOW
# ------------------------------------------------------------

def all_firsts(G):
    """
    Calcula o conjunto FIRST para todos os não-terminais da gramática G.
    Retorna um dicionário {não_terminal: conjunto_de_terminais}.
    """
    EPS = "ε"
    FIRST = {nt: set() for nt in G}
    changed = True

    # Loop até não haver mais mudanças (propagação completa dos FIRSTs)
    while changed:
        changed = False
        for A, prods in G.items():
            for prod in prods:
                # Caso a produção seja ε
                if prod == [EPS]:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
                    continue

                # Percorre os símbolos da produção da esquerda para a direita
                for X in prod:
                    if X not in G:
                        # Se X é terminal, adiciona ele no FIRST de A
                        if X not in FIRST[A]:
                            FIRST[A].add(X)
                            changed = True
                        break  # para ao encontrar o primeiro terminal
                    else:
                        # Se X é não-terminal, adiciona FIRST(X) - {ε} no FIRST(A)
                        novos = FIRST[X] - {EPS}
                        if not novos.issubset(FIRST[A]):
                            FIRST[A] |= novos
                            changed = True
                        # Se X não gera ε, para o loop
                        if EPS not in FIRST[X]:
                            break
                else:
                    # Se todos os símbolos geram ε, adiciona ε em FIRST(A)
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
    return FIRST


def first(simbolo, G):
    """
    Retorna o conjunto FIRST de um símbolo específico.
    Se o símbolo for terminal, retorna ele mesmo como conjunto.
    """
    FIRST = all_firsts(G)
    if simbolo not in G:  # Se for terminal
        return {simbolo}
    return FIRST[simbolo]


def first_seq(seq, FIRST):
    """
    Calcula o FIRST de uma sequência de símbolos (ex: [A, B, c]).
    Considera a presença de ε corretamente.
    """
    EPS = "ε"
    result = set()
    for X in seq:
        # Adiciona FIRST(X) - {ε}
        result |= (FIRST.get(X, {X}) - {EPS})
        # Se X não gera ε, interrompe
        if EPS not in FIRST.get(X, set()):
            break
    else:
        # Se todos os símbolos geram ε, adiciona ε no resultado
        result.add(EPS)
    return result


def follow(nao_terminal, grammar, start_symbol):
    """
    Calcula o conjunto FOLLOW de um não-terminal específico.
    FOLLOW(A) contém os terminais que podem aparecer à direita de A
    em alguma produção, durante a derivação da gramática.
    """
    EPS = "ε"
    FIRST = all_firsts(grammar)
    FOLLOW = {nt: set() for nt in grammar}

    # O símbolo inicial sempre contém EOF no FOLLOW
    FOLLOW[start_symbol].add("EOF")

    changed = True
    while changed:
        changed = False
        for A, producoes in grammar.items():
            for prod in producoes:
                for i, simbolo in enumerate(prod):
                    if simbolo in grammar:  # Se é não-terminal
                        resto = prod[i + 1:]  # Símbolos que vêm depois dele

                        if resto:
                            # FIRST do que vem depois
                            first_resto = first_seq(resto, FIRST)
                            # Adiciona FIRST(resto) - {ε} no FOLLOW(simbolo)
                            for t in first_resto - {EPS}:
                                if t not in FOLLOW[simbolo]:
                                    FOLLOW[simbolo].add(t)
                                    changed = True
                            # Se ε está no FIRST(resto), propaga FOLLOW(A)
                            if EPS in first_resto:
                                for t in FOLLOW[A]:
                                    if t not in FOLLOW[simbolo]:
                                        FOLLOW[simbolo].add(t)
                                        changed = True
                        else:
                            # Se simbolo está no fim da produção,
                            # propaga FOLLOW(A) → FOLLOW(simbolo)
                            for t in FOLLOW[A]:
                                if t not in FOLLOW[simbolo]:
                                    FOLLOW[simbolo].add(t)
                                    changed = True
    # Retorna apenas o FOLLOW do não-terminal solicitado
    return FOLLOW[nao_terminal]