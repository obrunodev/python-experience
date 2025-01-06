from pyboleto.pdf import BoletoPDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class CustomBoletoPDF(BoletoPDF):

    def drawBoleto(self, boleto_dados):
        # Chame o método super para desenhar o boleto normalmente
        super().drawBoleto(boleto_dados)

        # A partir daqui, você pode adicionar o logo e o nome do banco
        c = self.pdf_canvas


        # Adicionando o nome do banco ao lado do logo
        logo_x = 50  # Posição em x
        logo_y = 735  # Posição em y
        banco_nome = "Banco ABC Brasil"  # Substitua pelo nome do seu banco
        c.setFont("Helvetica-Bold", 10)  # Define a fonte e o tamanho
        c.setFillColor(colors.black)  # Define a cor do texto
        c.drawString(logo_x, logo_y, banco_nome)  # Ajuste a posição do texto

# Uso do CustomBoletoPDF
# arquivo_pdf = CustomBoletoPDF("boleto.pdf")
# boleto_dados = BoletoData()  # Preencha com os dados necessários
# arquivo_pdf.drawBoleto(boleto_dados)
# arquivo_pdf.save()