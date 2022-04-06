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
        # diferenca_km = total_2020_km / total_2019_km
        # diferenca_pax = total_2020_pax / total_2019_pax

        custo_atual = self.tarifa_vigente * self.calcula_ipk_2019()
        custo_novo = custo_atual * (1 + self.perda_custo)

        self.tarifa_equilibrio = custo_novo / self.calcula_ipk_2020()

        return self.tarifa_equilibrio, self.calcula_ipk_2019(), self.calcula_ipk_2020()


if __name__ == '__main__':
    tarif_vig = 4.05
    perda_custo = -3.0549 / 100

    bd_xlsx = pd.read_excel('BD.xlsx')
    df = pd.DataFrame(bd_xlsx)

    ct = CalculaTarifa(tarif_vig, perda_custo, df)

    ct.soma_excel()
    # print()
    # print(f'KM 2019 = {total_2019_km}')
    # print(f'KM 2020 = {total_2020_km}')
    # print()
    # print(f'PAX 2019 = {total_2019_pax}')
    # print(f'PAX 2020 = {total_2020_pax}')
    #
    # te = ct.tarifa_equivalente()
    #
    # print()
    # print(f'IPK 2019 = {ipk_2019}')
    # print(f'IPK 2020 = {ipk_2020}')
    # print()
    # print(f'TARIFA DE EQUILÍBRIO = {tarifa_equilibrio}')
