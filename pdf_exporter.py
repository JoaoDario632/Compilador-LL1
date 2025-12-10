# pdf_exporter.py
from fpdf import FPDF

#  FONTE E CONFIGURAÇÃO DO PDF
class PDF(FPDF):
    def __init__(self):
        super().__init__()

        # fontes dentro da pasta fonts/
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)

        self.set_auto_page_break(auto=True, margin=12)
        self.set_font("DejaVu", "", 12)

    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "Relatório do Compilador (LL(1) + SLR)", 0, 1, "C")
        self.ln(4)

    def chapter_title(self, title):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 8, title, 0, 1)
        self.ln(2)

def abreviar(texto, limite):
    texto = str(texto)
    if len(texto) > limite and len(texto) > 12:
        return texto[:limite - 3] + "..."
    return texto


def wrap_text(text, nmaximoChar):
    """Quebra texto em linhas sem quebrar palavras."""
    words = text.split()
    lines = []
    line = ""

    for w in words:
        if len(line) + len(w) + 1 <= nmaximoChar:
            line += (" " + w) if line else w
        else:
            lines.append(line)
            line = w

    if line:
        lines.append(line)

    return lines

def quebrar_tokens(texto):
    tokens = texto.split()
    linhas = []

    for i in range(0, len(tokens), 1):
        linhas.append(" ".join(tokens[i:i + 1]))

    return linhas

#  TABELAS COM ABREVIAÇÃO
def draw_table(pdf, data, col_widths, line_height=6, pilha_cols=[]):

    pdf.set_font("DejaVu", "", 9)

    for row in data:

        linhasCelulas = []
        max_lines = 0

        for i, cell in enumerate(row):
            width = col_widths[i]
            nmaximoChar = max(8, int(width / 2.1))

            text = abreviar(cell, nmaximoChar * 3)
            
            if i in pilha_cols:
                wrapped = quebrar_tokens(text)
            else:
                wrapped = wrap_text(text, nmaximoChar)

            linhasCelulas.append(wrapped)
            max_lines = max(max_lines, len(wrapped))

        row_h = max_lines * line_height + 3

        if pdf.get_y() + row_h > pdf.page_break_trigger:
            pdf.add_page()

        x_start = pdf.get_x()
        y_start = pdf.get_y()
        x = x_start

        for i, lines in enumerate(linhasCelulas):
            width = col_widths[i]

            # desenha o retângulo
            pdf.rect(x, y_start, width, row_h)

            # salva posição interna
            x_cell = x
            y_cell = y_start

            texto_formatado = "\n".join(lines)
            pdf.set_xy(x_cell + 1, y_cell)
            pdf.multi_cell(width - 2, line_height, texto_formatado)

            # Após terminar a célula
            pdf.set_xy(x + width, y_start)

            x += width

        pdf.set_xy(x_start, y_start + row_h)

#  FUNÇÃO PRINCIPAL: gerar_pdf()
def gerar_pdf(tokens, passos_ll1, passos_slr, gram_convertida, caminho="relatorio_compilador.pdf"):

    pdf = PDF()
    pdf.add_page()

    # TABELA TOKENS
    pdf.chapter_title("=== TABELA DE TOKENS ===")
    tabela_tokens = [["Tipo", "Lexema"]] + [
        [tk[0], tk[1] or ""] for tk in tokens
    ]
    draw_table(pdf, tabela_tokens, [40, 120])

    # GRAMÁTICA
    pdf.add_page()
    pdf.chapter_title("=== GRAMÁTICA CONVERTIDA PARA LR(0) ===")

    pdf.set_font("DejaVu", "", 10)
    safe_width = pdf.w - 20

    for nt, prods in gram_convertida.items():
        texto = f"{nt}:\n" + "\n".join(f"  • {' '.join(p) if p else 'ε'}" for p in prods)
        pdf.multi_cell(safe_width, 6, texto)
        pdf.ln(2)

    # LL(1)
    pdf.add_page()
    pdf.chapter_title("=== ÚLTIMOS 25 PASSOS DO LL(1) ===")

    ll1_data = [["Passo", "Pilha", "Entrada", "Ação"]]
    for p in passos_ll1[-25:]:
        ll1_data.append([p[0], p[1], p[2], p[3]])

    draw_table(pdf, ll1_data, [20, 70, 25, 75], pilha_cols=[1])

    # SLR
    pdf.add_page()
    pdf.chapter_title("=== ÚLTIMOS 25 PASSOS DO SLR(1) ===")

    slr_data = [["Passo", "Estados", "Símbolos", "Entrada", "Ação"]]
    for p in passos_slr[-25:]:
        slr_data.append([p[0], p[1], p[2], p[3], p[4]])

    draw_table(pdf, slr_data, [20, 40, 60, 20, 50], pilha_cols=[2])

    pdf.output(caminho)
    print(f"\nPDF gerado com sucesso: {caminho}\n")
