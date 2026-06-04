## ContaAzul RPA

Este projeto é um script Python para automatizar a pesquisa e baixa de parcelas no Conta Azul usando um arquivo Excel.
O foco é permitir que você leia um arquivo com notas e valores, pesquise as parcelas correspondentes e execute a baixa de forma automatizada.

---

### Principais funcionalidades

- **Leitura de planilha Excel** (`planilha.xlsx` ou outro nome definido em `main.py`)
- **Pesquisa de contas a receber** no Conta Azul por descrição/nota
- **Baixa automática de parcelas** usando API Conta Azul
- **Normalização de valores** em diferentes formatos (`R$ 1.234,56`, `1234,56`, `1.234,56`, etc.)
- **Suporte a múltiplas contas financeiras** (`ID_CONTABANCARIA1` e `ID_CONTABANCARIA2`)

---

### Arquitetura geral

- **`main.py`**
  - Lê a planilha Excel
  - Solicita data de pagamento e conta financeira
  - Chama `pesquisa` e `dar_baixa` para cada linha

- **`services/auth.py`**
  - Autentica no Conta Azul com OAuth2
  - Obtém o `access_token` a partir de `CLIENT_ID`, `CLIENT_SECRET` e `REFRESH_TOKEN`

- **`services/pesquisa.py`**
  - Consulta a API de contas a receber
  - Usa `descricao` e intervalo de vencimento para buscar as parcelas

- **`services/baixa.py`**
  - Envia requisição de baixa para a parcela encontrada
  - Retorna o status da operação para validação

---

### Fluxo de uso

1. **Abrir o script**
   - Execute `python main.py`
2. **Informar data de pagamento**
   - Formato `YYYY-MM-DD`
3. **Escolher conta financeira**
   - `itau` ou `sicoob`, por exemplo
4. **O script processa cada nota**
   - Pesquisa a nota no Conta Azul
   - Se encontrar, envia a baixa
   - Mostra sucesso ou erro para cada item

---

### Requisitos e execução

- **Pré-requisitos**
  - Python 3.11+ instalado
  - Biblioteca `requests`
  - Biblioteca `python-dotenv`
  - Biblioteca `pandas`

- **Passos básicos**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

> Ajuste o nome do arquivo Excel em `main.py` se for usar outro arquivo.

---

### Variáveis de ambiente

- **`CLIENT_ID`**
- **`CLIENT_SECRET`**
- **`REFRESH_TOKEN`**
- **`ID_CONTABANCARIA1`**
- **`ID_CONTABANCARIA2`** 


---

### Estrutura resumida do projeto

- `main.py` – ponto de entrada do script
- `services/auth.py` – autenticação Conta Azul
- `services/pesquisa.py` – busca de contas a receber
- `services/baixa.py` – execução de baixa
- `.env.example` – exemplo de variáveis de ambiente
- `requirements.txt` – dependências Python

---

### Observações

- Se o valor da planilha estiver em formato brasileiro com `R$`, espaços ou pontos, o script tenta normalizar automaticamente.
- Se a nota não for encontrada, ela é pulada e o script segue para a próxima linha.
- Se a API retornar erro, o script mostra o código HTTP e a mensagem de erro.
