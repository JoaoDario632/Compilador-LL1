from scanner import analisador_lexico
from ll1_parser import AnalisadorSintaticoLL1
from slr_parser import analisar_slr
from grammar import grammar, first, follow
from tabela import exibicao  
from pdf_exporter import gerar_pdf

def execucaoAnalisador(caminho_arquivo: str):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("\n=== ETAPA 1: ANÁLISE LÉXICA ===")
    tokens = analisador_lexico(codigo)
    exibicao(tokens)

    print("=== ETAPA 2: FIRST & FOLLOW ===")
    print("FIRST(PROGRAMA_G):", first("PROGRAMA_G", grammar))
    print("FOLLOW(PROGRAMA_G):", follow("PROGRAMA_G", grammar, "PROGRAMA_G"))

    print("\n=== ETAPA 3: ANÁLISE SINTÁTICA ===")
    parser = AnalisadorSintaticoLL1(grammar)
    passos_ll1 = parser.analisar(tokens)

    print("\n=== ETAPA 4: ANÁLISE SINTÁTICA SLR(1) ===")
    gram_convertida, passos_slr = analisar_slr(tokens, grammar)

    gerar_pdf(tokens, passos_ll1, passos_slr, gram_convertida)
if __name__ == "__main__":
    execucaoAnalisador("app.br")
