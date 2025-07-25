import pandas as pd
import numpy as np

# Carica i dati
s_out_df = pd.read_csv("s_out_i.csv", index_col=0)
s_in_df = pd.read_csv("s_in_i.csv", index_col=0)

# Uniforma intestazioni
s_out_df.columns = s_out_df.columns.astype(str)
s_in_df.columns = s_in_df.columns.astype(str)

# Anni da considerare
years = [str(y) for y in range(1989, 2025)]

# Calcolo eta_eff(t)
eta_eff = {}
for year in years:
    s_out = s_out_df[year]
    s_in = s_in_df[year]
    weights = s_out
    denom = np.sum(weights)
    L_sin = np.sum(weights * s_in) / denom if denom != 0 else np.nan
    L_sout = np.sum(weights * s_out) / denom if denom != 0 else np.nan
    eta_eff[year] = L_sin - L_sout

# Salva i risultati
eta_eff_df = pd.DataFrame.from_dict(eta_eff, orient='index', columns=["eta_eff"])
eta_eff_df.index.name = "Year"
eta_eff_df.to_csv("eta_eff_1989_2024.csv")
