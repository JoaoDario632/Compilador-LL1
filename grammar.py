# grammar.py

grammar = {
    # ======= PROGRAMA =======
    "PROGRAMA": [["DECL_FUNCOES", "FUNCAO_PRINCIPAL"]],

    # Declarações de funções antes do principal
    "DECL_FUNCOES": [["FUNCAO_DEF", "DECL_FUNCOES"], ["ε"]],

    # Definição de função
    "FUNCAO_DEF": [["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS_OPC", "RPAREN", "BLOCO"]],

    # Função principal
    "FUNCAO_PRINCIPAL": [["PRINCIPAL", "BLOCO"]],

    # ======= BLOCOS =======
    "BLOCO": [["LCHAVE", "BLOCO_INTERNO", "RCHAVE"]],

    # Dentro do bloco, aceita declarações de variáveis + comandos
    "BLOCO_INTERNO": [["DECL_VAR_BLOCO", "COMANDOS"], ["COMANDOS"]],

    # Declarações de variáveis dentro de blocos
    "DECL_VAR_BLOCO": [["DECLARACAO", "DECL_VAR_BLOCO"], ["ε"]],

    "COMANDOS": [["COMANDO", "COMANDOS"], ["ε"]],

    # ======= COMANDOS =======
    "COMANDO": [
        ["SE_INST"],
        ["ENQUANTO_INST"],
        ["PARA_INST"],
        ["RETORNO_INST"],
        ["ATRIB_INST"],
        ["CHAMADA_FUNCAO"]
    ],

    # ======= DECLARAÇÃO =======
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECL_INICIAL_OPC", "PONTOVIRG"]],
    "DECL_INICIAL_OPC": [["ATRIB", "EXPRESSAO"], ["ε"]],

    # ======= ATRIBUIÇÕES =======
    "ATRIB_INST": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],
    "RETORNO_INST": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # ======= CHAMADA DE FUNÇÃO COMO COMANDO =======
    "CHAMADA_FUNCAO": [["IDENT", "LPAREN", "PARAMS_OPC", "RPAREN", "PONTOVIRG"]],

    # ======= ESTRUTURAS DE CONTROLE =======
    "SE_INST": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_PARTE"]],
    "SENAO_PARTE": [["SENAO", "BLOCO"], ["ε"]],
    "ENQUANTO_INST": [["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"]],
    "PARA_INST": [["PARA", "LPAREN", "ATRIB_INST", "EXPRESSAO", "PONTOVIRG", "ATRIB_INST", "RPAREN", "BLOCO"]],

    # ======= EXPRESSÕES =======
    "EXPRESSAO": [["EXP_LOG"]],
    "EXP_LOG": [["EXP_COMPARACAO", "EXP_LOG_OPC"]],
    "EXP_LOG_OPC": [["OPER_LOGI", "EXP_COMPARACAO", "EXP_LOG_OPC"], ["ε"]],
    "EXP_COMPARACAO": [["EXP_ARIT", "EXP_COMPARACAO_OPC"]],
    "EXP_COMPARACAO_OPC": [["COMPAR", "EXP_ARIT", "EXP_COMPARACAO_OPC"], ["ε"]],
    "EXP_ARIT": [["TERMO", "EXP_ARIT_OPC"]],
    "EXP_ARIT_OPC": [["OPER_ARIT", "TERMO", "EXP_ARIT_OPC"], ["ε"]],

    # ======= TERMOS =======
    "TERMO": [
        ["IDENT", "TERMO_CHAMADA_OPC"],
        ["NUMERO_INT"],
        ["NUMERO_REAL"],
        ["CADEIA_LITERAL"],
        ["BOOLEANO"],
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
        "RETORNO", "BOOLEANO", "NUMERO_INT", "NUMERO_REAL", "CARACTERE", "CADEIA_LITERAL",
        "PALAVRA", "IDENT", "COMPAR", "OPER_ARIT", "OPER_LOGI", "ATRIB",
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