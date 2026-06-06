from services.auth import get_access_token
from services.pesquisa import pesquisa
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
tokens = get_access_token()

planilha = pd.read_csv("canhotos.csv", sep=";", encoding="latin-1")  

for linha in planilha.index:
    nota = int(planilha.loc[linha, "NF"])
    nota_certa = f"{nota}.0"

    resultado_pesquisa = pesquisa(nota_certa, tokens["access_token"])

    if resultado_pesquisa["itens_totais"] == 0:
        planilha.loc[linha, "Status"] = "NÃO ENCONTRADA"
    else:
        planilha.loc[linha, "Status"] = resultado_pesquisa["itens"][0]["status_traduzido"]

planilha.to_csv("canhotos_resultado.csv", index=False)

print("Processamento concluído. Verifique o arquivo 'canhotos_resultado.csv' para os resultados.")
