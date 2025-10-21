from grammar import grammar, first, follow

class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.tabela = self.build_table()

    def build_table(self):
        tabela = {}
        for head, bodies in self.grammar.items():
            for body in bodies:
                first_set = set()
                for sym in body:
                    f = first(sym, self.grammar)
                    first_set |= (f - {"ε"})
                    if "ε" not in f:
                        break
                else:
                    first_set.add("ε")

                for term in first_set:
                    if term != "ε":
                        tabela[(head, term)] = body

                if "ε" in first_set:
                    for f in follow(head, self.grammar):
                        tabela[(head, f)] = body
        return tabela

    def parse(self, tokens):
        stack = ["EOF", "PROGRAMA"]
        pos = 0
        token_type = tokens[pos][0]

        while stack:
            top = stack.pop()
            if top == token_type:
                pos += 1
                if pos < len(tokens):
                    token_type = tokens[pos][0]
            elif top in self.grammar:
                rule = self.tabela.get((top, token_type))
                if not rule:
                    expected = [k[1] for k in self.tabela if k[0] == top]
                    raise SyntaxError(f"Erro de sintaxe: esperado um de {expected}, encontrado {token_type}")
                for sym in reversed(rule):
                    if sym != "ε":
                        stack.append(sym)
            elif top == "ε":
                continue
            else:
                raise SyntaxError(f"Erro inesperado: {token_type}")

        print("\nAnálise sintática concluída com sucesso.")

def first(symbol, grammar, visitado=None):
    if visitado is None:
        visitado = set()
    if symbol not in grammar:
        return {symbol}  # terminal
    if symbol in visitado:
        return set()
    visitado.add(symbol)
    first_set = set()
    for rule in grammar[symbol]:
        for sym in rule:
            f = first(sym, grammar, visitado.copy())
            first_set |= (f - {"ε"})
            if "ε" not in f:
                break
        else:
            first_set.add("ε")
    return first_set
