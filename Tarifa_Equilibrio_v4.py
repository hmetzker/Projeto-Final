# calcula a tarifa de equilíbrio em função da variação (perda ou ganho) entre dois períodos distintos

# 1- temos somente 1 importação da planilha BD2.xlsx e 1 DataFrame (planilha_BD2 e d_fr), ambos com
# base em pesquisas no Pandas através dos anos digitados (keys) e aos totais (values);
# 2- para auxiliar no código, utilizamos conversões da planilha e do DataFrame para uma lista e um dicionário;
# 3- Arquivo BD2.xlsx com N planilhas separadas por cada ano, contendo dados de km e pax pagantes.
# 4- Introdução de interface para entrada e saída de dados através da Framework GUI Tkinter


import pandas as pd
import xlsxwriter
import tkinter as tk
from tkinter import ttk
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')


class CalculaTarifa:

    def __init__(self, ano_atipico, ano_referencia, tarifa_vigente, perda_custo, planilha_BD2, lista_excel):
# variáveis de entrada
        self.ano_atipico = ano_atipico                      # ano da queda de oferta/ demanda de pax
        self.ano_referencia = ano_referencia                # ano de referência relativo à ofeta/ demanda de pax
        self.tarifa_vigente = tarifa_vigente                # tarifa praticada vigente
        self.perda_custo = float(perda_custo) / 100         # perda pela retirada de veículos da frota de ônibus
        self.planilha_BD2 = planilha_BD2                    # planilha BD2 importada para o Pandas
        self.lista_excel = lista_excel                      # corresponde BD2.xlsx convertido em lista

# variáveis de saída
        self.total_ano_anterior_km = 0
        self.total_ano_anterior_pax = 0
        self.total_ano_atipico_km = 0
        self.total_ano_atipico_pax = 0
        self.tarifa_equilibrio = 0

# totais do ano atípico e do ano de referência (oferta/ demanda de pax de acordo com o planejamento)
    def soma_excel(self):
        tabelaKM = {}
        tabelaPAX = {}
        for i in range(len(self.lista_excel)):
            d_fr = pd.DataFrame(self.planilha_BD2[self.lista_excel[i]])
            tabelaKM.update({self.lista_excel[i]: d_fr['km coberto'].sum()})
            tabelaPAX.update({self.lista_excel[i]: d_fr['pax pagantes'].sum()})
            if self.ano_atipico == self.lista_excel[i]:
                self.total_ano_atipico_km = tabelaKM[self.lista_excel[i]]
                self.total_ano_atipico_pax = tabelaPAX[self.lista_excel[i]]
            if self.ano_referencia == self.lista_excel[i]:
                self.total_ano_anterior_km = tabelaKM[self.lista_excel[i]]
                self.total_ano_anterior_pax = tabelaPAX[self.lista_excel[i]]
        return self.total_ano_anterior_km, self.total_ano_anterior_pax, self.total_ano_atipico_km, self.total_ano_atipico_pax

# calculo do IPK de pax pagantes do ano de referência (oferta/ demanda de pax de acordo com o planejamento)
    def calcula_ipk_ano_anterior(self):
        return self.total_ano_anterior_pax / self.total_ano_anterior_km

# calculo do IPK de pax pagantes do ano atípico (ano de queda de oferta/ demanda de pax)
    def calcula_ipk_ano_atipico(self):
        return self.total_ano_atipico_pax / self.total_ano_atipico_km

# tarifa calculada em função da queda de oferta/ demanda de pax (manutenção do equilíbrio econômico-financeiro)
    def tarifa_equilibrada(self):
        custo_atual = float(self.tarifa_vigente) * self.calcula_ipk_ano_anterior()
        custo_novo = custo_atual * (1 - (self.total_ano_atipico_km / self.total_ano_anterior_km * self.perda_custo))
        self.tarifa_equilibrio = custo_novo / self.calcula_ipk_ano_atipico()
        return self.calcula_ipk_ano_anterior(), self.calcula_ipk_ano_atipico(), self.tarifa_equilibrio

# mostrando gráfico de barras, com index modificado
    def mostra_grafico(self):
        self.geraExcel = pd.DataFrame({'valor': [float(self.tarifa_vigente), float(self.tarifa_equilibrio)]},
                                      index=['T-vig', 'T-eq'])
        self.geraExcel['valor'].plot.barh()
        return plt.show()

# gerando arquivo BD3.xlsx com as tarifas vigente e de equilíbrio
    def gera_Excel(self):
        gravaExcel = xlsxwriter.Workbook('BD3.xlsx')
        planilhaUnica = gravaExcel.add_worksheet('Tarifa de equilíbrio')
        monta_celulas = (['T-vig', locale.currency(self.tarifa_vigente)], ['T-eq', locale.currency(self.tarifa_equilibrio)])
        centro = gravaExcel.add_format()
        centro.set_align('center')
        centro.set_bold()
        row = 0
        col = 0
        planilhaUnica.write(row, col + 1, 'Valores', centro)
        row += 1
        for i, j in monta_celulas:
            planilhaUnica.write(row, col, i, centro)
            planilhaUnica.write(row, col + 1, j)
            row += 1

        gravaExcel.close()
        return

