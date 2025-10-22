from grammar import grammar, first, follow

class AnalisadorSintaticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.analiseTabela = self.construir_tabela_ll1()  # corrigido o nome


    def construir_tabela_ll1(self):
        tabela = {}

        for cabeca, producoes in self.gramatica.items():
            for producao in producoes:
                # calcula FIRST de toda a produção
                conjPrimeiro = set()
                encontrou_vazio = True

                for simbolo in producao:
                    primeiros = first(simbolo, self.gramatica)
                    conjPrimeiro |= (primeiros - {"ε"})
                    if "ε" not in primeiros:
                        encontrou_vazio = False
                        break
                if encontrou_vazio:
                    conjPrimeiro.add("ε")

                # adiciona as regras à tabela LL(1)
                for simbolo in conjPrimeiro - {"ε"}:
                    tabela[(cabeca, simbolo)] = producao
                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica):
                        tabela[(cabeca, simbolo)] = producao

        return tabela

    # === ANÁLISE SINTÁTICA ===
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

        print("\n Análise sintática concluída com sucesso!")
