import pandas as pd
import numpy as np

# Carica i dati
s_out_df = pd.read_csv("s_out_i.csv", index_col=0)
Ri_df_raw = pd.read_csv("Ri_1965_2025_6specie.csv")

# Mappa ISO-2 → ISO-3
iso2_to_iso3 = {
    "DE": "DEU",
    "DK": "DNK",
    "FR": "FRA",
    "GB": "GBR",
    "NL": "NLD",
    "NO": "NOR",
    "SE": "SWE"
}
Ri_df_raw["paese"] = Ri_df_raw["paese"].map(iso2_to_iso3)

# Normalizza intestazioni delle colonne
s_out_df.columns = s_out_df.columns.astype(str)
years = [str(y) for y in range(1989, 2025)]

# Calcolo di Reff(t)
R_eff = {}
for year in years:
    s_out_year = s_out_df[year]
    Ri_year_df = Ri_df_raw[Ri_df_raw["anno"] == int(year)]
    merged = pd.merge(
        Ri_year_df,
        s_out_year.rename("s_out"),
        left_on="paese",
        right_index=True,
        how="inner"
    )
    numerator = np.sum(merged["s_out"] * merged["cpue_totale_per_haul_per_hour"])
    denominator = np.sum(merged["s_out"])
    R_eff[year] = numerator / denominator if denominator != 0 else np.nan

# Salva il risultato
R_eff_df = pd.DataFrame.from_dict(R_eff, orient='index', columns=["R_eff"])
R_eff_df.index.name = "Year"
R_eff_df.to_csv("Reff_1989_2024.csv")
