from services.auth import get_access_token
from services.pesquisa import pesquisa
from services.baixa import dar_baixa
from dotenv import load_dotenv
import os

import pandas as pd

load_dotenv()

tokens = get_access_token()


data_pagamento_input = input("Digite a data de pagamento (formato YYYY-MM-DD): (ou dê enter para usar a data do arquivo)")
id_conta_financeira = input("Nome da conta financeira (itau ou sicoob): ")
arquivo = input("Digite o nome do arquivo Excel (ex: darbaixa.xlsx): ")

planilha = pd.read_excel(arquivo)

if id_conta_financeira.lower() == "itau":
    conta_financeira = os.getenv("ID_ITAU")
elif id_conta_financeira.lower() == "sicoob":
    conta_financeira = os.getenv("ID_SICOOB")

for linha in planilha.index:
    nota = int(planilha.loc[linha, "Nota"])
    nota_certa = f"{nota}.0"

    valor_original = planilha.loc[linha, "Valor"]
    
    if isinstance(valor_original, str):
        valor_limpo = (
            valor_original
            .replace("R$", "")
            .replace(" ", "")
            .replace(".", "")
            .replace(",", ".")
        )

    else:
        valor = float(valor_original)

    data_pagamento = (
        data_pagamento_input 
        if data_pagamento_input 
        else planilha.loc[linha, "Data"].strftime("%Y-%m-%d")
    )
    
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

    


