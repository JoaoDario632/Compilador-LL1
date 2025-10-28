from scanner import analisador_lexico       
from ll1_parser import AnalisadorSintaticoLL1  
from grammar import grammar, first, follow   

if __name__ == "__main__":
    with open("app.br", "r", encoding="utf-8") as f:
        codigo = f.read()

    # === ANÁLISE LÉXICA ===
    print("\n=== ANÁLISE LÉXICA ===")
    tokens = analisador_lexico(codigo) 
    for t in tokens:
        print(t)

    # Mostra o conjunto FIRST do símbolo inicial "PROGRAMA"
    print("\n=== TESTE FIRST(PROGRAMA) ===")
    print("FIRST(PROGRAMA):", first("PROGRAMA", grammar))

    # === ANÁLISE SINTÁTICA ===
    print("\n=== ANÁLISE SINTÁTICA ===")
    parser = AnalisadorSintaticoLL1(grammar)  
    parser.analisar(tokens)                  
