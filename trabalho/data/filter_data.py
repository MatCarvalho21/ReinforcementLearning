# import pandas as pd 

# dataframe = pd.read_excel('./models/data/final_data.xlsx', index_col=0)  
# df = dataframe[dataframe["Nome Competição"] == "Semaine Olympique Francaise De Voile 2022"]
# df = df[df["Classe Vela"] == "49ER"].sort_values(by="Posição Geral", ascending=True)

# df_final = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final["Name"] = df["Nome Competidor"].unique()
# df_final["Position"] = df_final.index + 1
# df_final["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final["Classe"] = "49ER"
# df_final.to_csv("./models/data/SOFDV_2022_49ER_FILTERED.csv", index=False)

# df_filtered = dataframe[dataframe["Nome Competição"] == "Semaine Olympique Francaise De Voile 2022"]
# df_filtered_1 = df_filtered[df_filtered["Classe Vela"] == "FORMULA KITE FEM."].sort_values(by="Posição Geral", ascending=True)
# df_filtered_2 = df_filtered[df_filtered["Classe Vela"] == "FORMULA KITE MASC."].sort_values(by="Posição Geral", ascending=True)
# df_filtered_3 = df_filtered[df_filtered["Classe Vela"] == "IQFOIL FEM."].sort_values(by="Posição Geral", ascending=True)
# df_filtered_4 = df_filtered[df_filtered["Classe Vela"] == "470"].sort_values(by="Posição Geral", ascending=True)
# df_filtered_5 = df_filtered[df_filtered["Classe Vela"] == "ILCA 6"].sort_values(by="Posição Geral", ascending=True)

# df_final_1 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_1["Name"] = df_filtered_1["Nome Competidor"].unique()
# df_final_1["Position"] = df_final_1.index + 1
# df_final_1["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_1["Classe"] = "FORMULA KITE FEM."

# df_final_2 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_2["Name"] = df_filtered_2["Nome Competidor"].unique()
# df_final_2["Position"] = df_final_2.index + 1
# df_final_2["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_2["Classe"] = "FORMULA KITE MASC."

# df_final_3 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_3["Name"] = df_filtered_3["Nome Competidor"].unique()
# df_final_3["Position"] = df_final_3.index + 1
# df_final_3["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_3["Classe"] = "IQFOIL FEM."

# df_final_4 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_4["Name"] = df_filtered_4["Nome Competidor"].unique()
# df_final_4["Position"] = df_final_4.index + 1
# df_final_4["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_4["Classe"] = "470"

# df_final_5 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_5["Name"] = df_filtered_5["Nome Competidor"].unique()
# df_final_5["Position"] = df_final_5.index + 1
# df_final_5["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_5["Classe"] = "ILCA 6"

# df_filtered_6 = dataframe[dataframe["Nome Competição"] == "World Championship 2019"]
# df_filtered_6 = df_filtered_6[df_filtered_6["Classe Vela"] == "49ER"].sort_values(by="Posição Geral", ascending=True)
# df_final_6 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_6["Name"] = df_filtered_6["Nome Competidor"].unique()
# df_final_6["Position"] = df_final_6.index + 1
# df_final_6["Competicao"] = "World Championship 2019"
# df_final_6["Classe"] = "49ER"

# df_filtered_7 = dataframe[dataframe["Nome Competição"] == "Trofeo S.A.R Princesa Sofia 2023"]
# df_filtered_7 = df_filtered_7[df_filtered_7["Classe Vela"] == "NACRA 17"].sort_values(by="Posição Geral", ascending=True)
# df_final_7 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_7["Name"] = df_filtered_7["Nome Competidor"].unique()
# df_final_7["Position"] = df_final_7.index + 1
# df_final_7["Competicao"] = "Trofeo S.A.R Princesa Sofia 2023"
# df_final_7["Classe"] = "NACRA 17"

# final_dataframe = pd.concat([df_final, df_final_1, df_final_2, df_final_3, df_final_4, df_final_5, df_final_6, df_final_7])
# final_dataframe.to_csv("./models/data/GOLDEN_DATA.csv", index=False) 

# df1 = pd.read_csv("./models/data/Semaine Olympique Francaise De Voile 2022 49ERFX.CSV", low_memory=False, sep=";").sort_values(by="Position", ascending=True)
# df2 = pd.read_csv("./models/data/Semaine Olympique Francaise De Voile 2022 FORMULA KITE FEM..csv", low_memory=False).sort_values(by="Position", ascending=True)
# df3 = pd.read_csv("./models/data/Semaine Olympique Francaise De Voile 2022 FORMULA KITE MASC..csv", low_memory=False).sort_values(by="Position", ascending=True)
# df4 = pd.read_csv("./models/data/Semaine Olympique Francaise De Voile 2022 IQFOIL FEM..csv", low_memory=False, sep=";").sort_values(by="Position", ascending=True)
# df5 = pd.read_csv("./models/data/SemaineOlympiqueFrancaiseDeVoile2022_470.csv", low_memory=False).sort_values(by="Position", ascending=True)
# df6 = pd.read_csv("./models/data/SemaineOlympiqueFrancaiseDeVoile2022_ilca6.csv", low_memory=False).sort_values(by="Position", ascending=True)
# df7 = pd.read_csv("./models/data/World Championship 2019_49er.csv", low_memory=False).sort_values(by="Position", ascending=True)
# df8 = pd.read_csv("./models/data/Trofeo S.A.R Princesa Sofia 2023 NACRA 17.CSV", low_memory=False, sep=";").sort_values(by="Position", ascending=True)

# df_final_1 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_1["Name"] = df1["Name"].unique()
# df_final_1["Position"] = df_final_1.index + 1
# df_final_1["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_1["Classe"] = "49ERFX"

# df_final_2 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_2["Name"] = df2["Name"].unique()
# df_final_2["Position"] = df_final_2.index + 1
# df_final_2["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_2["Classe"] = "FORMULA KITE FEM."

# df_final_3 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_3["Name"] = df3["Name"].unique()
# df_final_3["Position"] = df_final_3.index + 1
# df_final_3["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_3["Classe"] = "FORMULA KITE MASC."

# df_final_4 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_4["Name"] = df4["Name"].unique()
# df_final_4["Position"] = df_final_4.index + 1
# df_final_4["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_4["Classe"] = "IQFOIL FEM."

# df_final_5 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_5["Name"] = df5["Name"].unique()
# df_final_5["Position"] = df_final_5.index + 1
# df_final_5["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_5["Classe"] = "470"

# df_final_6 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_6["Name"] = df6["Name"].unique()
# df_final_6["Position"] = df_final_6.index + 1
# df_final_6["Competicao"] = "Semaine Olympique Francaise De Voile 2022"
# df_final_6["Classe"] = "ILCA 6"

# df_final_7 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_7["Name"] = df7["Name"].unique()
# df_final_7["Position"] = df_final_7.index + 1
# df_final_7["Competicao"] = "World Championship 2019"
# df_final_7["Classe"] = "49ER"

# df_final_8 = pd.DataFrame(columns=["Position", "Name", "Competicao", "Classe"])
# df_final_8["Name"] = df8["Name"].unique()
# df_final_8["Position"] = df_final_8.index + 1
# df_final_8["Competicao"] = "Trofeo S.A.R Princesa Sofia 2023"
# df_final_8["Classe"] = "NACRA 17"

# final_dataframe = pd.concat([df_final_1, df_final_2, df_final_3, df_final_4, df_final_5, df_final_6, df_final_7, df_final_8])
# final_dataframe.to_csv("./models/data/raw_data.csv", index=False)
