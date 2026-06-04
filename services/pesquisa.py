from datetime import datetime

import requests

ano_atual = datetime.now().year
ano_anterior = ano_atual - 1

data_vencimento_de = f"{ano_anterior}-01-01"
data_vencimento_ate = f"{ano_atual}-12-31"

def pesquisa(nota, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "descricao": nota
    }


    response = requests.post(
        "https://api-v2.contaazul.com/v1/financeiro/eventos-financeiros/contas-a-receber/buscar",
        headers=headers,
        params={"descricao": nota, "data_vencimento_de": data_vencimento_de, "data_vencimento_ate": data_vencimento_ate},
        json=body
    )

    return response.json()

