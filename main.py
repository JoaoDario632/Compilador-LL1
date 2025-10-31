# main_analisador.py
from scanner import analisador_lexico
from ll1_parser import AnalisadorSintaticoLL1
from grammar import grammar, first, follow
from tabela import exibicao  
from tabulate import tabulate
import time


def execucaoAnalisador(caminho_arquivo: str):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("\n=== ETAPA 1: ANÁLISE LÉXICA ===")
    inicio_lex = time.perf_counter()
    tokens = analisador_lexico(codigo)
    fim_lex = time.perf_counter()
    duracao_lex = fim_lex - inicio_lex

    exibicao(tokens)
    print(f"\nTempo de análise léxica: {duracao_lex:.6f} segundos\n")

    print("=== ETAPA 2: FIRST & FOLLOW ===")
    print("FIRST(PROGRAMA):", first("PROGRAMA", grammar))
    print("FOLLOW(PROGRAMA):", follow("PROGRAMA", grammar))

    print("\n=== ETAPA 3: ANÁLISE SINTÁTICA ===")
    parser = AnalisadorSintaticoLL1(grammar)
    inicio_sint = time.perf_counter()
    parser.analisar(tokens)
    fim_sint = time.perf_counter()

    print(f"\n Tempo de análise sintática: {fim_sint - inicio_sint:.6f} segundos\n")


if __name__ == "__main__":
    execucaoAnalisador("app.br")
