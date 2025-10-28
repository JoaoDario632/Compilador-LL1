# Implementa o analisador sintático preditivo LL(1)
# usando tabela de análise gerada a partir de FIRST e FOLLOW.

from grammar import grammar, first, follow

class AnalisadorSintaticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.analiseTabela = self.construir_tabela_ll1()  # Gera a tabela LL(1)

    # ===================== CONSTRUÇÃO DA TABELA LL(1) =====================
    def construir_tabela_ll1(self):
        """
        Constrói a tabela de análise LL(1):
        M[A, a] = α, onde A → α é uma produção e 'a' ∈ FIRST(α)
        ou, se ε ∈ FIRST(α), 'a' ∈ FOLLOW(A)
        """
        tabela = {}

        for cabeca, producoes in self.gramatica.items():
            for producao in producoes:
                conjPrimeiro = set()
                encontrou_vazio = True

                # Calcula FIRST da produção inteira
                for simbolo in producao:
                    primeiros = first(simbolo, self.gramatica)
                    conjPrimeiro |= (primeiros - {"ε"})
                    if "ε" not in primeiros:
                        encontrou_vazio = False
                        break
                if encontrou_vazio:
                    conjPrimeiro.add("ε")

                # Preenche tabela com os símbolos terminais de FIRST
                for simbolo in conjPrimeiro - {"ε"}:
                    chave = (cabeca, simbolo)
                    if chave in tabela:
                        print(f"[Aviso] Conflito LL(1): {cabeca} com {simbolo}")
                    tabela[chave] = producao

                # Caso a produção gere ε, usa FOLLOW(cabeca)
                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica):
                        chave = (cabeca, simbolo)
                        if chave in tabela:
                            print(f"[Aviso] Conflito LL(1): {cabeca} com {simbolo}")
                        tabela[chave] = producao

        return tabela


    # ===================== ANÁLISE SINTÁTICA =====================
    def analisar(self, tokens):
        """
        Executa o algoritmo do analisador LL(1) usando pilha.
        """
        pilha = ["EOF", "PROGRAMA"]  # Pilha inicial (símbolo inicial + EOF)
        posicao = 0
        ttoken = tokens[posicao][0]  # Primeiro token (tipo do token)

        # Percorre até a pilha ficar vazia
        while pilha:
            topo = pilha.pop()

            # Caso 1: topo == token → consome token
            if topo == ttoken:
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                continue

            # Caso 2: topo é um não-terminal → aplica regra da tabela LL(1)
            elif topo in self.gramatica:
                regra = self.analiseTabela.get((topo, ttoken))  # Busca regra na tabela

                # Se não existir regra válida → erro sintático
                if not regra:
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    raise SyntaxError(
                        f"Erro de sintaxe: esperado um de {esperados}, mas foi encontrado {ttoken}"
                    )

                # Empilha a produção ao contrário (pois a pilha é LIFO)
                for simbolo in reversed(regra):
                    if simbolo != "ε":
                        pilha.append(simbolo)

            # Caso 3: ignora epsilon
            elif topo == "ε":
                continue

            # Caso 4: erro — token inesperado
            else:
                raise SyntaxError(f"Erro inesperado: {ttoken} (esperava {topo})")

        print("\nAnálise sintática concluída com sucesso!")
