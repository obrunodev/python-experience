from services.boleto.abc import BoletoABC
from pyboleto.pdf import BoletoPDF
import datetime


def gerar_boleto_reag():
    ...


def gerar_boleto_abc():
    lista_dados = []

    for i in range(1):
        b = BoletoABC(7, 2)
        b.nosso_numero = '87654'
        b.numero_documento = '27.030195.10'
        b.convenio = '7777777'
        b.especie_documento = 'DM'
        b.especie = 'Real'

        b.carteira = '11'  # 112 corrigir
        b.cedente = 'QFlash Tecnologia'
        b.cedente_documento = "102.323.777-01"
        b.cedente_endereco = ("Rua Acme, 123 - " +
                              "Centro - Sao Paulo/SP - " +
                              "CEP: 12345-678")
        b.agencia_cedente = '9999'
        b.conta_cedente = '99999'

        b.data_vencimento = datetime.date(2010, 3, 27)
        b.data_documento = datetime.date(2010, 2, 12)
        b.data_processamento = datetime.date(2010, 2, 12)

        b.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
        ]
        b.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
        ]
        b.valor_documento = 255.00

        b.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
        ]
        lista_dados.append(b)


    boleto = BoletoPDF('meu-boleto-teste.pdf')
    for i in range(len(lista_dados)):
        boleto.drawBoleto(lista_dados[i])
        boleto.nextPage()
        boleto.save()


if __name__ == '__main__':
    gerar_boleto_abc()
    gerar_boleto_reag()