# ========================= grammar.py =========================
# Define a gramática LL(1), e as funções para calcular os conjuntos FIRST e FOLLOW.

grammar = {
    # ======= PROGRAMA =======
    "PROGRAMA": [["DECL_FUNCOES", "FUNCAO_PRINCIPAL"]],

    # ======= FUNÇÕES =======
    "DECL_FUNCOES": [["FUNCAO_DEF", "DECL_FUNCOES"], ["ε"]],
    "FUNCAO_DEF": [["FUNCAO", "TIPO_VAR", "IDENT", "LPAREN", "PARAMS_OPC", "RPAREN", "BLOCO"]],
    "FUNCAO_PRINCIPAL": [["PRINCIPAL", "BLOCO"]],

    # ======= BLOCOS =======
    "BLOCO": [["LCHAVE", "DECLS_OPC", "COMANDOS", "RCHAVE"]],
    "DECLS_OPC": [["DECLARACAO", "DECLS_OPC"], ["ε"]],
    "COMANDOS": [["COMANDO", "COMANDOS"], ["ε"]],

    # ======= COMANDOS =======
    "COMANDO": [
        ["SE_INST"],
        ["ENQUANTO_INST"],
        ["PARA_INST"],
        ["RETORNO_INST"],
        ["ATRIB_INST"]
    ],

    # ======= DECLARAÇÕES =======
    "DECLARACAO": [["TIPO_VAR", "IDENT", "DECL_INICIAL_OPC", "PONTOVIRG"]],
    "DECL_INICIAL_OPC": [["ATRIB", "EXPRESSAO"], ["ε"]],

    # ======= ATRIBUIÇÕES =======
    "ATRIB_INST": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],
    "RETORNO_INST": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],

    # ======= ESTRUTURAS DE CONTROLE =======
    "SE_INST": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_PARTE"]],
    "SENAO_PARTE": [["SENAO", "BLOCO"], ["ε"]],
    "ENQUANTO_INST": [["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"]],
    "PARA_INST": [["PARA", "LPAREN", "ATRIB_INST", "EXPRESSAO", "PONTOVIRG", "ATRIB_INST", "RPAREN", "BLOCO"]],

    # ======= EXPRESSÕES =======
    "EXPRESSAO": [["EXP_LOG"]],
    "EXP_LOG": [["EXP_COMPARACAO", "EXP_LOG'"]],
    "EXP_LOG'": [["OPER_LOGI", "EXP_COMPARACAO", "EXP_LOG'"], ["ε"]],

    "EXP_COMPARACAO": [["EXP_ARIT", "EXP_COMPARACAO'"]],
    "EXP_COMPARACAO'": [["COMPAR", "EXP_ARIT", "EXP_COMPARACAO'"], ["ε"]],

    "EXP_ARIT": [["TERMO", "EXP_ARIT'"]],
    "EXP_ARIT'": [["OPER_ARIT", "TERMO", "EXP_ARIT'"], ["ε"]],

    # ======= TERMOS E PARÂMETROS =======
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
    """
    Calcula o conjunto FIRST de um símbolo.
    FIRST(X) = conjunto de tokens que podem iniciar derivações a partir de X.
    """
    if visitados is None:
        visitados = set()

    # Conjunto de todos os terminais conhecidos
    terminais = {
        "FUNCAO", "PRINCIPAL", "TIPO_VAR", "SE", "SENAO", "ENQUANTO", "FACA", "PARA",
        "RETORNO", "BOOLEANO", "NUMERO_INT", "NUMERO_REAL", "CARACTERE", "CADEIA_LITERAL",
        "PALAVRA", "IDENT", "COMPAR", "OPER_ARIT", "OPER_LOGI", "ATRIB",
        "LPAREN", "RPAREN", "LCHAVE", "RCHAVE", "VIRGULA", "PONTOVIRG", "EOF"
    }

    # Caso base: se for terminal, retorna ele mesmo
    if simbolo in terminais or simbolo not in gramatica:
        return {simbolo}

    # Evita recursão infinita
    if simbolo in visitados:
        return set()

    visitados.add(simbolo)
    conj = set()

    # Percorre cada produção de X → α
    for producao in gramatica[simbolo]:
        vazio = True
        for s in producao:
            primeiros = first(s, gramatica, visitados.copy())  # Calcula FIRST(s)
            conj |= (primeiros - {"ε"})                        # Adiciona todos exceto ε
            if "ε" not in primeiros:                           # Se não produz ε, interrompe
                vazio = False
                break
        if vazio:
            conj.add("ε")                                      # Se todas produzem ε, adiciona ε
    return conj


# ======= FOLLOW =======
def follow(simbolo, gramatica, inicio="PROGRAMA"):
    """
    Calcula o conjunto FOLLOW de um símbolo não-terminal.
    FOLLOW(A) = conjunto de tokens que podem aparecer imediatamente após A.
    """
    segundo = set()

    # Símbolo inicial sempre contém EOF no FOLLOW
    if simbolo == inicio:
        segundo.add("EOF")

    # Percorre todas as produções da gramática
    for cabeca, producoes in gramatica.items():
        for producao in producoes:
            for i in range(len(producao)):
                if producao[i] == simbolo:
                    # Caso: A → αBβ
                    if i + 1 < len(producao):
                        prox = producao[i + 1]
                        vizinhos = first(prox, gramatica)
                        segundo |= (vizinhos - {"ε"})
                        # Se β ⇒ ε, adiciona FOLLOW(A)
                        if "ε" in vizinhos:
                            segundo |= follow(cabeca, gramatica)
                    # Caso: A → αB
                    else:
                        if cabeca != simbolo:
                            segundo |= follow(cabeca, gramatica)
    return segundo
