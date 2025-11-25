# pdf_exporter.py
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()

        # === Registrar fontes ===
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)

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



# ======================================================
# FUNÇÃO DE TABELA PROFISSIONAL (SEM SOBREPOSIÇÃO)
# ======================================================
def draw_table(pdf, data, col_widths, line_height=6):

    pdf.set_font("DejaVu", "", 10)

    for row in data:

        # 1 - calcular altura real da linha
        max_height = 0
        cell_texts = []

        for idx, cell in enumerate(row):
            width = col_widths[idx]
            text = str(cell)

            lines = pdf.multi_cell(width, line_height, text, split_only=True)
            cell_texts.append(lines)

            height = len(lines) * line_height
            if height > max_height:
                max_height = height

        # 2 - quebra de página se necessário
        if pdf.get_y() + max_height > pdf.page_break_trigger:
            pdf.add_page()

        # 3 - desenhar linha completa
        x = pdf.get_x()
        y = pdf.get_y()

        for idx, lines in enumerate(cell_texts):
            width = col_widths[idx]

            pdf.rect(x, y, width, max_height)

            pdf.set_xy(x + 1, y + 1)
            for ln in lines:
                pdf.cell(width - 2, line_height, ln, ln=1)

            x += width

        pdf.set_xy(pdf.l_margin, y + max_height)



# ======================================================
# FUNÇÃO PRINCIPAL
# ======================================================
def gerar_pdf(tokens, passos_ll1, passos_slr, gram_convertida, caminho="relatorio_compilador.pdf"):

    pdf = PDF()
    pdf.add_page()

    # TABELA DE TOKENS
    pdf.chapter_title("=== TABELA DE TOKENS ===")
    tabela_tokens = [["Tipo", "Lexema"]] + [[tk[0], tk[1] or ""] for tk in tokens]
    draw_table(pdf, tabela_tokens, [40, 120])

    # LL(1)
    pdf.add_page()
    pdf.chapter_title("=== ÚLTIMOS 10 PASSOS DO LL(1) ===")
    ll1 = [["Passo", "Pilha", "Entrada", "Ação"]]
    for p in passos_ll1[-10:]:
        ll1.append([p[0], p[1], p[2], p[3]])
    draw_table(pdf, ll1, [15, 60, 20, 85])

    # GRAMÁTICA
    pdf.add_page()
    pdf.chapter_title("=== GRAMÁTICA CONVERTIDA PARA LR(0) ===")
    pdf.set_font("DejaVu", "", 10)
    safe_width = pdf.w - 20
    for nt, prods in gram_convertida.items():
        texto = f"{nt}:\n" + "\n".join(f"  • {' '.join(p) if p else 'ε'}" for p in prods)
        pdf.multi_cell(safe_width, 6, texto)
        pdf.ln(2)

    # SLR
    pdf.add_page()
    pdf.chapter_title("=== ÚLTIMOS 25 PASSOS DO SLR(1) ===")
    slr = [["Passo", "Estados", "Símbolos", "Entrada", "Ação"]]
    for p in passos_slr[-25:]:
        slr.append([p[0], p[1], p[2], p[3], p[4]])
    draw_table(pdf, slr, [15, 45, 45, 20, 65])

    pdf.output(caminho)
    print(f"\nPDF gerado com sucesso: {caminho}\n")
