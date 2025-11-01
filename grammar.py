# grammar.py
grammar = {
    # ======= PROGRAMA =======
    "PROGRAMA": [["DECL_FUNCOES", "FUNCAO_PRINCIPAL"]],

    # ======= FUNÇÕES =======
    "DECL_FUNCOES": [["FUNCAO_DEF", "DECL_FUNCOES"], ["ε"]],
    "FUNCAO_DEF": [["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS_OPC", "RPAREN", "BLOCO"]],
    "FUNCAO_PRINCIPAL": [["PRINCIPAL", "BLOCO"]],

    # ======= BLOCOS =======
    "BLOCO": [["LCHAVE", "DECLS_COMANDOS", "RCHAVE"]],
    "DECLS_COMANDOS": [
        ["COMANDO", "DECLS_COMANDOS"],
        ["ε"]
    ],

    # ======= COMANDOS =======
    "COMANDO": [
        ["DECLARACAO"], ["SE_INST"], ["ENQUANTO_INST"], ["FACA_INST"],
        ["PARA_INST"], ["RETORNO_INST"], ["ATRIB_INST"], ["ESCREVER_INST"]
    ],

    "SE_INST": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_PARTE"]],
    "SENAO_PARTE": [["SENAO", "BLOCO"], ["ε"]],
    "ENQUANTO_INST": [["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"]],
    "FACA_INST": [["FACA", "BLOCO", "ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "PONTOVIRG"]],

    # Para corrigir o for (não usar PONTOVIRG dentro do cabeçalho)
    "ATRIB_FOR": [["IDENT", "ATRIB", "EXPRESSAO"]],
    "PARA_INST": [["PARA", "LPAREN", "ATRIB_FOR", "PONTOVIRG",
                   "EXPRESSAO", "PONTOVIRG", "ATRIB_FOR", "RPAREN", "BLOCO"]],

    "RETORNO_INST": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],
    "ESCREVER_INST": [["ESCREVER", "LPAREN", "LISTA_ARGS", "RPAREN", "PONTOVIRG"]],

    "LISTA_ARGS": [["EXPRESSAO", "LISTA_ARGS'"]],
    "LISTA_ARGS'": [["VIRGULA", "EXPRESSAO", "LISTA_ARGS'"], ["ε"]],

    # ======= DECLARAÇÕES =======
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECL_INICIAL_OPC", "PONTOVIRG"]],
    "DECL_INICIAL_OPC": [["ATRIB", "EXPRESSAO"], ["ε"]],

    # ======= ATRIBUIÇÕES =======
    "ATRIB_INST": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],

    # ======= EXPRESSÕES =======
    "EXPRESSAO": [["EXP_LOG"]],
    "EXP_LOG": [["EXP_COMPARACAO", "EXP_LOG'"]],
    "EXP_LOG'": [["OPER_LOGI", "EXP_COMPARACAO", "EXP_LOG'"], ["ε"]],
    "EXP_COMPARACAO": [["EXP_ARIT", "EXP_COMPARACAO'"]],
    "EXP_COMPARACAO'": [["COMPAR", "EXP_ARIT", "EXP_COMPARACAO'"], ["ε"]],
    "EXP_ARIT": [["TERMO", "EXP_ARIT'"]],
    "EXP_ARIT'": [["OPER_ARIT", "TERMO", "EXP_ARIT'"], ["ε"]],

    # ======= TERMOS =======
    "TERMO": [
        ["IDENT", "TERMO_CHAMADA_OPC"],
        ["NUMERO_INT"], ["NUMERO_REAL"],
        ["PALAVRA"], ["BOOLEANO"],
        ["LPAREN", "EXPRESSAO", "RPAREN"]
    ],
    "TERMO_CHAMADA_OPC": [["LPAREN", "PARAMS_OPC", "RPAREN"], ["ε"]],
    "PARAMS_OPC": [["PARAMS"], ["ε"]],
    "PARAMS": [["EXPRESSAO", "PARAMS_CONT"]],
    "PARAMS_CONT": [["VIRGULA", "EXPRESSAO", "PARAMS_CONT"], ["ε"]],
}

# ======= FIRST =======
def first(simbolo, gramatica, visitados=None):
    if visitados is None:
        visitados = set()

    terminais = {
        "FUNCAO", "PRINCIPAL", "TIPO_VAR", "SE", "SENAO", "ENQUANTO", "FACA", "PARA",
        "RETORNO", "BOOLEANO", "NUMERO_INT", "NUMERO_REAL", "PALAVRA", "IDENT",
        "COMPAR", "OPER_ARIT", "OPER_LOGI", "ATRIB",
        "LPAREN", "RPAREN", "LCHAVE", "RCHAVE", "VIRGULA", "PONTOVIRG", "EOF"
    }

    if simbolo in terminais or simbolo not in gramatica:
        return {simbolo}

    if simbolo in visitados:
        return set()

    visitados.add(simbolo)
    conj = set()

    for producao in gramatica[simbolo]:
        vazio = True
        for s in producao:
            primeiros = first(s, gramatica, visitados.copy())
            conj |= (primeiros - {"ε"})
            if "ε" not in primeiros:
                vazio = False
                break
        if vazio:
            conj.add("ε")
    return conj

# ======= FOLLOW =======
def follow(simbolo, gramatica, inicio="PROGRAMA"):
    segundo = set()
    if simbolo == inicio:
        segundo.add("EOF")

    for cabeca, producoes in gramatica.items():
        for producao in producoes:
            for i in range(len(producao)):
                if producao[i] == simbolo:
                    if i + 1 < len(producao):
                        prox = producao[i + 1]
                        vizinhos = first(prox, gramatica)
                        segundo |= (vizinhos - {"ε"})
                        if "ε" in vizinhos:
                            segundo |= follow(cabeca, gramatica)
                    else:
                        if cabeca != simbolo:
                            segundo |= follow(cabeca, gramatica)
    return segundo
