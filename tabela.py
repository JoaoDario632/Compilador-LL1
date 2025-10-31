from tabulate import tabulate

def exibicao(tokens):

    tabela = []
    for token in tokens:
        tipo = token[0] 
        if len(token) > 1:
            lexema = token[1] if token[1] is not None else ""
        else:
            lexema = ""

        tabela.append([tipo, lexema])

    # Exibe um título antes da tabela
    print("\n=== TABELA DE TOKENS RECONHECIDOS ===\n")
    print(tabulate(tabela, headers=["Tipo de Token", "Lexema"], tablefmt="fancy_grid"))
