# pdf_exporter.py
from fpdf import FPDF

def limpar(texto: str):
    return texto.replace("\n", " ").replace("\r", " ").strip()


def reduzir_lista(valor, limite=18):
    texto = limpar(str(valor))

    if len(texto) <= limite:
        return texto

    if texto.startswith("[") and texto.endswith("]"):
        itens = texto[1:-1].split(",")
        if len(itens) > 2:
            return f"[{itens[0].strip()}, ..., {itens[-1].strip()}]"

    return texto[:limite] + "..."


def reduzir_texto(valor, limite=35):
    texto = limpar(str(valor))

    if len(texto) <= limite:
        return texto
    return texto[:limite] + "..."

class PDF(FPDF):
    def __init__(self):
        super().__init__()

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

def draw_table(pdf, data, col_widths, line_height=6):
    pdf.set_font("DejaVu", "", 10)

    for row in data:

        processed = []
        for cell in row:
            txt = limpar(str(cell))

            # reduzir listas
            if txt.startswith("[") and txt.endswith("]"):
                txt = reduzir_lista(txt, limite=18)
            else:
                txt = reduzir_texto(txt, limite=35)

            processed.append(txt)

        cell_lines = []
        max_height = 0

        for i, cell in enumerate(processed):
            width = col_widths[i]
            lines = pdf.multi_cell(width, line_height, cell, split_only=True)
            cell_lines.append(lines)

            height = len(lines) * line_height
            if height > max_height:
                max_height = height

        if pdf.get_y() + max_height > pdf.page_break_trigger:
            pdf.add_page()
        x = pdf.get_x()
        y = pdf.get_y()

        for i, lines in enumerate(cell_lines):
            width = col_widths[i]

            pdf.rect(x, y, width, max_height)

            pdf.set_xy(x + 1, y + 1)
            for ln in lines:
                pdf.cell(width - 2, line_height, ln, ln=1)

            x += width

        pdf.set_y(y + max_height)

def gerar_pdf(tokens, passos_ll1, passos_slr, gram_convertida,
              caminho="relatorio_compilador.pdf"):

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("=== TABELA DE TOKENS ===")
    tabela_tokens = [["Tipo", "Lexema"]] + [
        [tk[0], tk[1] or ""]
        for tk in tokens
    ]
    draw_table(pdf, tabela_tokens, [40, 120])
    pdf.add_page()
    pdf.chapter_title("=== ÚLTIMOS 10 PASSOS DO LL(1) ===")

    ll1 = [["Passo", "Pilha", "Entrada", "Ação"]]
    for p in passos_ll1[-10:]:
        ll1.append([p[0], p[1], p[2], p[3]])

    draw_table(pdf, ll1, [18, 60, 20, 80])
    pdf.add_page()
    pdf.chapter_title("=== GRAMÁTICA CONVERTIDA PARA LR(0) ===")

    pdf.set_font("DejaVu", "", 10)
    safe_width = pdf.w - 20

    for nt, prods in gram_convertida.items():
        texto = f"{nt}:\n" + "\n".join(f"  • {' '.join(p) if p else 'ε'}" for p in prods)
        pdf.multi_cell(safe_width, 6, texto)
        pdf.ln(2)
    pdf.add_page()
    pdf.chapter_title("=== ÚLTIMOS 25 PASSOS DO SLR(1) ===")

    slr = [["Passo", "Estados", "Símbolos", "Entrada", "Ação"]]
    for p in passos_slr[-25:]:
        slr.append([p[0], p[1], p[2], p[3], p[4]])

    draw_table(pdf, slr, [18, 55, 55, 20, 60])

    pdf.output(caminho)
    print(f"\nPDF gerado com sucesso: {caminho}\n")
