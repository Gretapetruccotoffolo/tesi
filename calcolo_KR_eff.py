import pandas as pd

# Carica il file KRi
df = pd.read_csv("KRi.csv")

# Estrai il valore massimo dalla colonna Ri_massimo_storico
KRmax = df["Ri_massimo_storico"].max()

# Crea un DataFrame con intestazione KReff e valore sotto
pd.DataFrame({"KReff": [round(KRmax, 2)]}).to_csv("KReff.csv", index=False)
