import requests
import json
from tinydb import TinyDB
from datetime import datetime
import time

def extrair():
       url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
       response = requests.get(url)
       return(response.json())



def transformar(dados_json):
    dados = dados_json['data']
    dados_tratados = {
        "base": dados.get('base', ''),
        "moeda": dados.get('currency', ''),
        "valor": float(dados.get('amount', 0.0)),
        "timestamp": datetime.now().isoformat()
    }
    return dados_tratados

def load(dados_tratados):
      db = TinyDB('db.json')
      db.insert(dados_tratados)
      print("dados salvos com sucesso")


if __name__ == "__main__":

   while True:
    dados_json = extrair()
    dados_tratados = transformar(dados_json)
    load(dados_tratados)
    time.sleep(60)