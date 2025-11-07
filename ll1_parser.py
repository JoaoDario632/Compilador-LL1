# Importa a gramática e as funções FIRST e FOLLOW
from grammar import grammar, first, follow

# ----------------------------------------------------
# Classe: AnalisadorSintaticoLL1
# Implementa um analisador sintático preditivo LL(1)
# ----------------------------------------------------
class AnalisadorSintaticoLL1:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        # Cria a tabela LL(1) automaticamente com base na gramática
        self.analiseTabela = self.construir_tabela_ll1()

    # Construção da Tabela LL(1)
    def construir_tabela_ll1(self):
        tabela = {}

        # Percorre todas as produções da gramática
        for cabeca, producoes in self.gramatica.items():
            for producao in producoes:
                conjPrimeiro = set()
                encontrou_vazio = True  # Indica se ε (vazio) é possível

                # Percorre cada símbolo da produção
                for simbolo in producao:
                    # Calcula o FIRST do símbolo
                    primeiros = first(simbolo, self.gramatica)
                    # Adiciona tudo que não é ε
                    conjPrimeiro |= (primeiros - {"ε"})

                    # Se o símbolo não gera ε, para o loop
                    if "ε" not in primeiros:
                        encontrou_vazio = False
                        break

                # Se todos os símbolos puderem gerar ε, adiciona ε ao conjunto
                if encontrou_vazio:
                    conjPrimeiro.add("ε")

                # Para cada terminal em FIRST(A → α), adiciona A→α na tabela
                for simbolo in conjPrimeiro - {"ε"}:
                    chave = (cabeca, simbolo)
                    tabela[chave] = producao

                # Se ε ∈ FIRST(A → α), adiciona regra também para FOLLOW(A)
                if "ε" in conjPrimeiro:
                    for simbolo in follow(cabeca, self.gramatica):
                        tabela[(cabeca, simbolo)] = producao

        return tabela

    # Função principal de análise sintática
    # Recebe uma lista de tokens do analisador léxico
    def analisar(self, tokens):
        # Inicializa a pilha com o símbolo inicial e EOF
        pilha = ["EOF", "PROGRAMA"]
        posicao = 0
        ttoken = tokens[posicao][0]  # tipo do token atual

        # Loop principal de análise
        while pilha:
            topo = pilha.pop()  # Lê o topo da pilha

            # Caso 1: o topo da pilha é igual ao token → consome o token
            if topo == ttoken:
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                continue

            # Caso 2: topo é um não-terminal → consulta a tabela LL(1)
            elif topo in self.gramatica:
                regra = self.analiseTabela.get((topo, ttoken))

                # Se não existe regra correspondente → erro sintático
                if not regra:
                    esperados = [k[1] for k in self.analiseTabela if k[0] == topo]
                    print(f"[ERRO] Esperado um de {esperados}, mas encontrado '{ttoken}'.")
                    print("→ Recuperando em modo pânico.")

                    # Recuperação de erro: ignora tokens até encontrar algo no FOLLOW
                    follow_topo = follow(topo, self.gramatica)
                    while ttoken not in follow_topo and ttoken != "EOF":
                        posicao += 1
                        if posicao < len(tokens):
                            ttoken = tokens[posicao][0]
                        else:
                            break
                    continue  # tenta continuar análise após a recuperação

                # Se a regra foi encontrada, empilha a produção (em ordem reversa)
                for simbolo in reversed(regra):
                    if simbolo != "ε":  # ignora produções vazias
                        pilha.append(simbolo)

            # Caso 3: topo é ε → simplesmente ignora
            elif topo == "ε":
                continue

            # Caso 4: erro inesperado (símbolo terminal incorreto)
            else:
                print(f"[ERRO] Token inesperado '{ttoken}', esperado '{topo}'.")
                posicao += 1
                if posicao < len(tokens):
                    ttoken = tokens[posicao][0]
                else:
                    break

        print("\nAnálise sintática concluída (modo pânico ativo).")
