# scanner.py
import re
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
    ("NUMERO_REAL", r'\d+\.\d+'),
    ("NUMERO_INT",  r'\d+'),
    ("CARACTERE",   r'\'.\''),
    ("PALAVRA",     r'"(?:\\.|[^"\\])*"'),
    ("ESCREVER",    r'escrever'),   
    ("IDENT",       r'[a-zA-Z_]\w*'),
    ("COMPAR",      r'[<>]=?|==|!='),
    ("OPER_ARIT",   r'[+\-*/%]'),
    ("OPER_LOGI",   r'&&|\|\||!'),
    ("ATRIB",       r'='),
    ("LPAREN",      r'\('),
    ("RPAREN",      r'\)'),
    ("LCHAVE",      r'\{'),
    ("RCHAVE",      r'\}'),
    ("VIRGULA",     r','),
    ("PONTOVIRG",   r';'),
    ("IGNORAR",     r'[ \t\n]+'),
    ("INCOMPAT",    r'.'),
]


def analisador_lexico(codigo_fonte):
    cadeiaTokens = []

    expressaoRegular = ""
    for Tokennome, expressao in lexemas:
        expressaoRegular += f"(?P<{Tokennome}>{expressao})|"
    expressaoRegular = expressaoRegular[:-1]

    correspondencias = re.finditer(expressaoRegular, codigo_fonte)

    for correspondencia in correspondencias:
        tipo_token = correspondencia.lastgroup
        vtoken = correspondencia.group()

        if tipo_token == "IGNORAR":
            continue
        elif tipo_token == "INCOMPAT":
            raise RuntimeError(f"Caractere inesperado encontrado: {vtoken}")
        cadeiaTokens.append((tipo_token.lower(), vtoken))

    cadeiaTokens.append(("eof", None)) 

    return cadeiaTokens
