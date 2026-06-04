import requests


def dar_baixa(parcela_id, valor, data_pagamento, conta_financeira, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "data_pagamento": data_pagamento, 
        "composicao_valor": {
            "valor_bruto": valor,
        },
        "conta_financeira": conta_financeira
    }

    response = requests.post(
        f"https://api-v2.contaazul.com/v1/financeiro/eventos-financeiros/parcelas/{parcela_id}/baixa",
        headers=headers,    
        json=body
    )
    
    return response
