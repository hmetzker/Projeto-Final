import pandas as pd
import numpy as np


class CalculaTarifa:

    def __init__(self, ano_atipico, tarifa_vigente, perda_custo, df):
        self.tarifa_vigente = tarifa_vigente
        self.ano_atipico = ano_atipico
        self.perda_custo = perda_custo
        self.df = df
        self.total_ano_anterior_km = 0
        self.total_ano_anterior_pax = 0
        self.total_ano_atipico_km = 0
        self.total_ano_atipico_pax = 0
        self.tarifa_equilibrio = 0

    def soma_excel(self):
        for i in range(self.df['ano'].count()):
            if self.df['ano'].values[i] == int(self.ano_atipico) - 1:
                self.total_ano_anterior_km = self.total_ano_anterior_km + self.df['km coberto'].values[i]
                self.total_ano_anterior_pax = self.total_ano_anterior_pax + self.df['pax pagantes'].values[i]
            else:
                self.total_ano_atipico_km = self.total_ano_atipico_km + self.df['km coberto'].values[i]
                self.total_ano_atipico_pax = self.total_ano_atipico_pax + self.df['pax pagantes'].values[i]
        return self.total_ano_anterior_km, self.total_ano_anterior_pax, self.total_ano_atipico_km, self.total_ano_atipico_pax

    def calcula_ipk_ano_anterior(self):
        return self.total_ano_anterior_pax / self.total_ano_anterior_km

    def calcula_ipk_ano_atipico(self):
        return self.total_ano_atipico_pax / self.total_ano_atipico_km

    def tarifa_equivalente(self):
        custo_atual = np.float64(self.tarifa_vigente) * self.calcula_ipk_ano_anterior()
        custo_novo = custo_atual * (1 + self.perda_custo)
        self.tarifa_equilibrio = custo_novo / self.calcula_ipk_ano_atipico()
        return self.calcula_ipk_ano_anterior(), self.calcula_ipk_ano_atipico(), self.tarifa_equilibrio


if __name__ == '__main__':
    ano_atp = input("ANO ATÍPICO = ")
    tarifa_vig = input("TARIFA VIGENTE = ")
    perda_oferta = -3.0549 / 100
    bd_xlsx = pd.read_excel('BD.xlsx')
    d_fr = pd.DataFrame(bd_xlsx)
    ct = CalculaTarifa(ano_atp, tarifa_vig, perda_oferta, d_fr)
    total = ct.soma_excel()
    for i in range(0, len(total), 2):
        saida_km = f'KM {ano_atp} = '
        saida_pax = f'PAX {ano_atp} = '
        if i == 0:
            saida_km = f'KM {int(ano_atp) - 1} = '
            saida_pax = f'PAX {int(ano_atp) - 1} = '
        print(f'{saida_km}{total[i]}')
        print(f'{saida_pax}{total[i + 1]}')

    t_eq = ct.tarifa_equivalente()
    for i in range(len(t_eq)):
        saida_te = f'IPK {ano_atp} = '
        if i == 0:
            saida_te = f'IPK {int(ano_atp) - 1} = '
        elif i == 2:
            saida_te = 'TARIFA DE EQUILÍBRIO = '
        print(f'{saida_te}{t_eq[i]}')
