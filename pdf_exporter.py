# pdf_exporter.py
from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()

        # Caminho local da fonte enviada
        font_path = "DejaVuSans.ttf"

        # Registrar fonte Unicode completa
        self.add_font("DejaVu", "", font_path, uni=True)

        self.set_font("DejaVu", "", 12)

    def header(self):
        self.set_font("DejaVu", "", 14)
        self.cell(0, 10, "Relatório do Compilador (LL(1) + SLR)", 0, 1, "C")
        self.ln(3)

    def chapter_title(self, title):
        self.set_font("DejaVu", "", 12)
        self.cell(0, 8, title, 0, 1)
        self.ln(1)

    def chapter_body(self, text):
        self.set_font("DejaVu", "", 11)

        safe_width = self.w - 20  # largura segura com margens
        self.multi_cell(safe_width, 6, text, align="L")
        self.ln(2)

def add_table(pdf, headers, rows, col_widths):
    """
    Cria uma tabela real usando recursos nativos do fpdf2.
    """
    pdf.set_font("DejaVu", "", 11)
    for i, head in enumerate(headers):
        pdf.set_fill_color(200, 200, 200)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_widths[i], 8, txt=str(head), border=1, align="C", fill=True)
    pdf.ln()
    for row in rows:
        for i, cell in enumerate(row):
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(col_widths[i], 8, txt=str(cell), border=1, align="L")
        pdf.ln()

    pdf.ln(3)

def gerar_pdf(tokens, passos_ll1, passos_slr, gram_convertida, caminho="relatorio_compilador.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("=== TABELA DE TOKENS ===")

    headers = ["Tipo", "Lexema"]
    rows = [[tk[0], tk[1] if tk[1] else ""] for tk in tokens]
    add_table(pdf, headers, rows, [40, 120])
    pdf.chapter_title("=== ÚLTIMOS PASSOS DO LL(1) ===")

    headers = ["Passo", "Pilha", "Entrada", "Ação"]
    rows = [[p[0], p[1], p[2], p[3]] for p in passos_ll1]
    add_table(pdf, headers, rows, [15, 60, 25, 80])

    pdf.chapter_title("=== GRAMÁTICA CONVERTIDA PARA LR(0) ===")

    safe_width = pdf.w - 20

    for nt, producoes in gram_convertida.items():
        texto = f"{nt}:\n"
        for p in producoes:
            texto += f" • {' '.join(p) if p else 'ε'}\n"

        pdf.multi_cell(safe_width, 6, texto, align="L")
        pdf.ln(1)
    pdf.chapter_title("=== ÚLTIMOS PASSOS DO SLR(1) ===")

    headers = ["Passo", "Pilha Estados", "Pilha Símbolos", "Entrada", "Ação"]
    rows = [[p[0], p[1], p[2], p[3], p[4]] for p in passos_slr]
    add_table(pdf, headers, rows, [15, 40, 40, 20, 60])

    pdf.output(caminho)
    print(f"\nPDF gerado com sucesso em: {caminho}\n")
