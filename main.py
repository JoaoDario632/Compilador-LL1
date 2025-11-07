from scanner import analisador_lexico
from ll1_parser import AnalisadorSintaticoLL1
from grammar import grammar, first, follow
from tabela import exibicao  
from tabulate import tabulate
from slr_parser import analisar_slr

def execucaoAnalisador(caminho_arquivo: str):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("\n=== ETAPA 1: ANÁLISE LÉXICA ===")
    tokens = analisador_lexico(codigo)

    exibicao(tokens)
    print("=== ETAPA 2: FIRST & FOLLOW ===")
    print("FIRST(DECL_FUNCOES_G):", first("DECL_FUNCOES_G", grammar))
    print("FOLLOW(DECL_FUNCOES_G):", follow("DECL_FUNCOES_G", grammar, "PROGRAMA_G"))

    print("\n=== ETAPA 3: ANÁLISE SINTÁTICA ===")
    parser = AnalisadorSintaticoLL1(grammar)
    parser.analisar(tokens)

    print("\n=== ETAPA 4: ANÁLISE SINTÁTICA SLR(1) ===")
    analisar_slr(tokens, grammar)
if __name__ == "__main__":
    execucaoAnalisador("app.br")
