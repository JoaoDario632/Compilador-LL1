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
            for s in conjunto_primeiro:
                if s != "ε":
                    conjPrimeiro.add(s)
            if "ε" not in conjunto_primeiro:
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
                        viznhosProx = first(prox, gramatica)
                        for s in viznhosProx:
                            if s != "ε":
                                segundo.add(s)
                        if "ε" in viznhosProx:
                            segundo |= follow(cabeca, gramatica)
                    else:
                        if cabeca != simbolo:
                            segundo |= follow(cabeca, gramatica)
    return segundo