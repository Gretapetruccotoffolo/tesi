import pandas as pd
import numpy as np

# Mappa da nome completo a codice ISO-3
name_to_iso3 = {
    "Germany": "DEU",
    "Denmark": "DNK",
    "France": "FRA",
    "United Kingdom": "GBR",
    "Netherlands": "NLD",
    "Norway": "NOR",
    "Sweden": "SWE"
}

# Carica i dati
dieta_df = pd.read_csv("di(t).csv")
popolazione_df = pd.read_csv("popolazione_1960_2025.csv")
s_out_df = pd.read_csv("s_out_i.csv", index_col=0)
s_out_df.columns = s_out_df.columns.astype(str)

# Applica mappatura
dieta_df["Entity"] = dieta_df["Entity"].map(name_to_iso3)
popolazione_df["Entity"] = popolazione_df["Entity"].map(name_to_iso3)

# Rinomina colonne
dieta_df = dieta_df.rename(columns={"Entity": "paese", "Year": "anno", "Consumo_kg_procapite": "dieta"})
popolazione_df = popolazione_df.rename(columns={"Entity": "paese", "Year": "anno", "Population (historical)": "popolazione"})

# Calcolo c_eff(t)
years = [str(y) for y in range(1989, 2025)]
c_eff = {}

for year in years:
    d_year = dieta_df[dieta_df["anno"] == int(year)]
    L_year = popolazione_df[popolazione_df["anno"] == int(year)]
    s_out_year = s_out_df[year]

    merged = pd.merge(d_year, L_year, on=["paese", "anno"], how="inner")
    merged = pd.merge(merged, s_out_year.rename("s_out"), left_on="paese", right_index=True, how="inner")

    merged["term"] = merged["dieta"] * merged["popolazione"]
    numerator = np.sum(merged["s_out"] * merged["term"])
    denominator = np.sum(merged["s_out"])
    c_eff[year] = numerator / denominator if denominator != 0 else np.nan

# Salva il risultato
c_eff_df = pd.DataFrame.from_dict(c_eff, orient='index', columns=["c_eff"])
c_eff_df.index.name = "Year"
c_eff_df.to_csv("c_eff_1989_2024.csv")
