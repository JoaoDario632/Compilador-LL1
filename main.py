from scanner import scanner
from ll1_parser import LL1Parser
from grammar import grammar

if __name__ == "__main__":
    with open("app.br", "r", encoding="utf-8") as f:
        codigo = f.read()

    print("\n=== ANÁLISE LÉXICA ===")
    tokens = scanner(codigo)
    for t in tokens:
        print(t)

    print("\n=== ANÁLISE SINTÁTICA ===")
    parser = LL1Parser(grammar)
    parser.parse(tokens)
