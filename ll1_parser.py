from grammar import grammar, first, follow
from scanner import scanner

class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.tabela = self.build_table()

    def build_table(self):
        tabela = {}
        for head, bodies in self.grammar.items():
            for body in bodies:
                for term in first(body[0], self.grammar):
                    if term != "ε":
                        tabela[(head, term)] = body
                if "ε" in first(body[0], self.grammar):
                    for f in follow(head, self.grammar):
                        tabela[(head, f)] = body
        return tabela

    def parse(self, tokens):
        stack = ["EOF", "PROGRAMA"]
        pos = 0
        token = tokens[pos][0]

        while stack:
            top = stack.pop()
            if top == token:
                pos += 1
                token = tokens[pos][0]
            elif top in self.grammar:
                rule = self.tabela.get((top, token))
                if not rule:
                    raise SyntaxError(f"Erro de sintaxe: esperado {top}, encontrado {token}")
                for sym in reversed(rule):
                    if sym != "ε":
                        stack.append(sym)
            elif top == "ε":
                continue
            else:
                raise SyntaxError(f"Erro inesperado: {token}")

        print("\nAnálise sintática concluída com sucesso.")
