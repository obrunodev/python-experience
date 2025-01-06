from services.boleto.abc import BoletoABC
from services.boleto.pdf import CustomBoletoPDF
from pyboleto.pdf import BoletoPDF
import datetime


def gerar_boleto_reag():
    ...


def gerar_boleto_abc():
    lista_dados = []

    for i in range(1):
        b = BoletoABC(7, 2)
        b.nosso_numero = '87654'
        b.numero_documento = 'QF1234/001'
        b.convenio = '7777777'
        b.especie_documento = 'DM'
        b.especie = 'Real'

        b.carteira = '11'  # 112 corrigir
        b.cedente = 'QFLASH TECNOLOGIA LTDA - CNPJ: 31.604.994/0001-07'
        b.cedente_documento = "102.323.777-01"
        b.cedente_endereco = ("Rua Butanta, 434 - Conjunto 43 e 44 - Pinheiros - CEP: 05424-000 São Paulo - SP")
        b.agencia_cedente = '00010'
        b.conta_cedente = '222287820'

        b.data_vencimento = datetime.date(2020, 12, 29)
        b.data_documento = datetime.date(2020, 11, 2)
        b.data_processamento = datetime.date(2020, 11, 2)

        b.valor_documento = 1000.00

        b.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
        ]
        lista_dados.append(b)


    boleto = CustomBoletoPDF('boleto-abc.pdf')
    for i in range(len(lista_dados)):
        boleto.drawBoleto(lista_dados[i])
        boleto.nextPage()
        boleto.save()


if __name__ == '__main__':
    gerar_boleto_abc()
    gerar_boleto_reag()