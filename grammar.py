grammar = {
    # O programa pode começar com funções e/ou declarações antes do bloco principal
    "PROGRAMA": [["DECLARACOES", "PRINCIPAL_BLOCO"]],

    # Declarações no topo — podem ser funções ou variáveis
    "DECLARACOES": [
        ["FUNCAO_DECL", "DECLARACOES"],
        ["DECLARACAO", "DECLARACOES"],
        ["ε"]
    ],

    # Função principal obrigatória
    "PRINCIPAL_BLOCO": [["PRINCIPAL", "LCHAVE", "INSTRUCOES", "RCHAVE"]],

    # Definição de função
    "FUNCAO_DECL": [["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS", "RPAREN", "FUNCAO_CORPO"]],
    "PARAMS": [["TIPO_VAR", "IDENT", "PARAMS'"], ["ε"]],
    "PARAMS'": [["VIRGULA", "TIPO_VAR", "IDENT", "PARAMS'"], ["ε"]],
    "FUNCAO_CORPO": [["LCHAVE", "INSTRUCOES", "RCHAVE"]],

    # Blocos de código
    "BLOCO": [["LCHAVE", "INSTRUCOES", "RCHAVE"]],

  "INSTRUCAO": [
    ["DECLARACAO"],
    ["ATRIBUICAO"],
    ["CONDICIONAL"],
    ["LOOP"],
    ["RETORNO_INST"], 
    ["CHAMADA_INST"],
    ["ESCRITA"]
],


    # Retorno de função
    "RETORNO_INST": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # Declarações de variáveis
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECLARACAO_OPC"]],
    "DECLARACAO_OPC": [["ATRIB", "EXPRESSAO", "PONTOVIRG"], ["PONTOVIRG"]],

    # Atribuições e retorno
    "ATRIBUICAO": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],
    "RETORNO": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # Estruturas de controle
    "CONDICIONAL": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_OPC"]],
    "SENAO_OPC": [["SENAO", "BLOCO"], ["ε"]],

    "LOOP": [
        ["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"],
        ["FACA", "BLOCO", "ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "PONTOVIRG"],
        ["PARA", "LPAREN", "DECLARACAO", "EXPRESSAO", "PONTOVIRG", "ATRIBUICAO", "RPAREN", "BLOCO"]
    ],

    # Escrita e chamadas
    "ESCRITA": [["IDENT", "LPAREN", "ARG_LIST", "RPAREN", "PONTOVIRG"]],
    "CHAMADA_TERM": [["IDENT", "LPAREN", "ARG_LIST", "RPAREN"]],
    "CHAMADA_INST": [["CHAMADA_TERM", "PONTOVIRG"]],

    # Expressões
    "ARG_LIST": [["EXPRESSAO", "ARG_LIST'"], ["ε"]],
    "ARG_LIST'": [["VIRGULA", "EXPRESSAO", "ARG_LIST'"], ["ε"]],
    "EXPRESSAO": [["TERMO", "EXPRESSAO'"]],
    "EXPRESSAO'": [["OPER_ARIT", "TERMO", "EXPRESSAO'"], ["COMPAR", "TERMO", "EXPRESSAO'"], ["ε"]],
    "TERMO": [
        ["IDENT"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["PALAVRA"],
        ["BOOLEANO"],
        ["LPAREN", "EXPRESSAO", "RPAREN"],
        ["CHAMADA_TERM"]
    ],
}


def first(symbol, grammar, visitado=None):
    if visitado is None:
        visitado = set()
    if symbol not in grammar:
        return {symbol}
    if symbol in visitado:
        return set()
    visitado.add(symbol)
    firstSet = set()
    for rule in grammar[symbol]:
        for sym in rule:
            f = first(sym, grammar, visitado.copy())
            firstSet |= (f - {"ε"})
            if "ε" not in f:
                break
        else:
            firstSet.add("ε")
    return firstSet


def follow(symbol, grammar, start_symbol="PROGRAMA"):
    followset = set()
    if symbol == start_symbol:
        followset.add("EOF")
    for head, bodies in grammar.items():
        for body in bodies:
            for i, sym in enumerate(body):
                if sym == symbol:
                    if i + 1 < len(body):
                        next_sym = body[i + 1]
                        followset |= (first(next_sym, grammar) - {"ε"})
                        if "ε" in first(next_sym, grammar):
                            followset |= follow(head, grammar)
                    else:
                        if head != symbol:
                            followset |= follow(head, grammar)
    return followset