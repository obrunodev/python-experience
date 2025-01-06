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


class ReagBoletoPDF(object):

    def __init__(self, file_descr, landscape=False):
        if landscape:
            pagesize = pagesize_landscape(A4)
        else:
            pagesize = A4

        self.c = canvas.Canvas(file_descr, pagesize=pagesize)
        self.c.setStrokeColor(colors.black)
    
    def marcacao_dimensao_reag(self):
        # Configuração do tamanho da página A4
        page_width, page_height = A4
        c = self.c
        
        # Dimensões da Ficha de Compensação em mm
        ficha_width = 170 * mm  # Largura mínima de 170 mm
        ficha_height = 95 * mm  # Altura mínima de 95 mm
        
        # Dimensões do Recibo do Pagador (a critério do banco, vamos definir como 100 x 170 mm)
        recibo_width = 170 * mm
        recibo_height = 100 * mm
        
        # Posição inicial (margem superior para o recibo)
        x_start = 20 * mm
        y_start = page_height - (recibo_height + ficha_height + 20 * mm)  # Margem de 20 mm

        # Desenhar o Recibo do Pagador
        c.setStrokeColor("black")
        c.setLineWidth(1)
        c.rect(x_start, y_start + ficha_height, recibo_width, recibo_height)  # Retângulo do Recibo
        c.setFont("Helvetica", 8)
        c.drawString(x_start + 10 * mm, y_start + ficha_height + recibo_height - 10 * mm, "Recibo do Pagador")
        c.drawString(x_start + 10 * mm, y_start + ficha_height + recibo_height - 20 * mm, "Valor do Documento: R$ 0,00")
        c.drawString(x_start + 10 * mm, y_start + ficha_height + recibo_height - 30 * mm, "Nosso Número: 000000000")
        c.drawString(x_start + 10 * mm, y_start + ficha_height + recibo_height - 40 * mm, "Carteira: 00")
        c.drawString(x_start + 10 * mm, y_start + ficha_height + recibo_height - 50 * mm, "Agência/Código do Beneficiário: 0000/000000")
        c.drawString(x_start + 10 * mm, y_start + ficha_height + recibo_height - 60 * mm, "Data do Vencimento: 00/00/0000")

        # Desenhar a Ficha de Compensação
        c.setStrokeColor("black")
        c.setLineWidth(1)
        c.rect(x_start, y_start, ficha_width, ficha_height)  # Retângulo da Ficha de Compensação

        # Cabeçalho da Ficha de Compensação (Nome do Banco e Linha Digitável)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_start + 10 * mm, y_start + ficha_height - 10 * mm, "Banco Exemplo S.A. 001-9")  # Nome e número do banco
        c.setFont("Helvetica", 8)
        c.drawString(x_start + ficha_width - 90 * mm, y_start + ficha_height - 10 * mm, "12345.67890 12345.678901 12345.678901 1 12340000012345")  # Linha digitável

        # Linha de corte
        c.setDash(3, 3)  # Linha tracejada
        c.line(x_start, y_start + ficha_height, x_start + ficha_width, y_start + ficha_height)

        # Dados genéricos na Ficha de Compensação
        c.setDash()  # Retira a linha tracejada
        c.setFont("Helvetica", 8)
        c.drawString(x_start + 10 * mm, y_start + ficha_height - 30 * mm, "Pagador: Nome do Pagador")
        c.drawString(x_start + 10 * mm, y_start + ficha_height - 40 * mm, "CPF/CNPJ: 000.000.000-00")
        c.drawString(x_start + 10 * mm, y_start + ficha_height - 50 * mm, "Endereço: Endereço do Pagador")
        c.drawString(x_start + 10 * mm, y_start + ficha_height - 60 * mm, "Cidade/UF: Cidade - UF")
        c.drawString(x_start + ficha_width - 90 * mm, y_start + ficha_height - 70 * mm, "Valor do Documento: R$ 0,00")
        c.drawString(x_start + ficha_width - 90 * mm, y_start + ficha_height - 80 * mm, "Data do Vencimento: 00/00/0000")

    def draw_line(self, x1, y1, x2, y2):
        self.c.line(x1, y1, x2, y2)

    def draw_recibo(self):
        self.draw_lines(self.c, 26, 150)
    
    def draw_lines(c, x_start, y_start):
        """Desenha as 3 linhas no canto superior esquerdo."""
        # Linha vertical esquerda
        c.line(x_start, y_start, x_start, y_start + 50)
        # Linha vertical direita
        c.line(x_start + 114, y_start, x_start + 114, y_start + 50)
        # Linha horizontal superior
        c.line(x_start, y_start + 50, x_start + 114, y_start + 50)
    
    def draw_ficha_compensação(self):
        self.draw_recibo()
        ...

    def draw_boleto(self, boleto_dados):
        self.marcacao_dimensao_reag()
        self.draw_ficha_compensação()
        self.draw_recibo()
    
    def save(self):
        self.c.save()


