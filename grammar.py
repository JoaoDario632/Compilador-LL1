# grammar.py — Definição da gramática do compilador Brick + FIRST e FOLLOW
from collections import defaultdict, deque
# GRAMÁTICA DA LINGUAGEM "BRICK
# Cada não-terminal aponta para uma lista de produções.
# Cada produção é uma lista de símbolos terminais ou não-terminais.
# O símbolo "ε" representa a produção vazia

grammar = {
    # Programa composto por declarações de funções + função principal obrigatória.
    "PROGRAMA_G": [["DECL_FUNCOES_G", "PRINCIPAL_G"]],

    # Lista recursiva de funções. Pode ser vazia.
    "DECL_FUNCOES_G": [
        ["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE", "DECL_FUNCOES_G"],
        ["ε"]
    ],

    # Chamada de função simples
    "CHAM_FUNCOES_G": [["IDENT", "LPAREN", "ARGUMENTOS_G", "RPAREN"]],

    # Bloco principal obrigatório
    "PRINCIPAL_G": [["PRINCIPAL", "LCHAVE", "COMANDOS_G", "RCHAVE"]],

    # Parâmetros formais da função
    "PARAMS_G": [["TIPO_VAR", "IDENT", "PARAMS_RESTO_G"], ["ε"]],
    "PARAMS_RESTO_G": [["VIRGULA", "TIPO_VAR", "IDENT", "PARAMS_RESTO_G"], ["ε"]],

    # Lista de comandos
    "COMANDOS_G": [["COMANDO_G", "COMANDOS_G"], ["ε"]],

    # Categoria principal dos comandos da linguagem
    "COMANDO_G": [
        ["DECLARACOES_G", "PONTOVIRG"],                           # Declaração de variável
        ["IDENT", "ELEMENTO_IDENT_G", "PONTOVIRG"],               # Ident seguido de atribuição ou chamada
        ["SE", "LPAREN", "EXPRESSAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE", "SENAO_G"],  # Condicional
        ["ENQUANTO", "LPAREN", "EXPRESSAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE"],       # While
        ["FACA", "LCHAVE", "COMANDOS_G", "RCHAVE", "ENQUANTO", "LPAREN", "EXPRESSAO_G", "RPAREN", "PONTOVIRG"], # Do-while
        ["PARA", "LPAREN", "DECL_OU_ATRIB_G", "PONTOVIRG", "EXPRESSAO_G", "PONTOVIRG", "ATRIBUICAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE"],  # For
        ["RETORNO", "EXPRESSAO_G", "PONTOVIRG"]                   # Return
    ],

    # Produção que aceita declarações ou atribuições
    "DECL_OU_ATRIB_G": [["DECLARACOES_G"], ["ATRIBUICAO_G"]],

    # Declarações locais
    "DECLARACOES_G": [
        ["TIPO_VAR", "IDENT", "DECLARACOES_ATRIB_G", "DECLARACOES_RESTO_G"]
    ],
    "DECLARACOES_RESTO_G": [["VIRGULA", "IDENT", "DECLARACOES_ATRIB_G", "DECLARACOES_RESTO_G"], ["ε"]],
    "DECLARACOES_ATRIB_G": [["ATRIB", "EXPRESSAO_G"], ["ε"]],

    # Atribuição
    "ATRIBUICAO_G": [["IDENT", "ATRIB", "EXPRESSAO_G"]],

    # Elemento que segue um identificador: atribuição ou chamada
    "ELEMENTO_IDENT_G": [
        ["ATRIB", "EXPRESSAO_G"],
        ["LPAREN", "ARGUMENTOS_G", "RPAREN"]
    ],

    # Ramo opcional
    "SENAO_G": [["SENAO", "LCHAVE", "COMANDOS_G", "RCHAVE"], ["ε"]],

    # Argumentos de chamada de função
    "ARGUMENTOS_G": [["EXPRESSAO_G", "ARGUMENTOS_RESTO_G"], ["ε"]],
    "ARGUMENTOS_RESTO_G": [["VIRGULA", "EXPRESSAO_G", "ARGUMENTOS_RESTO_G"], ["ε"]],

    # Expressões lógicas, comparativas e aritméticas
    "EXPRESSAO_G": [["EXPR_LOGICA_G"]],

    # Expressões lógicas binárias
    "EXPR_LOGICA_G": [["EXPR_COMPAR_G", "EXPR_LOGICA_RESTO_G"]],
    "EXPR_LOGICA_RESTO_G": [["OPER_LOGI_BIN", "EXPR_COMPAR_G", "EXPR_LOGICA_RESTO_G"], ["ε"]],

    # Expressões comparativas
    "EXPR_COMPAR_G": [["EXPR_ARITMETICA_G", "EXPR_COMPAR_RESTO_G"]],
    "EXPR_COMPAR_RESTO_G": [["COMPAR", "EXPR_ARITMETICA_G", "EXPR_COMPAR_RESTO_G"], ["ε"]],

    # Expressões aritméticas
    "EXPR_ARITMETICA_G": [["TERMO_G", "EXPR_ARITMETICA_RESTO_G"]],
    "EXPR_ARITMETICA_RESTO_G": [["OPER_ARIT", "TERMO_G", "EXPR_ARITMETICA_RESTO_G"], ["ε"]],

    # Termos
    "TERMO_G": [["FATOR_G", "TERMO_RESTO_G"]],
    "TERMO_RESTO_G": [["OPER_ARIT", "FATOR_G", "TERMO_RESTO_G"], ["ε"]],

    # Valores possíveis de expressão
    "FATOR_G": [
        ["LPAREN", "EXPRESSAO_G", "RPAREN"],
        ["OPER_LOGI_UN", "FATOR_G"],
        ["IDENT", "FATOR_IDENT_G"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["PALAVRA"],
        ["CARACTERE"],
        ["BOOLEANO"]
    ],

    # Identificação de função ou variável
    "FATOR_IDENT_G": [
        ["LPAREN", "ARGUMENTOS_G", "RPAREN"],
        ["ε"]
    ],
}

EPS = "ε"

def all_firsts(G):
    """
    Calcula FIRST(X) para TODOS os não-terminais.
    """
    EPS = "ε"
    FIRST = {nt: set() for nt in G}

    changed = True
    while changed:
        changed = False

        for A, prods in G.items():
            for prod in prods:

                # Produção epsilon
                if prod == [EPS]:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
                    continue

                # Percorre símbolos da produção
                for X in prod:
                    # X é terminal → FIRST(A) recebe X
                    if X not in G:
                        if X not in FIRST[A]:
                            FIRST[A].add(X)
                            changed = True
                        break
                    else:
                        # X é não-terminal → copia FIRST(X) sem epsilon
                        novos = FIRST[X] - {EPS}
                        if not novos.issubset(FIRST[A]):
                            FIRST[A] |= novos
                            changed = True

                        # Se FIRST(X) não contém epsilon, para
                        if EPS not in FIRST[X]:
                            break
                else:
                    # Todos continham epsilon → adiciona epsilon
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True

    return FIRST


def first(simbolo, G):
    """
    FIRST de um único símbolo.
    """
    FIRST = all_firsts(G)
    if simbolo not in G:
        return {simbolo}
    return FIRST[simbolo]


def first_seq(seq, FIRST):
    """
    FIRST de uma sequência de símbolos.
    """
    EPS = "ε"
    result = set()

    for X in seq:
        result |= (FIRST.get(X, {X}) - {EPS})
        if EPS not in FIRST.get(X, set()):
            break
    else:
        result.add(EPS)

    return result


def follow(nao_terminal, grammar, start_symbol):
    """
    Implementação completa de FOLLOW(X).
    """
    EPS = "ε"
    FIRST = all_firsts(grammar)
    FOLLOW = {nt: set() for nt in grammar}

    # EOF pertence ao símbolo inicial
    FOLLOW[start_symbol].add("EOF")

    changed = True
    while changed:
        changed = False

        # Percorre toda a gramática
        for A, producoes in grammar.items():
            for prod in producoes:
                for i, simbolo in enumerate(prod):
                    if simbolo in grammar:  # é não-terminal
                        resto = prod[i + 1:]

                        # Caso exista sequência à direita
                        if resto:
                            first_resto = first_seq(resto, FIRST)

                            # Adiciona FIRST(resto) - epsilon
                            for t in first_resto - {EPS}:
                                if t not in FOLLOW[simbolo]:
                                    FOLLOW[simbolo].add(t)
                                    changed = True

                            # Se resto produz epsilon → FOLLOW(A) também pertence
                            if EPS in first_resto:
                                for t in FOLLOW[A]:
                                    if t not in FOLLOW[simbolo]:
                                        FOLLOW[simbolo].add(t)
                                        changed = True

                        else:
                            # Não há resto → FOLLOW(A) pertence a FOLLOW(simbolo)
                            for t in FOLLOW[A]:
                                if t not in FOLLOW[simbolo]:
                                    FOLLOW[simbolo].add(t)
                                    changed = True

    return FOLLOW[nao_terminal]
