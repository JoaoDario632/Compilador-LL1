grammar = {
    "PROGRAMA": [["FUNCAO_PRINCIPAL"]],
    "FUNCAO_PRINCIPAL": [["FUNCAO", "PRINCIPAL", "LPAREN", "RPAREN", "BLOCO"]],
    "BLOCO": [["LCHAVE", "DECLS_OPC", "COMANDOS", "RCHAVE"]],
    "DECLS_OPC": [["DECLARACAO", "DECLS_OPC"], ["ε"]],
    "COMANDOS": [["COMANDO", "COMANDOS"], ["ε"]],
    "COMANDO": [["SE_INST"], ["ENQUANTO_INST"], ["PARA_INST"], ["RETORNO_INST"], ["ATRIB_INST"]],
    "DECLARACAO": [["TIPO_VAR", "IDENT", "PONTOVIRG"]],
    "ATRIB_INST": [["IDENT", "ATRIB", "EXPRESSAO", "PONTOVIRG"]],
    "RETORNO_INST": [["RETORNO", "EXPRESSAO", "PONTOVIRG"]],
    "SE_INST": [["SE", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO", "SENAO_PARTE"]],
    "SENAO_PARTE": [["SENAO", "BLOCO"], ["ε"]],
    "ENQUANTO_INST": [["ENQUANTO", "LPAREN", "EXPRESSAO", "RPAREN", "BLOCO"]],
    "PARA_INST": [["PARA", "LPAREN", "ATRIB_INST", "EXPRESSAO", "PONTOVIRG", "ATRIB_INST", "RPAREN", "BLOCO"]],

    # EXPRESSÕES
    "EXPRESSAO": [["EXP_LOG"]],
    "EXP_LOG": [["EXP_COMPARACAO", "EXP_LOG_OPC"]],
    "EXP_LOG_OPC": [["OPER_LOGI", "EXP_COMPARACAO", "EXP_LOG_OPC"], ["ε"]],
    "EXP_COMPARACAO": [["EXP_ARIT", "EXP_COMPARACAO_OPC"]],
    "EXP_COMPARACAO_OPC": [["COMPAR", "EXP_ARIT", "EXP_COMPARACAO_OPC"], ["ε"]],
    "EXP_ARIT": [["TERMO", "EXP_ARIT_OPC"]],
    "EXP_ARIT_OPC": [["OPER_ARIT", "TERMO", "EXP_ARIT_OPC"], ["ε"]],

   
    "TERMO": [["IDENT", "TERMO_CHAMADA_OPC"], ["NUMERO_INT"], ["NUMERO_REAL"], ["CADEIA_LITERAL"], ["BOOLEANO"], ["LPAREN", "EXPRESSAO", "RPAREN"]],
    "TERMO_CHAMADA_OPC": [["LPAREN", "PARAMS_OPC", "RPAREN"], ["ε"]],
    "PARAMS_OPC": [["PARAMS"], ["ε"]],
    "PARAMS": [["EXPRESSAO", "PARAMS_CONT"]],
    "PARAMS_CONT": [["VIRGULA", "EXPRESSAO", "PARAMS_CONT"], ["ε"]],
}


def first(simbolo, gramatica, visitados=None):
    if visitados is None:
        visitados = set()

    # Lista de todos os terminais conhecidos
    terminais = {
        "FUNCAO", "PRINCIPAL", "TIPO_VAR", "SE", "SENAO", "ENQUANTO", "FACA", "PARA",
        "RETORNO", "BOOLEANO", "NUMERO_INT", "NUMERO_REAL", "CARACTERE", "CADEIA_LITERAL",
        "PALAVRA", "IDENT", "COMPAR", "OPER_ARIT", "OPER_LOGI", "ATRIB",
        "LPAREN", "RPAREN", "LCHAVE", "RCHAVE", "VIRGULA", "PONTOVIRG", "EOF"
    }

    # Se o símbolo é terminal → o FIRST é ele mesmo
    if simbolo in terminais or simbolo not in gramatica:
        return {simbolo}

    # Evita recursão infinita
    if simbolo in visitados:
        return set()

    visitados.add(simbolo)
    conjPrimeiro = set()

    for producao in gramatica[simbolo]:
        encontrou_vazio = True

        for atual in producao:
            primeiros_atual = first(atual, gramatica, visitados.copy())
            conjPrimeiro |= (primeiros_atual - {"ε"})
            if "ε" not in primeiros_atual:
                encontrou_vazio = False
                break
        if encontrou_vazio:
            conjPrimeiro.add("ε")

    return conjPrimeiro

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
