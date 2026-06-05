from services.auth import get_access_token
from services.pesquisa import pesquisa
from services.baixa import dar_baixa
from dotenv import load_dotenv
import os

import pandas as pd

load_dotenv()
conta_financeira = os.getenv("ID_ITAU") or os.getenv("ID_SICOOB")

tokens = get_access_token()
planilha = pd.read_excel("elasa02.xlsx")

data_pagamento = input("Digite a data de pagamento (formato YYYY-MM-DD): ")
id_conta_financeira = input("Nome da conta financeira (itau ou sicoob): ")

if id_conta_financeira.lower() == "itau":
    conta_financeira = os.getenv("ID_ITAU")
elif id_conta_financeira.lower() == "sicoob":
    conta_financeira = os.getenv("ID_SICOOB")

for linha in planilha.index:
    nota = int(planilha.loc[linha, "Nota"])
    nota_certa = f"{nota}.0"
    valor_texto = str(planilha.loc[linha, "Valor"]).strip()
    
    # Remove "R$" e espaços, depois converte vírgula em ponto
    valor_limpo = valor_texto.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")

    try:
        valor = float(valor_limpo)
    except ValueError:
        print(f"Erro ao converter valor para nota {nota_certa}: {valor_texto}")
        continue

    resultado_pesquisa = pesquisa(nota_certa, tokens["access_token"])


    if resultado_pesquisa["itens_totais"] == 0:
        print(f"Nota {nota_certa} não encontrada.")
        continue

    parcela_id = resultado_pesquisa["itens"][0]["id"]

    resposta_baixa = dar_baixa(
        parcela_id, 
        valor, 
        data_pagamento,
        conta_financeira,
        tokens["access_token"]
    )

    if resposta_baixa.status_code == 200:
        print(f"✓ Nota {nota_certa} baixada com sucesso!")
    else:
        print(f"✗ Erro ao baixar nota {nota_certa}: {resposta_baixa.status_code}")
        print(f"  Resposta: {resposta_baixa.text}")

    






# print("Autenticação OK")

# resultado = pesquisa("269746.0", tokens["access_token"])
# print("Pesquisa OK")

# dar_baixa= dar_baixa("7bc5ed0b-ba35-4bed-96aa-4b945617ed1a", 825.40, "2026-06-01", "16e33d66-a6d6-497c-a6fa-78a8771df1dd", tokens["access_token"])
# print("Dar baixa OK")