
import pandas as pd


# === STEP 1: Carica le matrici Cij (in individui) ===
xls = pd.ExcelFile("matrici_Cij_individui_1989_2024.xlsx")
anni = xls.sheet_names

# === STEP 2: Carica dati di popolazione ===
df_pop = pd.read_csv("popolazione_1960_2025.csv")
df_pop = df_pop.rename(columns={
    "Entity": "Paese",
    "Year": "Anno",
    "Population (historical)": "Popolazione"
})

# === STEP 3: Definizione paesi ===
iso_to_nome = {
    "DNK": "Denmark",
    "DEU": "Germany",
    "FRA": "France",
    "GBR": "United Kingdom",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "SWE": "Sweden"
}

# === STEP 4: Filtra la popolazione per i paesi e anni corretti ===
df_pop = df_pop[df_pop["Paese"].isin(iso_to_nome.values()) & df_pop["Anno"].isin(map(int, anni))]
pop_dict = {
    str(anno): df_pop[df_pop["Anno"] == int(anno)].set_index("Paese")["Popolazione"]
    for anno in anni
}

# === STEP 5: Calcolo di s_out_i(t) = somma_j≠i [ C_ji(t) * L_j(t) ] ===
s_out = []
for anno in anni:
    C = xls.parse(anno, index_col=0)
    L = pop_dict[anno]
    s_out_anno = {}
    for i_iso in iso_to_nome:
        i_nome = iso_to_nome[i_iso]
        somma = sum(C.loc[j_iso, i_iso] * L[iso_to_nome[j_iso]] for j_iso in iso_to_nome if j_iso != i_iso)
        s_out_anno[i_iso] = somma
    df_sout_anno = pd.DataFrame.from_dict(s_out_anno, orient='index', columns=[int(anno)])
    s_out.append(df_sout_anno)

# === STEP 6: Unisci i risultati e salva ===
df_sout = pd.concat(s_out, axis=1).sort_index()
df_sout.to_csv("s_out_i_per_tempo.csv")
