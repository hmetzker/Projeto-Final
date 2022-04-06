import pandas as pd


class CalculaTarifa:

    def __init__(self, tarifa_vigente, perda_custo, df):
        self.tarifa_vigente = tarifa_vigente
        self.perda_custo = perda_custo
        self.df = df
        self.total_2019_km = 0
        self.total_2019_pax = 0
        self.total_2020_km = 0
        self.total_2020_pax = 0
        self.tarifa_equilibrio = 0

    def soma_excel(self):
        for i in range(self.df['ano'].count()):
            if self.df['ano'].values[i] == 2019:
                self.total_2019_km = self.total_2019_km + self.df['km coberto'].values[i]
                self.total_2019_pax = self.total_2019_pax + self.df['pax pagantes'].values[i]
            else:
                self.total_2020_km = self.total_2020_km + self.df['km coberto'].values[i]
                self.total_2020_pax = self.total_2020_pax + self.df['pax pagantes'].values[i]
        return self.total_2019_km, self.total_2019_pax, self.total_2020_km, self.total_2020_pax

    def calcula_ipk_2019(self):
        return self.total_2019_pax / self.total_2019_km

    def calcula_ipk_2020(self):
        return self.total_2020_pax / self.total_2020_km

    def tarifa_equivalente(self):
        custo_atual = self.tarifa_vigente * self.calcula_ipk_2019()
        custo_novo = custo_atual * (1 + self.perda_custo)
        self.tarifa_equilibrio = custo_novo / self.calcula_ipk_2020()
        return self.calcula_ipk_2019(), self.calcula_ipk_2020(), self.tarifa_equilibrio


if __name__ == '__main__':
    tarifa_vig = 4.05
    perda_oferta = -3.0549 / 100
    bd_xlsx = pd.read_excel('BD.xlsx')
    d_fr = pd.DataFrame(bd_xlsx)
    ct = CalculaTarifa(tarifa_vig, perda_oferta, d_fr)
    total = ct.soma_excel()
    for i in range(0, len(total), 2):
        saida_km = 'KM 2020 = '
        saida_pax = 'PAX 2020 = '
        if i == 0:
            saida_km = 'KM 2019 = '
            saida_pax = 'PAX 2019 = '
        print(f'{saida_km}{total[i]}')
        print(f'{saida_pax}{total[i + 1]}')

    t_eq = ct.tarifa_equivalente()
    for i in range(len(t_eq)):
        saida_te = 'IPK 2020 = '
        if i == 0:
            saida_te = 'IPK 2019 = '
        elif i == 2:
            saida_te = 'TARIFA DE EQUILÍBRIO = '
        print(f'{saida_te}{t_eq[i]}')
