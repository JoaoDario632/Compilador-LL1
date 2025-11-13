from tabulate import tabulate
def exibicao(tokens):
    tabela = []

    for token in tokens:
        tipo = token[0]
        lexema = token[1] if len(token) > 1 and token[1] is not None else ""
        tabela.append([tipo, lexema])

    print("\n=== TABELA DE TOKENS RECONHECIDOS ===\n")
    print(tabulate(
        tabela,
        headers=["Tipo de Token", "Lexema"],
        tablefmt="fancy_grid"
    ))
def GramaticaConvertida(G):
    print("\n=== GRAMÁTICA CONVERTIDA PARA LR(0) ===\n")

    linhas = []
    for nt, producoes in G.items():
        bloco = "\n".join(f"• {' '.join(p) if p else 'ε'}" for p in producoes)
        linhas.append([nt, bloco])

    print(tabulate(
        linhas,
        headers=["Não-terminal", "Produções"],
        tablefmt="fancy_grid",
        maxcolwidths=[20, 80]
    ))
def ReducaoFinal(passos, ultimos=25):

    print("\n=== TABELA DE REDUÇÃO — ÚLTIMOS PASSOS ===\n")

    final = passos[-ultimos:] if len(passos) > ultimos else passos
    linhas = []

    def corta(txt, tam=35):
        txt = str(txt)
        return txt if len(txt) <= tam else txt[:tam] + "..."

    for (num, pilha_est, pilha_simb, entrada, acao) in final:
        linhas.append([
            num,
            corta(pilha_est, 30),
            corta(pilha_simb, 30),
            entrada,
            corta(acao, 40)
        ])

    print(tabulate(
        linhas,
        headers=["Passo", "Pilha Estados", "Pilha Símbolos", "Entrada", "Ação"],
        tablefmt="fancy_grid",
        maxcolwidths=[7, 30, 30, 10, 40],
        stralign="center"
    ))
