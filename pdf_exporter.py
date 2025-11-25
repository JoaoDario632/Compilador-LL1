# pdf_exporter.py
from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()

        # Caminho local da fonte enviada
        font_path = "DejaVuSans.ttf"

        # Registrar fonte Unicode
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
        self.multi_cell(0, 6, text)
        self.ln(2)


def format_table(rows, col_widths=None):
    lines = []
    for row in rows:
        line = ""
        for i, cell in enumerate(row):
            width = col_widths[i] if col_widths else 25
            line += str(cell).ljust(width)
        lines.append(line)
    return "\n".join(lines)


def gerar_pdf(tokens, passos_ll1, passos_slr, gram_convertida, caminho="relatorio_compilador.pdf"):
    pdf = PDF()
    pdf.add_page()

    # ==========================
    # TABELA DE TOKENS
    # ==========================
    pdf.chapter_title("=== TABELA DE TOKENS ===")
    tabela_tokens = [["Tipo", "Lexema"]]
    for tk in tokens:
        tabela_tokens.append([tk[0], tk[1] if tk[1] else ""])
    pdf.chapter_body(format_table(tabela_tokens, [30, 40]))

    # ==========================
    # LL(1)
    # ==========================
    pdf.chapter_title("=== ÚLTIMOS PASSOS DO LL(1) ===")
    ll1_rows = [["Passo", "Pilha", "Entrada", "Ação"]]
    for passo in passos_ll1:
        ll1_rows.append([passo[0], passo[1], passo[2], passo[3]])
    pdf.chapter_body(format_table(ll1_rows, [10, 40, 12, 60]))

    # ==========================
    # GRAMÁTICA LR(0)
    # ==========================
    pdf.chapter_title("=== GRAMÁTICA CONVERTIDA PARA LR(0) ===")
    for nt, producoes in gram_convertida.items():
        texto = f"{nt}:\n"
        for p in producoes:
            texto += f"    • {' '.join(p) if p else 'ε'}\n"
        pdf.chapter_body(texto)

    # ==========================
    # SLR(1)
    # ==========================
    pdf.chapter_title("=== ÚLTIMOS PASSOS DO SLR(1) ===")
    slr_rows = [["Passo", "Pilha Estados", "Pilha Símbolos", "Entrada", "Ação"]]
    for passo in passos_slr:
        slr_rows.append([passo[0], passo[1], passo[2], passo[3], passo[4]])
    pdf.chapter_body(format_table(slr_rows, [10, 30, 30, 10, 40]))

    pdf.output(caminho)
    print(f"\nPDF gerado com sucesso em: {caminho}\n")