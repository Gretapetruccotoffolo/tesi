import pandas as pd

# Carica il file CSV
df = pd.read_csv('sample_CPUE_recent.csv')

# Rimuove eventuali spazi nelle intestazioni delle colonne
df.columns = df.columns.str.strip()

# Filtra i valori validi di cpue_hph (esclude -9 e valori nulli)
df = df[df['cpue_hph'].apply(lambda x: isinstance(x, (int, float))) | df['cpue_hph'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]
df['cpue_hph'] = pd.to_numeric(df['cpue_hph'], errors='coerce')
df = df[df['cpue_hph'] != -9]
df = df.dropna(subset=['cpue_hph'])

# Calcola la media dei cpue_hph per anno, paese, specie
media_per_specie = (
    df.groupby(['anno', 'paese', 'specie'])['cpue_hph']
    .mean()
    .reset_index()
)

# Somma le medie delle specie per ogni anno e paese
media_totale = (
    media_per_specie.groupby(['anno', 'paese'])['cpue_hph']
    .sum()
    .reset_index()
    .rename(columns={'cpue_hph': 'cpue_per_haul_per_hour_tot_medio'})
)

# Arrotonda a 3 decimali
media_totale['cpue_per_haul_per_hour_tot_medio'] = media_totale['cpue_per_haul_per_hour_tot_medio'].round(3)

# Salva il risultato in un nuovo CSV
media_totale.to_csv('cpue_paese_anno_totmedio.csv', index=False)