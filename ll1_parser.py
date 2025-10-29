from grammar import grammar, first, follow

class AnalisadorSintaticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.analiseTabela = self.construir_tabela_ll1()

    def construir_tabela_ll1(self):
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
                    chave = (cabeca, simbolo)
                    tabela[chave] = producao

                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica):
                        tabela[(cabeca, simbolo)] = producao

        return tabela

    def analisar(self, tokens):
        pilha = ["eof", "PROGRAMA"]
        posicao = 0
        ttoken = tokens[posicao][0]

        print("\n=== ANÁLISE SINTÁTICA ===")

        while pilha:
            topo = pilha.pop()

            # Caso 1: topo == token
            if topo == ttoken:
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                continue

            # Caso 2: topo é não-terminal
            elif topo in self.gramatica:
                regra = self.analiseTabela.get((topo, ttoken))

                if not regra:
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    print(f"[ERRO] Esperado um de {esperados}, mas encontrado '{ttoken}'.")
                    print("→ Recuperando em modo pânico...")

                    # 🔁 Recuperação em modo pânico
                    follow_topo = follow(topo, self.gramatica)
                    while ttoken not in follow_topo and ttoken != "eof":
                        posicao += 1
                        if posicao < len(tokens):
                            ttoken = tokens[posicao][0]
                        else:
                            break
                    continue  # tenta continuar análise

                for simbolo in reversed(regra):
                    if simbolo != "ε":
                        pilha.append(simbolo)

            elif topo == "ε":
                continue

            else:
                print(f"[ERRO] Token inesperado '{ttoken}', esperado '{topo}'.")
                print("→ Ignorando token e tentando sincronizar...")
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                else:
                    break

        print("\n Análise sintática concluída (modo pânico ativo).")
