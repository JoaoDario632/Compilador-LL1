# ll1_parser.py
from grammar import grammar, first, follow
from tabulate import tabulate

class AnalisadorSintaticoLL1:

    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.simbolo_inicial = "PROGRAMA_G"
        self.analiseTabela = self.TabelaLL1()

    def TabelaLL1(self):
        tabela = {}

        for cabeca, producoes in self.gramatica.items():
            for producao in producoes:
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

                for simbolo in conjPrimeiro - {"ε"}:
                    tabela[(cabeca, simbolo)] = producao

                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica, self.simbolo_inicial):
                        tabela[(cabeca, simbolo)] = producao

        return tabela

    def analisar(self, tokens):

        passos = []       
        Contador = 1      

        pilha = ["EOF", self.simbolo_inicial]
        pos = 0
        ttoken = tokens[pos][0]

        while pilha:
            topo = pilha.pop()
            entrada_atual = ttoken
            pilha_visivel = " ".join(pilha[::-1])
            acao = ""

            if topo == ttoken:
                acao = f"casar '{ttoken}'"
                passos.append([Contador, pilha_visivel, entrada_atual, acao])

                pos += 1
                if pos < len(tokens):
                    ttoken = tokens[pos][0]

                Contador += 1
                continue

            # CASO 2 — topo é não-terminal
            elif topo in self.gramatica:
                regra = self.analiseTabela.get((topo, ttoken))

                if not regra:
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    acao = f"ERRO – esperado {esperados}, encontrado '{ttoken}'"
                    passos.append([Contador, pilha_visivel, entrada_atual, acao])

                    # modo pânico:
                    follow_topo = follow(topo, self.gramatica, self.simbolo_inicial)
                    while ttoken not in follow_topo and ttoken != "EOF":
                        pos += 1
                        if pos < len(tokens):
                            ttoken = tokens[pos][0]
                        else:
                            break

                    Contador += 1
                    continue

                acao = f"expandir {topo} → {' '.join(regra) if regra else 'ε'}"
                passos.append([Contador, pilha_visivel, entrada_atual, acao])

                for simbolo in reversed(regra):
                    if simbolo != "ε":
                        pilha.append(simbolo)

                Contador += 1
                continue

            # CASO 3 — ε
            elif topo == "ε":
                acao = "produz ε"
                passos.append([Contador, pilha_visivel, entrada_atual, acao])
                Contador += 1
                continue

            # CASO 4 — erro terminal inesperado
            else:
                acao = f"ERRO – encontrado '{ttoken}', esperado '{topo}'"
                passos.append([Contador, pilha_visivel, entrada_atual, acao])

                pos += 1
                if pos < len(tokens):
                    ttoken = tokens[pos][0]
                else:
                    break

                Contador += 1
                continue
        estadosFinais = passos[-10:] if len(passos) > 10 else passos

        print("\n=== TABELA DO PROCESSO DA ANÁLISE LL(1) — ÚLTIMOS 10 PASSOS ===\n")
        print(tabulate(
            estadosFinais,
            headers=["Passo", "Pilha", "Entrada", "Ação"],
            tablefmt="fancy_grid",
            maxcolwidths=[6, 40, 12, 50]
        ))

        print("\nAnálise sintática concluída (modo pânico ativo).")
