import pandas as pd
import numpy as np


class CalculaTarifa:

    def __init__(self, ano_atipico, tarifa_vigente, perda_custo, df):
        self.tarifa_vigente = tarifa_vigente    # tarifa praticada vigente
        self.ano_atipico = ano_atipico          # ano de queda de oferta/ demanda
        self.perda_custo = perda_custo          # perda pela retirada de veículos da frota de ônibus
        self.df = df
        self.total_ano_anterior_km = 0
        self.total_ano_anterior_pax = 0
        self.total_ano_atipico_km = 0
        self.total_ano_atipico_pax = 0
        self.tarifa_equilibrio = 0

    # totais do ano atípico e do ano de referência (oferta/ demanda de acordo com o planejamento)
    def soma_excel(self):
        for i in range(self.df['ano'].count()):
            if self.df['ano'].values[i] == int(self.ano_atipico) - 1:
                self.total_ano_anterior_km = self.total_ano_anterior_km + self.df['km coberto'].values[i]
                self.total_ano_anterior_pax = self.total_ano_anterior_pax + self.df['pax pagantes'].values[i]
            else:
                self.total_ano_atipico_km = self.total_ano_atipico_km + self.df['km coberto'].values[i]
                self.total_ano_atipico_pax = self.total_ano_atipico_pax + self.df['pax pagantes'].values[i]
        return self.total_ano_anterior_km, self.total_ano_anterior_pax, self.total_ano_atipico_km, self.total_ano_atipico_pax

    # calculo do IPK de pax pagantes do ano de referência (oferta/ demanda de acordo com o planejamento)
    def calcula_ipk_ano_anterior(self):
        return self.total_ano_anterior_pax / self.total_ano_anterior_km

    # calculo do IPK de pax pagantes do ano atípico (ano de queda de oferta/ demanda)
    def calcula_ipk_ano_atipico(self):
        return self.total_ano_atipico_pax / self.total_ano_atipico_km

    # tarifa calculada em função da queda de oferta/ demanda (manutenção do equilíbrio econômico-financeiro)
    def tarifa_equilibrada(self):
        custo_atual = np.float64(self.tarifa_vigente) * self.calcula_ipk_ano_anterior()
        custo_novo = custo_atual * (1 + self.perda_custo)
        self.tarifa_equilibrio = custo_novo / self.calcula_ipk_ano_atipico()
        return self.calcula_ipk_ano_anterior(), self.calcula_ipk_ano_atipico(), self.tarifa_equilibrio


if __name__ == '__main__':
    ano_atip = input("ANO ATÍPICO = ")
    tarifa_vig = input("TARIFA VIGENTE = ")
    perda_oferta = -3.0549 / 100
    bd_xlsx = pd.read_excel('BD.xlsx')
    d_fr = pd.DataFrame(bd_xlsx)
    ct = CalculaTarifa(ano_atip, tarifa_vig, perda_oferta, d_fr)
    total = ct.soma_excel()
    for i in range(0, len(total), 2):
        saida_km = f'KM {ano_atip} = '
        saida_pax = f'PAX {ano_atip} = '
        if i == 0:
            saida_km = f'KM {int(ano_atip) - 1} = '
            saida_pax = f'PAX {int(ano_atip) - 1} = '
        print(f'{saida_km}{total[i]}')
        print(f'{saida_pax}{total[i + 1]}')

    t_eq = ct.tarifa_equilibrada()
    for i in range(len(t_eq)):
        saida_te = f'IPK {ano_atip} = '
        if i == 0:
            saida_te = f'IPK {int(ano_atip) - 1} = '
        elif i == 2:
            saida_te = 'TARIFA DE EQUILÍBRIO = '
        print(f'{saida_te}{t_eq[i]}')
