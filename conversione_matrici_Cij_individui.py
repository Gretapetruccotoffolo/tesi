
import pandas as pd

# Carica la matrice C_ij in kg per un anno (esempio 2024)
df = pd.read_excel("matrici_Cij_kg_1989_2024.xlsx", sheet_name="2024", index_col=0)

# Peso medio ponderato di un individuo (in kg), calcolato in precedenza
peso_medio_kg = 1.004652239705463

# Conversione da kg a numero di individui
df_individui = df / peso_medio_kg

# Salvataggio della matrice convertita
df_individui.to_excel("matrice_Cij_individui_2024.xlsx")
