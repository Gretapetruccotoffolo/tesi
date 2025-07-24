
import pandas as pd

# === PARAMETRI BASE ===
# Lista dei 7 paesi (codici ISO-3)
paesi = ['DNK', 'DEU', 'FRA', 'GBR', 'NLD', 'NOR', 'SWE']
anno_target = 2024  # Anno per cui costruire la matrice

# === CARICAMENTO DATI ===
# Carica il dataset già unificato (1989–2024) in formato Excel o CSV
df = pd.read_excel("trade_2013_2024.xlsx")  # oppure pd.read_csv(...)

# === FILTRI ===
# Consideriamo solo: export, partner e reporter nei 7 paesi, esclusa la diagonale
df_filtrato = df[
    (df['flowCode'] == 'X') &
    (df['refYear'] == anno_target) &
    (df['reporterISO'].isin(paesi)) &
    (df['partnerISO'].isin(paesi)) &
    (df['reporterISO'] != df['partnerISO'])
].copy()

# Assicuriamoci che netWgt sia numerico
df_filtrato['netWgt'] = pd.to_numeric(df_filtrato['netWgt'], errors='coerce')

# === COSTRUZIONE MATRICE Cij ===
# Riga = importatore (i), Colonna = esportatore (j)
C = pd.DataFrame(0.0, index=paesi, columns=paesi)

# Raggruppamento per coppia (importatore, esportatore)
gruppato = df_filtrato.groupby(['partnerISO', 'reporterISO'])['netWgt'].sum().reset_index()

# Riempimento della matrice
for _, row in gruppato.iterrows():
    importatore = row['partnerISO']
    esportatore = row['reporterISO']
    peso_kg = row['netWgt']
    C.loc[importatore, esportatore] = peso_kg

# === RISULTATO ===
print(f"Matrice Cij per l'anno {anno_target} (in kg):\n")
print(C)
