import pandas as pd

# 1. Carica il file CPUE
df = pd.read_csv("CPUE.csv")

# 2. Uniforma 'GB-SCT' a 'GB'
df['Country'] = df['Country'].replace({'GB-SCT': 'GB'})

# 3. Converte CPUE_number_per_hour in numerico (interpreta il punto come decimale)
df['CPUE_number_per_hour'] = pd.to_numeric(df['CPUE_number_per_hour'], errors='coerce')

# 4. Somma del CPUE per ogni haul (fissato Year, Country, HaulNo)
#    cioè: somma su tutte le righe con stessa haul, specie, lngtClass
haul_cpue = (
    df
    .groupby(['Country', 'Year', 'HaulNo'])['CPUE_number_per_hour']
    .sum()
    .reset_index(name='CPUE_sum_per_haul')
)

# 5. Media del CPUE per haul per ogni Country e Year
ri = (
    haul_cpue
    .groupby(['Country', 'Year'])['CPUE_sum_per_haul']
    .mean()
    .reset_index(name='Ri')
)

# 6. (Opzionale) Salva il risultato su file
ri.to_csv("Ri_calcolato.csv", index=False)

# 7. Mostra le prime righe
print(ri.head())
