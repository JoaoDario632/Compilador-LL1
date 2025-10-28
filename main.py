# Este arquivo orquestra o processo de análise léxica e sintática.
# Ele lê o código fonte ("app.br"), gera tokens e analisa sintaticamente.

from scanner import analisador_lexico           # Importa o analisador léxico (tokenizador)
from ll1_parser import AnalisadorSintaticoLL1   # Importa o analisador sintático LL(1)
from grammar import grammar, first, follow      # Importa a gramática e funções auxiliares

if __name__ == "__main__":
    # Lê o arquivo de código-fonte em português fictício "app.br"
    with open("app.br", "r", encoding="utf-8") as f:
        codigo = f.read()

    # === ANÁLISE LÉXICA ===
    print("\n=== ANÁLISE LÉXICA ===")
    tokens = analisador_lexico(codigo)  # Converte o código em uma lista de tokens (ex: [('IDENT','x'), ('ATRIB','=')...])
    for t in tokens:
        print(t)

    # Mostra o conjunto FIRST do símbolo inicial "PROGRAMA"
    print("\n=== TESTE FIRST(PROGRAMA) ===")
    print("FIRST(PROGRAMA):", first("PROGRAMA", grammar))

    # === ANÁLISE SINTÁTICA ===
    print("\n=== ANÁLISE SINTÁTICA ===")
    parser = AnalisadorSintaticoLL1(grammar)  # Cria o analisador sintático
    parser.analisar(tokens)                   # Executa a análise LL(1) dos tokens
