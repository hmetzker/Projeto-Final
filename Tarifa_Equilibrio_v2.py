# calcula a tarifa de equilíbrio em função da variação (perda ou ganho) entre dois períodos distintos


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CalculaTarifa:

    def __init__(self, tarifa_vigente, perda_custo, df1, df2):
# variáveis de entrada
        self.tarifa_vigente = tarifa_vigente                # tarifa praticada vigente
        self.perda_custo = np.float64(perda_custo) / 100    # perda pela retirada de veículos da frota de ônibus
        self.df1 = df1                                      # dataFrame referente ao ano atípico
        self.df2 = df2                                      # dataFrame referente ao ano de referência
# variáveis de saída
        self.total_ano_anterior_km = 0
        self.total_ano_anterior_pax = 0
        self.total_ano_atipico_km = 0
        self.total_ano_atipico_pax = 0
        self.tarifa_equilibrio = 0
        self.geraExcel = ''

# totais do ano atípico e do ano de referência (oferta/ demanda de pax de acordo com o planejamento)
    def soma_excel(self):
        self.total_ano_anterior_km = self.df2['km coberto'].sum()
        self.total_ano_atipico_km = self.df1['km coberto'].sum()
        self.total_ano_anterior_pax = self.df2['pax pagantes'].sum()
        self.total_ano_atipico_pax = self.df1['pax pagantes'].sum()
        return self.total_ano_anterior_km, self.total_ano_anterior_pax, self.total_ano_atipico_km, self.total_ano_atipico_pax

# calculo do IPK de pax pagantes do ano de referência (oferta/ demanda de pax de acordo com o planejamento)
    def calcula_ipk_ano_anterior(self):
        return self.total_ano_anterior_pax / self.total_ano_anterior_km

# calculo do IPK de pax pagantes do ano atípico (ano de queda de oferta/ demanda de pax)
    def calcula_ipk_ano_atipico(self):
        return self.total_ano_atipico_pax / self.total_ano_atipico_km

# tarifa calculada em função da queda de oferta/ demanda de pax (manutenção do equilíbrio econômico-financeiro)
    def tarifa_equilibrada(self):
        custo_atual = np.float64(self.tarifa_vigente) * self.calcula_ipk_ano_anterior()
        custo_novo = custo_atual * (1 - (self.total_ano_atipico_km / self.total_ano_anterior_km * self.perda_custo))
        self.tarifa_equilibrio = custo_novo / self.calcula_ipk_ano_atipico()
        return self.calcula_ipk_ano_anterior(), self.calcula_ipk_ano_atipico(), self.tarifa_equilibrio

# mostrando gráfico de barras, com index modificado
    def mostra_grafico(self):
        self.geraExcel = pd.DataFrame({'valor': [np.float64(self.tarifa_vigente), np.float64(self.tarifa_equilibrio)]}, index=['T-vig', 'T-eq'])
        self.geraExcel['valor'].plot.barh()
        return plt.show()

# gerando arquivo BD3.xlsx com as tarifas vigente e de equilíbrio
    def gera_Excel(self):
        return self.geraExcel.to_excel('BD3.xlsx')


if __name__ == '__main__':
    ano_atip = 0
    ano_ref = 1
    primeiraVez = False
    while ano_atip <= ano_ref:
        if primeiraVez:
            print()
            print('Ano atípico deve ser maior do que o ano de referência...')
            print()

        primeiraVez = True
        ano_atip = input("ANO ATÍPICO = ")
        ano_ref = input("ANO DE REFERÊNCIA = ")

# ano atípico e/ou de referência fora dos limites (entre 2015 e 2021). Nesse caso, os valores serão corrigidos
# pelos limites inferior (2015) e/ou superior (2021).
# A próxima evolução será identificar automaticamente os limites inferior e superior, sem precisar fixá-los no código

        if ano_atip > '2021':
            ano_atip = '2021'
        if ano_ref < '2015':
            ano_ref = '2015'
    else:
        perda_oferta = input("DIMINUIÇÃO DE CUSTO OPERACIONAL (%) = ")
        tarifa_vig = input("TARIFA VIGENTE = ")
        print()

# arquivo em Excel com planilhas separadas para cada ano de 2015 até 2021
# planilha_1 guarda as informações do ano atípico (queda de oferta/ demanda de pax)
# planilha_2 guarda as informações do ano de referência quanto a oferta/ demanda de pax

        planilha_1 = pd.read_excel('BD2.xlsx', sheet_name = ano_atip, index_col = 0)
        planilha_2 = pd.read_excel('BD2.xlsx', sheet_name = ano_ref, index_col = 0)
        d_fr1 = pd.DataFrame(planilha_1)
        d_fr2 = pd.DataFrame(planilha_2)
        ct = CalculaTarifa(tarifa_vig, perda_oferta, d_fr1, d_fr2)
        total = ct.soma_excel()
        for i in range(0, len(total), 2):
            saida_km = f'KM {ano_atip} = '
            saida_pax = f'PAX {ano_atip} = '
            if i == 0:
                saida_km = f'KM {ano_ref} = '
                saida_pax = f'PAX {ano_ref} = '
            print(f'{saida_km}{total[i]}')
            print(f'{saida_pax}{total[i + 1]}')
        t_eq = ct.tarifa_equilibrada()
        for i in range(len(t_eq)):
            saida_te = f'IPK {ano_atip} = '
            if i == 0:
                saida_te = f'IPK {ano_ref} = '
            elif i == 2:
                saida_te = 'TARIFA DE EQUILÍBRIO = '
            print(f'{saida_te}{t_eq[i]}')

    ct.mostra_grafico()
    ct.gera_Excel()
