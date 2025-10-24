#ll1_parser.py
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
                if chave in tabela:
                    print(f"[⚠️ Aviso] Conflito LL(1): {cabeca} com {simbolo}")
                tabela[chave] = producao

            if "ε" in conjPrimeiro:
                for simbolo in follow(cabeca, self.gramatica):
                    chave = (cabeca, simbolo)
                    if chave in tabela:
                        print(f"[⚠️ Aviso] Conflito LL(1): {cabeca} com {simbolo}")
                    tabela[chave] = producao

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
                continue


            elif topo in self.gramatica:
                regra = self.analiseTabela.get((topo, ttoken)) #Analisar aqui

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
            elif topo == ttoken:
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
            else:
                raise SyntaxError(f"Erro inesperado: {ttoken} (esperava {topo})")
        print("\n Análise sintática concluída com sucesso!")