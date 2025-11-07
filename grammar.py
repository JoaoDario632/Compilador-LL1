# grammar.py
from collections import defaultdict, deque

grammar = {
    "PROGRAMA_G": [["DECL_FUNCOES_G", "PRINCIPAL_G"]],

    # Declaração de funções
    "DECL_FUNCOES_G": [["FUNCAO", "IDENT", "LPAREN", "PARAMS_G", "RPAREN", "LCHAVE", "CORPO_G", "RCHAVE", "DECL_FUNCOES_G"], ["ε"]],

    # Função principal
    "PRINCIPAL_G": [["PRINCIPAL", "LPAREN", "RPAREN", "LCHAVE", "CORPO_G", "RCHAVE"]],

    # Parâmetros de função
    "PARAMS_G": [["TIPO_VAR", "IDENT", "PARAMS_RESTO_G"], ["ε"]],
    "PARAMS_RESTO_G": [["VIRGULA", "TIPO_VAR", "IDENT", "PARAMS_RESTO_G"], ["ε"]],

    # Corpo da função
    "CORPO_G": [["DECLARACOES_G", "COMANDOS_G"]],
    "DECLARACOES_G": [["TIPO_VAR", "IDENT", "DECLARACOES_RESTO_G", "PONTOVIRG", "DECLARACOES_G"], ["ε"]],
    "DECLARACOES_RESTO_G": [["VIRGULA", "IDENT", "DECLARACOES_RESTO_G"], ["ε"]],

    # Lista de comandos
    "COMANDOS_G": [["COMANDO_G", "COMANDOS_G"], ["ε"]],

    # Comandos
    "COMANDO_G": [
        ["SE", "LPAREN", "EXPRESSAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE", "SENAO_G"],
        ["ENQUANTO", "LPAREN", "EXPRESSAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE"],
        ["PARA", "LPAREN", "ATRIBUICAO_G", "PONTOVIRG", "EXPRESSAO_G", "PONTOVIRG", "ATRIBUICAO_G", "RPAREN", "LCHAVE", "COMANDOS_G", "RCHAVE"],
        ["ESCREVER", "LPAREN", "ARGUMENTOS_G", "RPAREN", "PONTOVIRG"],
        ["RETORNO", "EXPRESSAO_G", "PONTOVIRG"],
        ["ATRIBUICAO_G", "PONTOVIRG"]
    ],

    "SENAO_G": [["SENAO", "LCHAVE", "COMANDOS_G", "RCHAVE"], ["ε"]],

    # Atribuição
    "ATRIBUICAO_G": [["IDENT", "ATRIB", "EXPRESSAO_G"]],

    # Argumentos
    "ARGUMENTOS_G": [["EXPRESSAO_G", "ARGUMENTOS_RESTO_G"], ["ε"]],
    "ARGUMENTOS_RESTO_G": [["VIRGULA", "EXPRESSAO_G", "ARGUMENTOS_RESTO_G"], ["ε"]],

    # Expressões
    "EXPRESSAO_G": [["TERMO_G", "EXPRESSAO_RESTO_G"]],
    "EXPRESSAO_RESTO_G": [["OPER_ARIT", "TERMO_G", "EXPRESSAO_RESTO_G"], ["ε"]],
    "TERMO_G": [["FATOR_G", "TERMO_RESTO_G"]],
    "TERMO_RESTO_G": [["OPER_ARIT", "FATOR_G", "TERMO_RESTO_G"], ["ε"]],
    "FATOR_G": [
        ["LPAREN", "EXPRESSAO_G", "RPAREN"],
        ["IDENT"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["PALAVRA"],
        ["CARACTERE"],
        ["BOOLEANO"]
    ],
}

EPS = "ε"

# --------------------------------------------
# Funções auxiliares para FIRST e FOLLOW
# --------------------------------------------

def all_firsts(G):
    EPS = "ε"
    FIRST = {nt: set() for nt in G}
    changed = True
    while changed:
        changed = False
        for A, prods in G.items():
            for prod in prods:
                if prod == [EPS]:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
                    continue
                for X in prod:
                    if X not in G:  # terminal
                        if X not in FIRST[A]:
                            FIRST[A].add(X)
                            changed = True
                        break
                    else:  # não-terminal
                        novos = FIRST[X] - {EPS}
                        if not novos.issubset(FIRST[A]):
                            FIRST[A] |= novos
                            changed = True
                        if EPS not in FIRST[X]:
                            break
                else:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
    return FIRST


def first(simbolo, G):
    FIRST = all_firsts(G)
    # ✅ Agora funciona tanto para terminais quanto não-terminais
    if simbolo not in G:
        return {simbolo}
    return FIRST[simbolo]


def first_seq(seq, FIRST):
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
    EPS = "ε"
    FIRST = all_firsts(grammar)
    FOLLOW = {nt: set() for nt in grammar}

    # ✅ Garante que todas as chaves existem
    for nt in grammar:
        if nt not in FOLLOW:
            FOLLOW[nt] = set()

    # ✅ Adiciona EOF ao símbolo inicial
    FOLLOW[start_symbol].add("EOF")

    changed = True
    while changed:
        changed = False
        for A, producoes in grammar.items():
            for prod in producoes:
                for i, simbolo in enumerate(prod):
                    if simbolo in grammar:  # é não-terminal
                        resto = prod[i + 1:]
                        if resto:
                            first_resto = first_seq(resto, FIRST)
                            for t in first_resto - {EPS}:
                                if t not in FOLLOW[simbolo]:
                                    FOLLOW[simbolo].add(t)
                                    changed = True
                            if EPS in first_resto:
                                for t in FOLLOW[A]:
                                    if t not in FOLLOW[simbolo]:
                                        FOLLOW[simbolo].add(t)
                                        changed = True
                        else:
                            for t in FOLLOW[A]:
                                if t not in FOLLOW[simbolo]:
                                    FOLLOW[simbolo].add(t)
                                    changed = True
    return FOLLOW[nao_terminal]
