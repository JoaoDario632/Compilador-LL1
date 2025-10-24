# ll1_parser.py
from grammar import grammar, first, follow

class AnalisadorSintaticoLL1:
    """Classe para análise sintática LL(1)"""

    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.analiseTabela = self.construir_tabela_ll1()  # Constroi tabela LL(1)

    def construir_tabela_ll1(self):
        """Constroi a tabela de análise LL(1) a partir da gramática"""
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

                # Preenche tabela para cada terminal do FIRST
                for simbolo in conjPrimeiro - {"ε"}:
                    chave = (cabeca, simbolo)
                    if chave in tabela:
                        print(f"[⚠️ Aviso] Conflito LL(1): {cabeca} com {simbolo}")
                    tabela[chave] = producao

                # Preenche tabela para cada terminal do FOLLOW caso FIRST contenha ε
                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica):
                        chave = (cabeca, simbolo)
                        if chave in tabela:
                            print(f"[⚠️ Aviso] Conflito LL(1): {cabeca} com {simbolo}")
                        tabela[chave] = producao

        return tabela

    def analisar(self, tokens):
        """Realiza a análise sintática LL(1) usando a tabela construída"""
        pilha = ["EOF", "PROGRAMA"]
        posicao = 0
        ttoken = tokens[posicao][0]

        while pilha:
            topo = pilha.pop()

            if topo == ttoken:
                # Consome o token se for terminal
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                continue

            elif topo in self.gramatica:
                # Verifica a produção na tabela LL(1)
                regra = self.analiseTabela.get((topo, ttoken))

                if not regra:
                    # Se não encontrou produção, levanta erro de sintaxe
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    raise SyntaxError(
                        f"Erro de sintaxe: esperado um de {esperados}, mas foi encontrado {ttoken}"
                    )

                # Coloca os símbolos da produção na pilha (inversamente)
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
        print("\nAnálise sintática concluída com sucesso!")
