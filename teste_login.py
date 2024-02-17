import requests

# Dados para enviar no corpo da solicitação
data = {
    "email": "admin@admin.com",
    "password": "SUA SENHA"
}

# Credenciais de autenticação do IDP
idp_id = '123'
api_key = '321'

# URL do endpoint de login do seu sistema
host = 'http://127.0.0.1:8000'
url = f'{host}/api/singin'

# Realiza a solicitação POST com os dados e credenciais de autenticação
response = requests.post(
    url,
    json=data,
    auth=(idp_id, api_key),
    timeout=5
)

# Verifica a resposta
if response.status_code == 200:
    print("Sucesso! O usuário foi autenticado.")
    print("Resposta:", response.json())
else:
    # print(response.__dict__)
    print("Erro ao autenticar o usuário. Status code:", response.status_code)
