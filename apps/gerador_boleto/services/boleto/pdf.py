from pyboleto.pdf import BoletoPDF, load_image
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, landscape as pagesize_landscape
from reportlab.pdfgen import canvas

class ABCBoletoPDF(BoletoPDF):

    def __horizontalLine(self, x, y, width):
        self.pdf_canvas.line(x, y, x + width, y)

    def __verticalLine(self, x, y, width):
        self.pdf_canvas.line(x, y, x, y + width)

    def _drawReciboSacado(self, boleto_dados, x, y):
        self.pdf_canvas.saveState()

        self.pdf_canvas.translate(x, y)

        # De baixo para cima posicao 0,0 esta no canto inferior esquerdo
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        y = 1.5 * self.height_line
        y += 82
        self.pdf_canvas.drawRightString(
            self.width,
            (1.5 * self.height_line) + self.delta_title + 81,
            'Autenticação Mecânica / Ficha de Compensação'
        )

        # Primeira linha depois do codigo de barra
        y += self.height_line
        self.pdf_canvas.setLineWidth(2)
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.space, 'Código de baixa'
        )
        self.pdf_canvas.drawString(0, y + self.space, 'Pagador / Avalista')

        y += self.height_line
        self.pdf_canvas.drawString(0, y + self.delta_title, 'Nome do Pagador')
        sacado = boleto_dados.sacado

        # Linha grossa dividindo o Sacado
        y += self.height_line
        self.pdf_canvas.setLineWidth(2)
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.setFont('Helvetica', self.font_size_value)
        for i in range(len(sacado)):
            self.pdf_canvas.drawString(
                25 * mm,
                (y - 10) - (i * self.delta_font),
                sacado[i]
            )
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        # Linha vertical limitando todos os campos da direita
        self.pdf_canvas.setLineWidth(1)
        self.__verticalLine(self.width - (45 * mm), y, 9 * self.height_line)
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            '(=) Valor cobrado'
        )

        # Campos da direita
        y += self.height_line
        self.__horizontalLine(self.width - (45 * mm), y, 45 * mm)
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            '(+) Outros acréscimos'
        )

        y += self.height_line
        self.__horizontalLine(self.width - (45 * mm), y, 45 * mm)
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            '(+) Mora/Multa'
        )

        y += self.height_line
        self.__horizontalLine(self.width - (45 * mm), y, 45 * mm)
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            '(-) Outras deduções'
        )

        y += self.height_line
        self.__horizontalLine(self.width - (45 * mm), y, 45 * mm)
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            '(-) Descontos/Abatimentos'
        )
        self.pdf_canvas.drawString(
            0,
            y + self.delta_title,
            'Instruções (Informações de responsabilidade do beneficiário)'
        )

        self.pdf_canvas.setFont('Helvetica', self.font_size_value)
        instrucoes = boleto_dados.instrucoes
        for i in range(len(instrucoes)):
            self.pdf_canvas.drawString(
                2 * self.space,
                y - (i * self.delta_font),
                instrucoes[i]
            )
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        # Linha horizontal com primeiro campo Uso do Banco
        y += self.height_line
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.drawString(0, y + self.delta_title, 'Uso do banco')

        self.__verticalLine((30) * mm, y, 2 * self.height_line)
        self.pdf_canvas.drawString(
            (30 * mm) + self.space,
            y + self.delta_title,
            'Carteira'
        )

        self.__verticalLine((30 + 20) * mm, y, self.height_line)
        self.pdf_canvas.drawString(
            ((30 + 20) * mm) + self.space,
            y + self.delta_title,
            'Espécie'
        )

        self.__verticalLine(
            (30 + 20 + 20) * mm,
            y,
            2 * self.height_line
        )
        self.pdf_canvas.drawString(
            ((30 + 40) * mm) + self.space,
            y + self.delta_title,
            'Quantidade'
        )

        self.__verticalLine(
            (30 + 20 + 20 + 20 + 20) * mm, y, 2 * self.height_line)
        self.pdf_canvas.drawString(
            ((30 + 40 + 40) * mm) + self.space, y + self.delta_title, 'Valor')

        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            '(=) Valor documento'
        )

        self.pdf_canvas.setFont('Helvetica', self.font_size_value)
        self.pdf_canvas.drawString(
            (30 * mm) + self.space,
            y + self.space,
            boleto_dados.carteira
        )
        self.pdf_canvas.drawString(
            ((30 + 20) * mm) + self.space,
            y + self.space,
            boleto_dados.especie
        )
        self.pdf_canvas.drawString(
            ((30 + 20 + 20) * mm) + self.space,
            y + self.space,
            boleto_dados.quantidade
        )
        valor = self._formataValorParaExibir(boleto_dados.valor)
        self.pdf_canvas.drawString(
            ((30 + 20 + 20 + 20 + 20) * mm) + self.space,
            y + self.space,
            valor
        )
        valor_documento = self._formataValorParaExibir(
            boleto_dados.valor_documento
        )
        self.pdf_canvas.drawRightString(
            self.width - 2 * self.space,
            y + self.space,
            valor_documento
        )
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        # Linha horizontal com primeiro campo Data documento
        y += self.height_line
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.drawString(
            0,
            y + self.delta_title,
            'Data do documento'
        )
        self.pdf_canvas.drawString(
            (30 * mm) + self.space,
            y + self.delta_title,
            'N. do documento'
        )
        self.pdf_canvas.drawString(
            ((30 + 40) * mm) + self.space,
            y + self.delta_title,
            'Espécie doc'
        )
        self.__verticalLine(
            (30 + 20 + 20 + 20) * mm,
            y,
            self.height_line
        )
        self.pdf_canvas.drawString(
            ((30 + 40 + 20) * mm) + self.space,
            y + self.delta_title,
            'Aceite'
        )
        self.pdf_canvas.drawString(
            ((30 + 40 + 40) * mm) + self.space,
            y + self.delta_title,
            'Data processamento'
        )
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            'Nosso número'
        )

        self.pdf_canvas.setFont('Helvetica', self.font_size_value)
        self.pdf_canvas.drawString(
            0,
            y + self.space,
            boleto_dados.data_documento.strftime('%d/%m/%Y')
        )
        self.pdf_canvas.drawString(
            (30 * mm) + self.space,
            y + self.space,
            boleto_dados.numero_documento
        )
        self.pdf_canvas.drawString(
            ((30 + 40) * mm) + self.space,
            y + self.space,
            boleto_dados.especie_documento
        )
        self.pdf_canvas.drawString(
            ((30 + 40 + 20) * mm) + self.space,
            y + self.space,
            boleto_dados.aceite
        )
        self.pdf_canvas.drawString(
            ((30 + 40 + 40) * mm) + self.space,
            y + self.space,
            boleto_dados.data_processamento.strftime('%d/%m/%Y')
        )
        self.pdf_canvas.drawRightString(
            self.width - 2 * self.space,
            y + self.space,
            boleto_dados.format_nosso_numero()
        )
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        # Linha horizontal com primeiro campo Cedente
        y += self.height_line
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.drawString(0, y + self.delta_title, 'Beneficiário')
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            'Agência/Código Beneficiário'
        )

        self.pdf_canvas.setFont('Helvetica', self.font_size_value)
        self.pdf_canvas.drawString(0, y + self.space, boleto_dados.cedente)
        self.pdf_canvas.drawRightString(
            self.width - 2 * self.space,
            y + self.space,
            boleto_dados.agencia_conta_cedente
        )
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        # Linha horizontal com primeiro campo Local de Pagamento
        y += self.height_line
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.drawString(
            0,
            y + self.delta_title,
            'Local de pagamento'
        )
        self.pdf_canvas.drawString(
            self.width - (45 * mm) + self.space,
            y + self.delta_title,
            'Vencimento'
        )

        self.pdf_canvas.setFont('Helvetica', self.font_size_value)
        self.pdf_canvas.drawString(
            0,
            y + self.space,
            boleto_dados.local_pagamento
        )
        self.pdf_canvas.drawRightString(
            self.width - 2 * self.space,
            y + self.space,
            boleto_dados.data_vencimento.strftime('%d/%m/%Y')
        )
        self.pdf_canvas.setFont('Helvetica', self.font_size_title)

        # Linha grossa com primeiro campo logo tipo do banco
        self.pdf_canvas.setLineWidth(3)
        y += self.height_line
        self.__horizontalLine(0, y, self.width)
        self.pdf_canvas.setLineWidth(2)
        self.__verticalLine(40 * mm, y, self.height_line)  # Logo Tipo
        self.__verticalLine(60 * mm, y, self.height_line)  # Numero do Banco

        if boleto_dados.logo_image:
            logo_image_path = load_image(boleto_dados.logo_image)
            self.pdf_canvas.drawImage(
                logo_image_path,
                0,
                y + self.space + 1,
                40 * mm,
                self.height_line,
                preserveAspectRatio=True,
                anchor='sw'
            )
        self.pdf_canvas.setFont('Helvetica-Bold', 18)
        self.pdf_canvas.drawCentredString(
            50 * mm,
            y + 2 * self.space,
            boleto_dados.codigo_dv_banco
        )
        self.pdf_canvas.setFont('Helvetica-Bold', 11.5)
        self.pdf_canvas.drawRightString(
            self.width,
            y + 2 * self.space,
            boleto_dados.linha_digitavel
        )

        self.pdf_canvas.restoreState()

        return self.width, (y + self.height_line)

    def draw_bank_name(self, banco_nome, logo_x, logo_y):
        c = self.pdf_canvas
        c.setFont("Helvetica-Bold", 10)  
        c.setFillColor(colors.black)
        c.drawString(logo_x, logo_y, banco_nome)
        c.drawString(logo_x, logo_y - 440, banco_nome)

    def drawBoleto(self, boleto_dados):
        # Chame o método super para desenhar o boleto normalmente
        super().drawBoleto(boleto_dados)
        self.draw_bank_name("Banco ABC Brasil", 50, 735)


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

