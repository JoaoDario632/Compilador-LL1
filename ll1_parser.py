from grammar import grammar, first, follow

class AnalisadorSintaticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.analiseTabela = self.Tabela()

    def Tabela(self):
        tabela = {}

        for cabeca, corpos in self.gramatica.items():
            for corpo in corpos:
                conjPrimeiro = set()

                for simbolo in corpo:
                    primeiros = first(simbolo, self.gramatica)
                    conjPrimeiro |= (primeiros - {"ε"})
                    if "ε" not in primeiros:
                        break
                else:
                    conjPrimeiro.add("ε")

                for terminal in conjPrimeiro:
                    if terminal != "ε":
                        tabela[(cabeca, terminal)] = corpo

                if "ε" in conjPrimeiro:
                    for f in follow(cabeca, self.gramatica):
                        tabela[(cabeca, f)] = corpo

        return tabela

    def analisar(self, tokens):
        pilha = ["EOF", "PROGRAMA"]
        posicao = 0
        ttoken = tokens[posicao][0]

        while pilha:
            topo = pilha.pop()

            if topo == ttoken:
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
            elif topo in self.gramatica:
                regra = self.analiseTabela.get((topo, ttoken))

                if not regra:
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    raise SyntaxError(
                        f"Erro de sintaxe: esperado um de {esperados}, mas foi encontrado {ttoken}"
                    )

                for simbolo in reversed(regra):
                    if simbolo != "ε":
                        pilha.append(simbolo)

            elif topo == "ε":
                continue
            else:
                raise SyntaxError(f"Erro inesperado: {ttoken}")

        print("\nAnálise sintática concluída com sucesso")

def primeiro(simbolo, gramatica, visitados=None):
    if visitados is None:
        visitados = set()

    if simbolo not in gramatica:
        return {simbolo}

    if simbolo in visitados:
        return set()

    visitados.add(simbolo)
    conjPrimeiro = set()

    for regra in gramatica[simbolo]:
        for SImboloRegra in regra:
            primeiros = primeiro(SImboloRegra, gramatica, visitados.copy())
            conjPrimeiro |= (primeiros - {"ε"})
            if "ε" not in primeiros:
                break
        else:
            conjPrimeiro.add("ε")

    return conjPrimeiro
