grammar = {
    "PROGRAMA": [["DECLARACOES", "PRINCIPAL", "LCHAVE", "INSTRUCOES", "RCHAVE"]],

    "DECLARACOES": [
        ["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS", "RPAREN", "FUNCAO_CORPO", "DECLARACOES"],
        ["TIPO_VAR", "IDENT", "DECLARACAO_OPC", "DECLARACOES"],
        ["ε"]
    ],
    "FUNCAO_CORPO": [["LCHAVE", "INSTRUCOES", "RCHAVE"]],
    "BLOCO": [["LCHAVE", "INSTRUCOES", "RCHAVE"]],

    "INSTRUCOES": [["INSTRUCAO", "INSTRUCOES"], ["ε"]],
    "INSTRUCAO": [
        ["DECLARACAO"],
        ["ATRIBUICAO"],
        ["CONDICIONAL"],
        ["LOOP"],
        ["RETORNO"],
        ["CHAMADA_INST"],
        ["ESCRITA"],
        ["FUNCAO"]  # permite funções também como instrução
    ],

    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECLARACAO_OPC"]],
    "DECLARACAO_OPC": [["ATRIB", "EXPRESSAO", "PONTOVIRG"], ["PONTOVIRG"]],
    "ATRIBUICAO": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],

    "RETORNO": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    "CONDICIONAL": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_OPC"]],
    "SENAO_OPC": [["SENAO", "BLOCO"], ["ε"]],

    "LOOP": [
        ["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"],
        ["FACA", "BLOCO", "ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "PONTOVIRG"],
        ["PARA", "LPAREN", "DECLARACAO", "EXPRESSAO", "PONTOVIRG", "ATRIBUICAO", "RPAREN", "BLOCO"]
    ],

    "ESCRITA": [["IDENT", "LPAREN", "ARG_LIST", "RPAREN", "PONTOVIRG"]],
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

    "CHAMADA_TERM": [["IDENT", "LPAREN", "ARG_LIST", "RPAREN"]],
    "CHAMADA_INST": [["CHAMADA_TERM", "PONTOVIRG"]],
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
            f = first(sym, grammar, visitado)
            firstSet |= (f - {"ε"})
            if "ε" not in f:
                break
        else:
            firstSet.add("ε")
    return firstSet

def follow(symbol, grammar, start_symbol="PROGRAMA"):
    follwoset = set()
    if symbol == start_symbol:
        follwoset.add("EOF")
    for head, bodies in grammar.items():
        for body in bodies:
            for i, sym in enumerate(body):
                if sym == symbol:
                    if i + 1 < len(body):
                        next_sym = body[i + 1]
                        follwoset |= (first(next_sym, grammar) - {"ε"})
                        if "ε" in first(next_sym, grammar):
                            follwoset |= follow(head, grammar)
                    else:
                        if head != symbol:
                            follwoset |= follow(head, grammar)
    return follwoset
