import requests
from tinydb import TinyDB
import time

def extrair():
    url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
    response = requests.get(url)
    response.raise_for_status()  # para levantar exceção se der erro no request
    return response.json()

def transformar(dados_json):
    dados = dados_json['data']
    dados_tratados = {
        "base": dados.get('base', ''),
        "moeda": dados.get('currency', ''),
        "valor": dados.get('amount', '')
    }
    return dados_tratados

def load(db, dados_tratados):
    db.insert(dados_tratados)
    print("dados salvos com sucesso")

if __name__ == "__main__":
    db = TinyDB('db.json')
    while True:
        try:
            dados_json = extrair()
            dados_tratados = transformar(dados_json)
            load(db, dados_tratados)
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(5)
