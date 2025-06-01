import requests
import json

def extrair():
       url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
       response = requests.get(url)
       return(response.json())



def transformar(dados_json):
    dados = dados_json['data']
    dados_tratados = {
        "base": dados.get('base', ''),
        "moeda": dados.get('currency', ''),
        "valor": dados.get('amount', '')
     }

    return dados_tratados

if "__name__ == __main__":
    dados_json = extrair()
    dados_tratados = transformar(dados_json)
    print(dados_tratados)