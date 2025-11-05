# grammar.py
# Gramática para a linguagem exemplo do seu projeto
# Símbolo de epsilon: "ε"

from collections import defaultdict, deque

# -------------------------
# GRAMÁTICA (produções)
# -------------------------
# Cada cabeça mapeia para uma lista de produções; cada produção é lista de símbolos (strings)
grammar = {
    "PROGRAMA": [["DECL_FUNCOES", "PRINCIPAL"]],

    # Declaração de funções (opcional) e principal
    "DECL_FUNCOES": [["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS", "RPAREN", "BLOCO", "DECL_FUNCOES"],
                     ["ε"]],

    "PARAMS": [["PARAM", "VIRGULA", "PARAMS"], ["PARAM"], ["ε"]],
    "PARAM": [["TIPO_VAR", "IDENT"]],

    "PRINCIPAL": [["PRINCIPAL", "BLOCO"]],

    # Blocos com declarações e comandos
    "BLOCO": [["LCHAVE", "DECLARACOES", "COMANDOS", "RCHAVE"]],

    "DECLARACOES": [["DECLARACAO", "DECLARACOES"], ["ε"]],
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECLARACAO_OPC", "PONTOVIRG"]],
    "DECLARACAO_OPC": [["ATRIB", "EXPRESSAO"], ["ε"]],

    "COMANDOS": [["COMANDO", "COMANDOS"], ["ε"]],
    "COMANDO": [
        ["ATRIBUICAO"],
        ["SE_STAT"],
        ["ENQUANTO_STAT"],
        ["FACA_STAT"],
        ["PARA_STAT"],
        ["ESCREVER_STAT"],
        ["CHAMADA_FUNCAO"],
        ["RETORNO_STAT"]
    ],

    # Atribuição simples: IDENT = EXPRESSAO ;
    "ATRIBUICAO": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],

    # Chamada de função como comando: IDENT ( ARGUMENTOS ) ;
    "CHAMADA_FUNCAO": [["IDENT", "LPAREN", "ARGUMENTOS", "RPAREN", "PONTOVIRG"]],
    "ARGUMENTOS": [["EXPRESSAO", "VIRGULA", "ARGUMENTOS"], ["EXPRESSAO"], ["ε"]],

    # if / else
    "SE_STAT": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_OPT"]],
    "SENAO_OPT": [["SENAO", "BLOCO"], ["ε"]],

    # while
    "ENQUANTO_STAT": [["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"]],

    # do { } while (expr);
    "FACA_STAT": [["FACA", "BLOCO"]],

    # for: para ( TIPO_VAR IDENT = NUMERO ; IDENT COMPAR NUMERO ; IDENT ATRIB IDENT OPER_ARIT NUMERO ) BLOCO
    # Simplificamos para: PARA ( DECLARACAO_SIMPLES PONTOVIRG EXPRESSAO PONTOVIRG ATRIBUICAO_SIMPLES ) BLOCO
    "PARA_STAT": [["PARA", "LPAREN", "DECLARACAO_PARA", "PONTOVIRG", "EXPRESSAO", "PONTOVIRG", "ATRIBUICAO", "RPAREN", "BLOCO"]],
    "DECLARACAO_PARA": [["TIPO_VAR", "IDENT", "ATRIB", "EXPRESSAO"], ["IDENT", "ATRIB", "EXPRESSAO"]],

    "ESCREVER_STAT": [["ESCREVER", "LPAREN", "ARGUMENTOS", "RPAREN", "PONTOVIRG"]],
    "RETORNO_STAT": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # Expressões aritméticas/booleanas (simples)
    "EXPRESSAO": [["TERMO", "EXPRESSAO_PRIME"]],
    "EXPRESSAO_PRIME": [["OPER_ARIT", "TERMO", "EXPRESSAO_PRIME"], ["OPER_LOGI", "TERMO", "EXPRESSAO_PRIME"], ["ε"]],
    "TERMO": [
        ["IDENT"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["PALAVRA"],
        ["BOOLEANO"],
        ["LPAREN", "EXPRESSAO", "RPAREN"]
    ],

    # Função (declaração)
    "FUNCAO": [["FUNCAO"]],  # token 'funcao' já é reconhecido como FUNCAO pelo scanner; a produção real vem em DECL_FUNCOES

    # Tokens terminais (na prática, aparecem como terminais nas regras acima)
    # Não precisamos listá-los aqui — eles são aqueles que não aparecem como chaves de grammar.
}

