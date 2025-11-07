# grammar.py
from collections import defaultdict, deque
#DEFINIÇÃO DA GRAMÁTICA
# Cada não-terminal (como "PROGRAMA", "BLOCO", etc.)
# mapeia para uma lista de produções.
# Cada produção é uma lista de símbolos (terminais ou não-terminais).
# Exemplo:
#   "PROGRAMA": [["DECL_FUNCOES", "PRINCIPAL"]]
# significa que PROGRAMA → DECL_FUNCOES PRINCIPAL

grammar = {
    "PROGRAMA": [["DECL_FUNCOES", "PRINCIPAL_G"]],

    # Declaração de funções (opcional) e principal
    "DECL_FUNCOES": [["FUNCAO_G", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS", "RPAREN", "BLOCO", "DECL_FUNCOES"],
                     ["ε"]],

    # Lista de parâmetros de função
    "PARAMS": [["PARAM", "VIRGULA", "PARAMS"], ["PARAM"], ["ε"]],
    "PARAM": [["TIPO_VAR", "IDENT"]],

    "PRINCIPAL_G": [["PRINCIPAL", "BLOCO"]],

    # Estrutura de bloco: { DECLARACOES COMANDOS }
    "BLOCO": [["LCHAVE", "DECLARACOES", "COMANDOS", "RCHAVE"]],

    # Declarações de variáveis
    "DECLARACOES": [["DECLARACAO", "DECLARACOES"], ["ε"]],
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECLARACAO_OPC", "PONTOVIRG"]],
    "DECLARACAO_OPC": [["ATRIB", "EXPRESSAO"], ["ε"]],

    # Conjunto de comandos
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

    # Estrutura condicional if / else
    "SE_STAT": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_OPT"]],
    "SENAO_OPT": [["SENAO", "BLOCO"], ["ε"]],

    # Estrutura de repetição while
    "ENQUANTO_STAT": [["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"]],

    # Estrutura do-while: faca { } enquanto(expr);
    "FACA_STAT": [["FACA", "BLOCO"]],

    # Estrutura for
    # Simplificada: PARA ( DECLARACAO_PARA ; EXPRESSAO ; ATRIBUICAO ) BLOCO
    "PARA_STAT": [[
        "PARA", "LPAREN", "DECLARACAO_PARA", "PONTOVIRG", "EXPRESSAO",
        "PONTOVIRG", "ATRIBUICAO", "RPAREN", "BLOCO"
    ]],
    "DECLARACAO_PARA": [["TIPO_VAR", "IDENT", "ATRIB", "EXPRESSAO"], ["IDENT", "ATRIB", "EXPRESSAO"]],

    # Comando de saída
    "ESCREVER_STAT": [["ESCREVER", "LPAREN", "ARGUMENTOS", "RPAREN", "PONTOVIRG"]],

    # Retorno de função
    "RETORNO_STAT": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # Expressões aritméticas e booleanas
    "EXPRESSAO": [["TERMO", "EXPRESSAO_PRIME"]],
    "EXPRESSAO_PRIME": [
        ["OPER_ARIT", "TERMO", "EXPRESSAO_PRIME"],
        ["OPER_LOGI", "TERMO", "EXPRESSAO_PRIME"],
        ["ε"]
    ],

    # Termos de expressão (valores ou subexpressões)
    "TERMO": [
        ["IDENT"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["PALAVRA"],
        ["BOOLEANO"],
        ["LPAREN", "EXPRESSAO", "RPAREN"]
    ],

    # Função (declaração)
    "FUNCAO_G": [["FUNCAO"]],  # token 'funcao' já é reconhecido como FUNCAO pelo scanner; a produção real vem em DECL_FUNCOES

    # Tokens terminais (na prática, aparecem como terminais nas regras acima)
    # Não precisamos listá-los aqui — eles são aqueles que não aparecem como chaves de grammar.
}

# Símbolo especial epsilon
EPS = "ε"

# FUNÇÕES AUXILIARES

def is_nonterminal(sym):
    """
    Retorna True se o símbolo for um não-terminal (aparece nas chaves da gramática).
    Caso contrário, retorna False.
    """
    return sym in grammar


#               CÁLCULO DO CONJUNTO FIRST
def first(X, G):
    """
    Retorna o conjunto FIRST(X):
      - Se X é terminal, FIRST(X) = {X}
      - Se X é não-terminal, FIRST(X) é calculado por fixpoint
        considerando todas as produções de X.

    O conjunto FIRST contém todos os símbolos terminais
    que podem iniciar uma sentença derivada de X.
    """
    # Caso base: X é terminal
    if X not in G:
        if X == EPS:
            return {EPS}
        return {X}

    # Inicializa dicionário FIRST para todos os não-terminais
    FIRST = {nt: set() for nt in G}
    changed = True  # flag para detectar mudanças

    # Laço até estabilizar (não há mais mudanças nos conjuntos)
    while changed:
        changed = False
        for A, prods in G.items():  # percorre cada não-terminal e suas produções
            for prod in prods:
                # Produção vazia → adiciona ε
                if prod == [EPS] or prod == "ε" or prod == []:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
                    continue

                add_eps = True  # indica se ε pode propagar
                for symbol in prod:
                    # Caso o símbolo seja ε
                    if symbol == EPS:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS)
                            changed = True
                        add_eps = False
                        break

                    # Caso o símbolo seja terminal
                    if symbol not in G:
                        if symbol not in FIRST[A]:
                            FIRST[A].add(symbol)
                            changed = True
                        add_eps = False
                        break

                    # Caso o símbolo seja não-terminal
                    else:
                        # Adiciona FIRST(symbol) - {ε}
                        before = len(FIRST[A])
                        FIRST[A].update(x for x in FIRST[symbol] if x != EPS)
                        if len(FIRST[A]) != before:
                            changed = True

                        # Se FIRST(symbol) contém ε, continua para o próximo símbolo
                        if EPS in FIRST[symbol]:
                            add_eps = True
                        else:
                            add_eps = False
                            break

                # Se todos os símbolos da produção podem gerar ε, adiciona ε
                if add_eps:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True

    return FIRST[X]


#               CÁLCULO DO CONJUNTO FOLLOW
def follow(A, G):
    """
    Retorna o conjunto FOLLOW(A):
      - FIRST de símbolos à direita de A nas produções
      - FOLLOW do não-terminal à esquerda se A for o último
      - O símbolo inicial sempre contém EOF
    """
    # Inicializa FOLLOW vazio para todos os não-terminais
    FOLLOW = {nt: set() for nt in G}

    # O primeiro símbolo da gramática recebe 'EOF'
    start = list(G.keys())[0]
    FOLLOW[start].add("EOF")

    changed = True
    while changed:
        changed = False
        for head, prods in G.items():
            for prod in prods:
                # ignora produções vazias
                if prod == [EPS] or prod == "ε":
                    continue
                # percorre símbolos da produção
                for i, B in enumerate(prod):
                    # ignora terminais
                    if B not in G:
                        continue

                    beta = prod[i + 1:]  # parte da produção após B

                    # Caso 1: B é o último símbolo → adiciona FOLLOW(head)
                    if not beta:
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(FOLLOW[head])
                        if len(FOLLOW[B]) != before:
                            changed = True
                    else:
                        # Caso 2: há símbolos depois de B → calcula FIRST(beta)
                        primeiro_beta = set()
                        add_follow_head = True

                        for symbol in beta:
                            # símbolo é ε
                            if symbol == EPS:
                                primeiro_beta.add(EPS)
                                continue

                            # símbolo terminal → adiciona e para
                            if symbol not in G:
                                primeiro_beta.add(symbol)
                                add_follow_head = False
                                break

                            # símbolo não-terminal → adiciona FIRST(symbol) - {ε}
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

                        # Se beta →* ε, adiciona FOLLOW(head) a FOLLOW(B)
                        if add_follow_head or (EPS in primeiro_beta):
                            before = len(FOLLOW[B])
                            FOLLOW[B].update(FOLLOW[head])
                            if len(FOLLOW[B]) != before:
                                changed = True

    return FOLLOW[A]
__all__ = ["grammar", "first", "follow", "EPS"]
