import re

# ----------------------------------------------------
# Lista de padrões de tokens com expressões regulares
# ----------------------------------------------------
lexemas = [
    ("PRINCIPAL",   r'principal'),
    ("FUNCAO",      r'funcao'),
    ("TIPO_VAR",    r'int|real|cadeia|car|booleano|vazio'),
    ("SENAO",       r'senao'),
    ("SE",          r'se'),
    ("ENQUANTO",    r'enquanto'),
    ("FACA",        r'faca'),
    ("PARA",        r'para'),
    ("RETORNO",     r'retornar'),
    ("BOOLEANO",    r'verdadeiro|falso'),
    ("NUMERO_REAL", r'\d+\.\d+'),        # números reais
    ("NUMERO_INT",  r'\d+'),             # números inteiros
    ("CARACTERE",   r'\'.\''),           # caractere único
    ("PALAVRA",     r'"(?:\\.|[^"\\])*"'),# strings entre aspas
    ("ESCREVER",    r'escrever'),   
    ("IDENT",       r'[a-zA-Z_]\w*'),    # identificadores
    ("COMPAR",      r'[<>]=?|==|!='),    # operadores de comparação
    ("OPER_ARIT",   r'[+\-*/%]'),        # operadores aritméticos
    ("OPER_LOGI",   r'&&|\|\||!'),       # operadores lógicos
    ("ATRIB",       r'='),               # atribuição
    ("LPAREN",      r'\('),              # (
    ("RPAREN",      r'\)'),              # )
    ("LCHAVE",      r'\{'),              # {
    ("RCHAVE",      r'\}'),              # }
    ("VIRGULA",     r','),               # ,
    ("PONTOVIRG",   r';'),               # ;
    ("IGNORAR",     r'[ \t\n]+'),        # espaços e quebras de linha
    ("INCOMPAT",    r'.'),               # qualquer outro caractere
]

# Recebe o código fonte e devolve a lista de tokens
def analisador_lexico(codigo_fonte):
    cadeiaTokens = []

    # Cria uma expressão regular combinando todos os padrões
    expressaoRegular = ""
    for Tokennome, expressao in lexemas:
        expressaoRegular += f"(?P<{Tokennome}>{expressao})|"
    expressaoRegular = expressaoRegular[:-1]  # remove o último '|'

    # Executa o "scanner" — tenta casar cada lexema no código-fonte
    correspondencias = re.finditer(expressaoRegular, codigo_fonte)

    for correspondencia in correspondencias:
        tipo_token = correspondencia.lastgroup  # nome do token (ex: IDENT)
        vtoken = correspondencia.group()        # valor do lexema

        # Ignora espaços e quebras de linha
        if tipo_token == "IGNORAR":
            continue

        # Se encontrou caractere não reconhecido, lança erro
        elif tipo_token == "INCOMPAT":
            raise RuntimeError(f"Caractere inesperado encontrado: {vtoken}")

        # Caso contrário, adiciona o token à lista
        cadeiaTokens.append((tipo_token, vtoken))

    # Adiciona o marcador de fim de arquivo
    cadeiaTokens.append(("EOF", None))

    return cadeiaTokens