# -------------------------
# UTILITÁRIAS: FIRST e FOLLOW
# -------------------------
EPS = "ε"

def is_nonterminal(sym):
    return sym in grammar

def first(X, G):
    """
    Retorna conjunto FIRST(X).
    Se X for terminal, retorna {X}.
    Se X for não-terminal, computa usando algoritmo fixpoint.
    """
    # Se for terminal (não está nas chaves), FIRST(X) = {X}
    if X not in G:
        # Para o caso especial de epsilon solicitado diretamente
        if X == EPS:
            return {EPS}
        return {X}

    # Computa FIRST para todos não-terminais (fixpoint)
    FIRST = {nt: set() for nt in G}
    changed = True

    while changed:
        changed = False
        for A, prods in G.items():
            for prod in prods:
                # prod é uma lista de símbolos
                if prod == [EPS] or prod == "ε" or prod == []:
                    # Tratamos produção vazia
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
                    continue

                add_eps = True
                for symbol in prod:
                    # obter FIRST(symbol)
                    if symbol == EPS:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS)
                            changed = True
                        add_eps = False
                        break

                    if symbol not in G:
                        # symbol é terminal
                        if symbol not in FIRST[A]:
                            FIRST[A].add(symbol)
                            changed = True
                        add_eps = False
                        break
                    else:
                        # symbol é não-terminal
                        # adiciona FIRST(symbol) - {ε}
                        before = len(FIRST[A])
                        FIRST[A].update(x for x in FIRST[symbol] if x != EPS)
                        if len(FIRST[A]) != before:
                            changed = True

                        if EPS in FIRST[symbol]:
                            add_eps = True
                            # continua para o próximo símbolo
                        else:
                            add_eps = False
                            break

                if add_eps:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True

    return FIRST[X]

def follow(A, G):
    """
    Retorna conjunto FOLLOW(A). Assume G como grammar global.
    """
    # Inicializa FOLLOW para todos não-terminais
    FOLLOW = {nt: set() for nt in G}
    # Símbolo inicial recebe EOF no follow
    start = list(G.keys())[0]
    FOLLOW[start].add("EOF")

    changed = True
    while changed:
        changed = False
        for head, prods in G.items():
            for prod in prods:
                # percorre cada símbolo na produção
                if prod == [EPS] or prod == "ε":
                    continue
                for i, B in enumerate(prod):
                    if B not in G:
                        continue
                    # beta = prod[i+1:]
                    beta = prod[i+1:]
                    if not beta:
                        # se B é o último símbolo, FOLLOW(B) inclui FOLLOW(head)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(FOLLOW[head])
                        if len(FOLLOW[B]) != before:
                            changed = True
                    else:
                        # FIRST(beta)
                        primeiro_beta = set()
                        add_follow_head = True
                        for symbol in beta:
                            if symbol == EPS:
                                primeiro_beta.add(EPS)
                                continue
                            if symbol not in G:
                                primeiro_beta.add(symbol)
                                add_follow_head = False
                                break
                            else:
                                primeiro_beta.update(x for x in first(symbol, G) if x != EPS)
                                if EPS in first(symbol, G):
                                    add_follow_head = True
                                    continue
                                else:
                                    add_follow_head = False
                                    break

                        # adiciona FIRST(beta) - {ε} a FOLLOW(B)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(x for x in primeiro_beta if x != EPS)
                        if len(FOLLOW[B]) != before:
                            changed = True

                        if add_follow_head or (EPS in primeiro_beta):
                            before = len(FOLLOW[B])
                            FOLLOW[B].update(FOLLOW[head])
                            if len(FOLLOW[B]) != before:
                                changed = True

    return FOLLOW[A]

# Exporta para os módulos que importam
__all__ = ["grammar", "first", "follow", "EPS"]
