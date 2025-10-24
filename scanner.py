# scanner.py
import re

# ===== Definição dos lexemas =====
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
    ("IGNORAR",     r'[ \t\n]+'),  # Espaços em branco são ignorados
    ("INCOMPAT",    r'.'),          # Qualquer outro caractere inválido
]

def analisador_lexico(codigo_fonte):
    """Analisa o código fonte e retorna uma lista de tokens"""
    cadeiaTokens = []

    # Monta a regex combinando todos os lexemas
    expressaoRegular = ""
    for Tokennome , expressao in lexemas:
        expressaoRegular += f"(?P<{Tokennome}>{expressao})|"
    expressaoRegular = expressaoRegular[:-1]  # remove o último '|'

    # Encontra todas as correspondências no código fonte
    correspondencias = re.finditer(expressaoRegular, codigo_fonte)

    for correspondencia in correspondencias:
        tipo_token = correspondencia.lastgroup
        vtoken = correspondencia.group()

        if tipo_token == "IGNORAR":
            continue  # Ignora
