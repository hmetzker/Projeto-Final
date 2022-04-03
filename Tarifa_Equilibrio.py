import pandas as pd

class Calcula_tarifa():

    def __init__(self, tarifa_vigente, perda_custo, df):
        self.tarifa_vigente = tarifa_vigente
        self.perda_custo = perda_custo
        self.df = df

    def soma_excel(self):
        global total_2019_km
        global total_2019_pax
        global total_2020_km
        global total_2020_pax

        total_2019_km = 0
        total_2019_pax = 0
        total_2020_km = 0
        total_2020_pax = 0

        for i in range(self.df['ano'].count()):
            if self.df['ano'].values[i] == 2019:
                total_2019_km = total_2019_km + self.df['km coberto'].values[i]
                total_2019_pax = total_2019_pax + self.df['pax pagantes'].values[i]
            else:
                total_2020_km = total_2020_km + self.df['km coberto'].values[i]
                total_2020_pax = total_2020_pax + self.df['pax pagantes'].values[i]



        return total_2019_km, total_2019_pax, total_2020_km, total_2020_pax

    def tarifa_equivalente(self):
        global ipk_2019
        global ipk_2020
        global tarifa_equilibrio

        ipk_2019 = total_2019_pax / total_2019_km
        ipk_2020 = total_2020_pax / total_2020_km

        diferenca_km = total_2020_km / total_2019_km
        diferenca_pax = total_2020_pax / total_2019_pax

        custo_atual = self.tarifa_vigente * ipk_2019
        custo_novo = custo_atual * (1 + self.perda_custo)

        tarifa_equilibrio = custo_novo / ipk_2020

        return tarifa_equilibrio, ipk_2019, ipk_2020

if __name__ == '__main__':
    tarifa_vigente = 4.05
    perda_custo = -3.0549 / 100

    bd_xlsx = pd.read_excel('BD.xlsx')
    df = pd.DataFrame(bd_xlsx)

    ct = Calcula_tarifa(tarifa_vigente, perda_custo, df)

    ct.soma_excel()
    print()
    print(f'KM 2019 = {total_2019_km}')
    print(f'KM 2020 = {total_2020_km}')
    print()
    print(f'PAX 2019 = {total_2019_pax}')
    print(f'PAX 2020 = {total_2020_pax}')

    te = ct.tarifa_equivalente()

    print()
    print(f'IPK 2019 = {ipk_2019}')
    print(f'IPK 2020 = {ipk_2020}')
    print()
    print(f'TARIFA DE EQUILÍBRIO = {tarifa_equilibrio}')
