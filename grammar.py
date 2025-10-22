grammar = {
    # PROGRAMA
    "PROGRAMA": [["DECLARACOES", "PRINCIPAL_BLOCO"]],

    # Declarações antes do principal
    "DECLARACOES": [
        ["FUNCAO_DECL", "DECLARACOES"],
        ["DECLARACAO", "DECLARACOES"],
        ["ε"]
    ],

    # Bloco principal
    "PRINCIPAL_BLOCO": [["PRINCIPAL", "LCHAVE", "INSTRUCOES", "RCHAVE"]],

    # Funções
    "FUNCAO_DECL": [["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS", "RPAREN", "FUNCAO_CORPO"]],
    "FUNCAO_CORPO": [["LCHAVE", "INSTRUCOES", "RCHAVE"]],

    "PARAMS": [["TIPO_VAR", "IDENT", "PARAMS_OPC"], ["ε"]],
    "PARAMS_OPC": [["VIRGULA", "TIPO_VAR", "IDENT", "PARAMS_OPC"], ["ε"]],

    # Tipos de variáveis (agora inclui cadeia)
    "TIPO_VAR": [
        ["INT"],
        ["FLOAT"],
        ["STRING"],
        ["BOOL"],
        ["CADEIA"]
    ],

    # Bloco genérico
    "BLOCO": [["LCHAVE", "INSTRUCOES", "RCHAVE"]],

    # Sequência de instruções
    "INSTRUCOES": [
        ["INSTRUCAO", "INSTRUCOES"],
        ["ε"]
    ],

    # Instrução genérica
    "INSTRUCAO": [
        ["DECLARACAO"],
        ["ATRIBUICAO"],
        ["CONDICIONAL"],
        ["LOOP"],
        ["RETORNO_INST"],
        ["CHAMADA_INST"],
        ["ESCRITA"]
    ],

    # Declarações
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECLARACAO_OPC"]],
    "DECLARACAO_OPC": [["ATRIB", "EXPRESSAO", "PONTOVIRG"], ["PONTOVIRG"]],

    # Atribuições
    "ATRIBUICAO": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],

    # Retorno
    "RETORNO_INST": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # Estruturas de controle
    "CONDICIONAL": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_OPC"]],
    "SENAO_OPC": [["SENAO", "BLOCO"], ["ε"]],

    # Loops
    "LOOP": [
        ["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"],
        ["FACA", "BLOCO", "ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "PONTOVIRG"],
        ["PARA", "LPAREN", "DECLARACAO_PARA", "EXPRESSAO", "PONTOVIRG", "ATRIBUICAO", "RPAREN", "BLOCO"]
    ],

    # Declaração dentro do "para"
    "DECLARACAO_PARA": [["TIPO_VAR", "IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],

    # Escrita
    "ESCRITA": [["ESCREVER", "LPAREN", "ARG_LIST", "RPAREN", "PONTOVIRG"]],

    # Chamada de função
    "CHAMADA_TERM": [["IDENT", "LPAREN", "ARG_LIST", "RPAREN"]],
    "CHAMADA_INST": [["CHAMADA_TERM", "PONTOVIRG"]],

    # Argumentos
    "ARG_LIST": [["EXPRESSAO", "ARG_LIST_OPC"], ["ε"]],
    "ARG_LIST_OPC": [["VIRGULA", "EXPRESSAO", "ARG_LIST_OPC"], ["ε"]],

    # Expressões
    "EXPRESSAO": [["TERMO", "EXPRESSAO_OPC"]],
    "EXPRESSAO_OPC": [
        ["OPER_ARIT", "TERMO", "EXPRESSAO_OPC"],
        ["COMPAR", "TERMO", "EXPRESSAO_OPC"],
        ["ε"]
    ],

    "TERMO": [
        ["IDENT"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["PALAVRA"],
        ["CADEIA_LITERAL"],
        ["BOOLEANO"],
        ["LPAREN", "EXPRESSAO", "RPAREN"],
        ["CHAMADA_TERM"]
    ],
}

# === FIRST ===
def first(simbolo, gramatica, visitados=None):
    if visitados is None:
        visitados = set()

    if simbolo not in gramatica:
        return {simbolo}

    if simbolo in visitados:
        return set()

    visitados.add(simbolo)
    conjPrimeiro = set()

    for producao in gramatica[simbolo]:
        encontrou_vazio = True

        for atual in producao:
            conjunto_primeiro = first(atual, gramatica, visitados.copy())
            conjPrimeiro |= (conjunto_primeiro - {"ε"})
            if "ε" not in conjunto_primeiro:
                encontrou_vazio = False
                break
        if encontrou_vazio:
            conjPrimeiro.add("ε")

    return conjPrimeiro


# === FOLLOW ===
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
