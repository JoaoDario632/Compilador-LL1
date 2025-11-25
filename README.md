# 📝 Compilador Simples com Analisador LL(1)

Este projeto implementa um **compilador simplificado** para uma linguagem fictícia, com análise **léxica** e **sintática** baseada em **LL(1)**.  
Ele permite processar código fonte, identificar tokens e validar a sintaxe de programas escritos em sua gramática definida.

## 📂 Estrutura do Projeto
```
├── main.py # Programa principal
├── scanner.py # Analisador léxico (scanner)
├── ll1_parser.py # Analisador sintático LL(1)
├── grammar.py # Definição da gramática, funções first e follow
├── app.br # Exemplo de código da linguagem
├── slr_parser.py #Analisador Sintático SLR
├── tabela.py  #Demonstração das tabelas de Redução do SLR, Tokens e os Resultados do First e Follow
└── README.md # Documentação do projeto
```

## 🔹 Funcionalidades

1. **Análise Léxica**
   - Reconhece palavras-chave (`principal`, `funcao`, `se`, `senao`, etc.).
   - Identifica tipos de variáveis (`int`, `real`, `cadeia`, `car`, `booleano`, `vazio`).
   - Reconhece identificadores, números inteiros e reais, caracteres, strings e operadores.
   - Gera uma lista de tokens com tipo e valor.

2. **Análise Sintática LL(1)**
   - Valida a sintaxe do código baseado na gramática definida em `grammar.py`.
   - Implementa **primeiro (first)** e **seguinte (follow)** para construção da tabela LL(1).
   - Suporta:
     - Declarações de variáveis e funções
     - Blocos (`{ ... }`)
     - Estruturas condicionais (`se`, `senao`)
     - Laços (`enquanto`, `faca`, `para`)
     - Atribuições e retornos
     - Chamadas de função e expressões
     - Escrita de valores

3. **Mensagens de Erro**
   - Tokens incompatíveis durante a análise léxica geram exceção.
   - Erros de sintaxe no LL(1) informam o token esperado e o encontrado.
   - 
## ⚙️ Gramática da Linguagem

A linguagem aceita programas do tipo:

- programa ::= DECLARACOES PRINCIPAL_BLOCO
- DECLARACOES ::= FUNCAO_DECL DECLARACOES | DECLARACAO DECLARACOES | ε
- PRINCIPAL_BLOCO ::= principal { INSTRUCOES }

EXPRESSAO ::= TERMO EXPRESSAO'
TERMO ::= IDENT | NUMERO_INT | NUMERO_REAL | PALAVRA | BOOLEANO | (EXPRESSAO) | CHAMADA_TERM

## ▶️ Como Executar

- Abra o terminal na pasta do projeto.
- Certifique-se de ter Python 3 instalado.
- Execute o main.py:

## Dependências Usadas

Este projeto uso da biblioteca tabulete, a qual realiza a formatação de dados tabulares, para que eles possa ser exibidos de forma legível
> pip install tabulate
<br>
> pip install fpdf
<br>
> pip install fpdf2

## Para que o PDF seja gerado com as devidos caracteres, instale este arquivo através deste site

https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip/download?use_mirror=sinalbr

# 👨‍💻 Autores
<table>
  <tr>
     <td align="center">
            <a href="https://github.com/JoaoDario632">
         <img src="https://avatars.githubusercontent.com/u/134674876?v=4" style="border-radius: 50%" width="100px;" alt="ferreira"/>
         <br />
         <sub><b>João Dário 💻👑</b></sub>
       </a>
     </td>
    <td align="center">
       <a href="https://github.com/LucasAugustoSS">
         <img src="https://avatars.githubusercontent.com/u/126918429?v=4" style="border-radius: 50%" width="100px;" alt="Lucas augusto"/>
         <br />
         <sub><b>Lucas Augusto 💻👑</b></sub>
       </a>
     </td>
     <td align="center">
          <a href="https://github.com/FrrTiago">
         <img src="https://avatars.githubusercontent.com/u/132114628?v=4" style="border-radius: 50%" width="100px;" alt="ferreira"/>
         <br />
         <sub><b>Tiago Ferreira 💻</b></sub>
       </a>
     </td>
  </tr>
</table>
