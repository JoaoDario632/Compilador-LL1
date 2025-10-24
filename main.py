# main.py
from scanner import analisador_lexico 
from ll1_parser import AnalisadorSintaticoLL1
from grammar import grammar, first, follow

if __name__ == "__main__":
    # Lê o código fonte do arquivo "app.br"
    with open("app.br", "r", encoding="utf-8") as f:
        codigo = f.read()

    print("\n=== ANÁLISE LÉXICA ===")
    # Executa o analisador léxico para gerar a lista de tokens
    tokens = analisador_lexico(codigo) 
    for t in tokens:
        print(t)

    print("\n=== TESTE FIRST(PROGRAMA) ===")
    # Testa a função FIRST para o símbolo inicial "PROGRAMA"
    print("FIRST(PROGRAMA):", first("PROGRAMA", grammar))

    print("\n=== ANÁLISE SINTÁTICA ===")
    # Cria um analisador sintático LL(1) e analisa os tokens gerados
    parser = AnalisadorSintaticoLL1(grammar)
    parser.analisar(tokens)
