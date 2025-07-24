
import pandas as pd

# Carica la matrice C_ij in kg per un anno (esempio 2024)
df = pd.read_excel("matrici_Cij_kg_1989_2024.xlsx", sheet_name="2024", index_col=0)

# Passaggio 1: selezioniamo solo il 19.2% del totale (quota stimata delle 6 specie)
df_6specie = df * 0.192

# Passaggio 2: Peso medio ponderato di un individuo (in kg), calcolato in precedenza
peso_medio_kg = 1.004652239705463

# Passaggio 3: Conversione da kg a numero di individui
df_individui = df_6specie / peso_medio_kg

# Salvataggio della matrice convertita
df_individui.to_excel("matrice_Cij_individui_2024.xlsx")