class ReagBoletoPDF(object):

    def __init__(self, file_descr, landscape=False):
        if landscape:
            pagesize = pagesize_landscape(A4)
        else:
            pagesize = A4

        self.c = canvas.Canvas(file_descr, pagesize=pagesize)
        self.c.setStrokeColor(colors.black)


    def draw_line(self, x1, y1, x2, y2):
        self.c.line(x1, y1, x2, y2)


    def draw_linha_a(self, x_start, y_start):
        """Desenha a primeira linha do boleto"""
        c = self.c
        c.line(x_start, y_start, x_start, y_start + 50)  # Linha vertical esquerda
        c.line(x_start + 114, y_start, x_start + 114, y_start + 50)  # Linha vertical direita
        c.line(x_start, y_start + 50, x_start + 114, y_start + 50)  # Linha horizontal superior
        c.line(x_start, y_start, x_start + 170 * mm, y_start)  # Linha horizontal inferior

        text_x = x_start + 7  # Ajuste da posição horizontal
        text_y = y_start + 20  # Ajuste da posição vertical
        c.setFont("Helvetica", 12)  # Fonte e tamanho do texto
        c.drawString(text_x, text_y, "LOGOTIPO REAG")

        # Adicionar o nome do banco, código do banco e linha digitável ao lado direito do retângulo
        banco_x = x_start + 120  # Posiciona ao lado direito do retângulo
        banco_y = y_start + 5  # Posição vertical
        nome_banco = "Banco REAG"
        codigo_banco = "528-2"
        c.setFont("Helvetica-Bold", 8)  # Fonte para o nome do banco
        c.drawString(banco_x, banco_y, f"{nome_banco} | {codigo_banco}")  # Nome do banco

        # Linha digitável
        linha_digitavel_x = banco_x + 80
        linha_digitavel = "99999.99999 99999.99999 99999.99999D 99999999999999"
        c.setFont("Helvetica", 8)  # Fonte tipo monoespaçada para simular a linha digitável
        c.drawString(linha_digitavel_x, banco_y, f"| {linha_digitavel}")
    

    def draw_linha_b(self, x_start, y_start, width):
        """Desenha a linha B com as informações de local de pagamento, incluindo bordas."""
        c = self.c
        # Borda
        height = 25
        c.rect(x_start, y_start - height, width, height)

        # Linha de pagamento
        c.setFont("Helvetica", 8)
        c.drawString(x_start + 5, y_start - 10, "Local de Pagamento:")
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x_start + 5, y_start - 22, "Pagável Preferencialmente na Rede Banco REAG ou no Banco REAG Expresso")


    def draw_linha_c(self, x_start, y_start, width):
        """Desenha a linha C com as informações do beneficiário, incluindo bordas."""
        c = self.c
        # Borda
        height = 25
        c.rect(x_start, y_start - height, width, height)

        # Nome do beneficiário
        c.setFont("Helvetica", 8)
        c.drawString(x_start + 5, y_start - 10, "Nome do beneficiário/CPF/CNPJ/Endereço:")
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x_start + 5, y_start - 22, "QFLASH TECNOLOGIA LTDA – CNPJ: 31.504.994/0001-07")


    def draw_linha_d(self, x_start, y_start, width):
        """Desenha a linha D com os detalhes do documento."""
        c = self.c
        # Borda
        height = 35
        c.rect(x_start, y_start - height, width, height)

        # Colunas
        col_widths = [width * 0.2, width * 0.2, width * 0.2, width * 0.2, width * 0.2]
        col_titles = [
            "Data do Documento",
            "Número do Documento",
            "Espécie Documento",
            "Aceite",
            "Data Processamento",
        ]
        col_values = ["18/11/2024", "QF2024/007", "DM", "N", "18/11/2024"]

        # Títulos
        for i, title in enumerate(col_titles):
            c.setFont("Helvetica", 8)
            c.drawString(x_start + sum(col_widths[:i]) + 5, y_start - 7, title)

        # Valores
        for i, value in enumerate(col_values):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x_start + sum(col_widths[:i]) + 5, y_start - 30, value)


    def draw_linha_e(self, x_start, y_start, width):
        """Desenha a linha E com os valores do documento."""
        c = self.c
        # Borda
        height = 25
        c.rect(x_start, y_start - height, width, height)

        # Colunas
        col_widths = [width * 0.15, width * 0.1, width * 0.15, width * 0.1, width * 0.25, width * 0.25]
        col_titles = ["Uso do Banco", "CIP", "Carteira", "Moeda", "Quantidade", "Valor"]
        col_values = ["", "", "112", "R$", "", "1.500,00"]

        # Títulos
        for i, title in enumerate(col_titles):
            c.setFont("Helvetica", 8)
            c.drawString(x_start + sum(col_widths[:i]) + 5, y_start - 10, title)

        # Valores
        for i, value in enumerate(col_values):
            c.setFont("Helvetica-Bold", 8)
            c.drawString(x_start + sum(col_widths[:i]) + 5, y_start - 20, value)


    def draw_recibo(self, x_start, y_start, width, height):
        """Desenha recibo do pagador."""
        c = self.c

        # Borda principal
        c.setStrokeColor("black")
        c.setLineWidth(1)
        c.rect(x_start, y_start, width, height)

        # Linhas internas
        self.draw_linha_a(x_start, y_start + height - 50)
        self.draw_linha_b(x_start, y_start + height - 50, width)
        self.draw_linha_c(x_start, y_start + height - 75, width)
        self.draw_linha_d(x_start, y_start + height - 100, width)
        self.draw_linha_e(x_start, y_start + height - 135, width)

    def draw_ficha_compensacao(self, x_start, y_start, width, height):
        """Desenha a Ficha de Compensação."""
        c = self.c

        # Desenhar retângulo da ficha
        c.setStrokeColor("black")
        c.setLineWidth(1)
        c.rect(x_start, y_start, width, height)

        # Desenhar as 3 linhas no canto superior esquerdo
        self.draw_linha_a(x_start, y_start + height - 50)

    def draw_boleto(self, boleto_dados):
        # Configuração do tamanho da página A4
        page_width, page_height = A4
        c = self.c

        # Dimensões em mm
        ficha_width = 170 * mm
        ficha_height = 95 * mm
        recibo_width = 170 * mm
        recibo_height = 100 * mm
        spacing_between_sections = 50 * mm  # Espaço entre os retângulos

        # Margem e posição inicial
        x_start = 20 * mm
        y_start = page_height - (recibo_height + ficha_height + spacing_between_sections + 20 * mm)  # Margem de 20 mm

        self.draw_recibo(x_start, y_start + ficha_height + spacing_between_sections, recibo_width, recibo_height)
        self.draw_ficha_compensacao(x_start, y_start, ficha_width, ficha_height)

        # Linha de corte entre o recibo e a ficha
        c.setDash(3, 3)  # Linha tracejada
        c.line(x_start, y_start + ficha_height + (spacing_between_sections / 2),
               x_start + ficha_width, y_start + ficha_height + (spacing_between_sections / 2))
        c.setDash()  # Retira a linha tracejada

    def save(self):
        self.c.save()



