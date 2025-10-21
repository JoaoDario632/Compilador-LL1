from grammar import grammar, first, follow

class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.tabela = self.construcaoTabela()

    def primeiraSequencia(self, sequence):
        result = set()
        for sym in sequence:
            f = first(sym, self.grammar)
            result |= (f - {"ε"})
            if "ε" not in f:
                break
        else:
            result.add("ε")
        return result

    def construcaoTabela(self):
        tabela = {}
        for head, bodies in self.grammar.items():
            for body in bodies:
                first_set = self.primeiraSequencia(body)
                for term in first_set - {"ε"}:
                    tabela[(head, term)] = body
                if "ε" in first_set:
                    for term in follow(head, self.grammar):
                        tabela[(head, term)] = body
        return tabela

    def parse(self, tokens):
        stack = ["PROGRAMA", "EOF"]
        pos = 0
        token_type = tokens[pos][0]

        while stack:
            top = stack.pop()

            if top == "ε":
                continue

            # Terminal
            if top not in self.grammar:
                if top == token_type:
                    pos += 1
                    token_type = tokens[pos][0]
                else:
                    raise SyntaxError(f"Erro de sintaxe: esperado {top}, encontrado {token_type}")
                continue

            # Lookahead para instruções que começam com IDENT
            if top == "INSTRUCAO" and token_type == "IDENT":
                next_token_type = tokens[pos + 1][0]
                if next_token_type == "ATRIB":
                    production = ["ATRIBUICAO"]
                elif next_token_type == "LPAREN":
                    production = ["CHAMADA"]
                else:
                    raise SyntaxError(f"Erro inesperado após IDENT: {next_token_type}")
                for sym in reversed(production):
                    stack.append(sym)
                continue

            # Busca na tabela LL(1)
            key = (top, token_type)
            if key not in self.tabela:
                raise SyntaxError(f"Erro de sintaxe: esperado {top}, encontrado {token_type}")

            production = self.tabela[key]
            for sym in reversed(production):
                if sym != "ε":
                    stack.append(sym)

        print("\nAnálise sintática concluída com sucesso.")