# trabalha com os valores da GUI
def inicio():
    ano_atip = combo_anoAtip.get()
    ano_ref = combo_anoRef.get()
    tarifa_vig = mediaTarifa()
    perda_oferta = text_custo.get()
    if perda_oferta == '' or perda_oferta == 0:
        perda_oferta = 0.001

    ct = CalculaTarifa(ano_atip, ano_ref, tarifa_vig, perda_oferta, planilha_0, lista_BD2)
    total = ct.soma_excel()
    for i in range(0, len(total), 2):
        saida_km = f'Produção quilométrica em {ano_atip} = '
        saida_pax = f'Passageiros pagantes em {ano_atip} = '
        if i == 0:
            saida_km = f'Produção quilométrica em {ano_ref} = '
            saida_pax = f'Passageiros pagantes em {ano_ref} = '
        saida = f'{saida_km}{total[i]:,.0f}'
        for nada in range(11):
            label_nada = tk.Label(Janela, text=f'')
            label_nada.grid(row=nada, column=0, padx=0, pady=0, stick='W')

        label_km = tk.Label(Janela, text=saida)
        label_km.grid(row=i + 11, column=0, padx=44, pady=1, stick='W')
        saida = f'{saida_pax}{total[i + 1]:,.0f}'
        label_pax = tk.Label(Janela, text=saida)
        label_pax.grid(row=i + 12, column=0, padx=44, pady=1, stick='W')

    t_eq = ct.tarifa_equilibrada()
    for i in range(len(t_eq)):
        saida_te = f'Índice de passageiros pagantes por quilômetro em {ano_atip} = '
        teq = round(t_eq[i], 4)
        if i == 0:
            saida_te = f'Índice de passageiros pagantes por quilômetro em {ano_ref} = '
        elif i == 2:
            saida_te = 'TARIFA DE EQUILÍBRIO = '
            teq = locale.currency(t_eq[i])
        saida = f'{saida_te}{teq}'
        label_teq = tk.Label(Janela, text=saida)
        label_teq.grid(row=i + 15, column=0, padx=44, pady=1, stick='W')

    ct.gera_Excel()
    return

def mediaTarifa():
    mt = 0
    for i in range(len(lista_BD2)):
        if lista_BD2[i] == combo_anoAtip.get():
            d_fr = pd.DataFrame(planilha_0[lista_BD2[i]])
            mt = d_fr['tarifa'].sum() / 12
    return mt

def anoAtip_Func(event):
    label_tarifaVig = tk.Label(Janela, text=f'TARIFA VIGENTE = {locale.currency(mediaTarifa())}')
    label_tarifaVig.place(height=30, width=150, x=360, y=27)
    return


if __name__ == '__main__':
# ativa biblioteca Tkinter
    Janela = tk.Tk()
    Janela.title(f'Calcula Tarifa de Equilíbrio')

# define geometry
    largura = 550
    altura = 430
    largura_screen = Janela.winfo_screenwidth()
    altura_screen = Janela.winfo_screenheight()
    posx = (largura_screen - largura) / 2
    posy = (altura_screen - altura) / 2
    Janela.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

# importacão para o Pandas do arquivo em Excel, com planilhas separadas para cada ano
    planilha_0 = pd.read_excel('BD2.xlsx', None)
    lista_BD2 = list(planilha_0.keys())

    label_anoAtip = tk.Label(Janela, text=f'ANO ATÍPICO')
    label_anoAtip.place(height=50, width=150, x=9, y=16)
    combo_anoAtip = ttk.Combobox(Janela, values=lista_BD2, state='readonly')
    combo_anoAtip.place(height=22, width=150, x=190, y=30)
    combo_anoAtip.bind('<<ComboboxSelected>>', anoAtip_Func)
    label_anoRef = tk.Label(Janela, text=f'ANO REFERÊNCIA')
    label_anoRef.place(height=50, width=150, x=20, y=57)
    combo_anoRef = ttk.Combobox(Janela, values=lista_BD2, state='readonly')
    combo_anoRef.place(height=22, width=150, x=190, y=70)
    combo_anoRef.bind('<<ComboboxSelected>>', combo_anoRef.get())
    label_custo = tk.Label(Janela, text=f'DIFERENÇA R$/km (%)')
    label_custo.place(height=22, width=150, x=32, y=112)
    text_custo = tk.Entry(Janela)
    text_custo.place(height=22, width=40, x=190, y=110)
    cmd_Calc = tk.Button(Janela, text=f'Calcular', command=inicio)
    cmd_Calc.place(height=30, width=70, x=150, y=170)
    cmd_Fim = tk.Button(Janela, text=f'Fim', command=Janela.quit)
    cmd_Fim.place(height=30, width=70, x=330, y=170)

# mainLoop()
    Janela.mainloop()
