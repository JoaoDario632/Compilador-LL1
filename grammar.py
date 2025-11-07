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


def first(X, G):
    if X not in G:
        if X == EPS:
            return {EPS}
        return {X}
    FIRST = {nt: set() for nt in G}
    mudanca = True
    while mudanca:
        mudanca = False
        for A, prods in G.items():
            for prod in prods:
                if prod == [EPS] or prod == "ε" or prod == []:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        mudanca = True
                    continue
                inserirEPS = True
                for simbolo in prod:
                    if simbolo == EPS:
                        if EPS not in FIRST[A]:
                            FIRST[A].add(EPS)
                            mudanca = True
                        inserirEPS = False
                        break
                    if simbolo not in G:
                        if simbolo not in FIRST[A]:
                            FIRST[A].add(simbolo)
                            mudanca = True
                        inserirEPS = False
                        break
                    else:
                        before = len(FIRST[A])
                        FIRST[A].update(x for x in FIRST[simbolo] if x != EPS)
                        if len(FIRST[A]) != before:
                            mudanca = True
                        if EPS in FIRST[simbolo]:
                            inserirEPS = True
                        else:
                            inserirEPS = False
                            break
                if inserirEPS:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        mudanca = True

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

    mudanca = True
    while mudanca:
        mudanca = False
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
                            mudanca = True
                    else:
                        # Caso 2: há símbolos depois de B → calcula FIRST(beta)
                        primeiro_beta = set()
                        add_follow_head = True

                        for simbolo in beta:
                            # símbolo é ε
                            if simbolo == EPS:
                                primeiro_beta.add(EPS)
                                continue

                            # símbolo terminal → adiciona e para
                            if simbolo not in G:
                                primeiro_beta.add(simbolo)
                                add_follow_head = False
                                break

                            # símbolo não-terminal → adiciona FIRST(simbolo) - {ε}
                            primeiro_beta.update(x for x in first(simbolo, G) if x != EPS)
                            if EPS in first(simbolo, G):
                                add_follow_head = True
                                continue
                            else:
                                add_follow_head = False
                                break

                        # adiciona FIRST(beta) - {ε} a FOLLOW(B)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(x for x in primeiro_beta if x != EPS)
                        if len(FOLLOW[B]) != before:
                            mudanca = True

                        # Se beta →* ε, adiciona FOLLOW(head) a FOLLOW(B)
                        if add_follow_head or (EPS in primeiro_beta):
                            before = len(FOLLOW[B])
                            FOLLOW[B].update(FOLLOW[head])
                            if len(FOLLOW[B]) != before:
                                mudanca = True

    return FOLLOW[A]
__all__ = ["grammar", "first", "follow", "EPS"]
