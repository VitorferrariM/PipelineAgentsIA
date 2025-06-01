import requests
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_KEY")
if not DATABASE_URL:
    raise Exception("❌ DATABASE_KEY não encontrada no .env e não foi definida manualmente.")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class DolarDados(Base):
    __tablename__ = "agents_bitcoin"
    
    id = Column(Integer, primary_key=True)
    base = Column(String(10))
    moeda = Column(String(10))
    valor = Column(Float)
    data_insercao = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    timestamp = Column(DateTime(timezone=True), nullable=True)

# IMPORTANTE: Para desenvolvimento, pode querer recriar a tabela para garantir colunas atualizadas
Base.metadata.drop_all(engine)  # Apaga tabela se existir
Base.metadata.create_all(engine)  # Cria tabela nova com colunas corretas

def extrair_dados_dolar():
    url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
    resposta = requests.get(url)
    if resposta.status_code != 200:
        raise Exception(f"Erro ao buscar dados da API! Status code: {resposta.status_code}")
    return resposta.json()

def tratar_dados_dolar(dados_json):
    dados = dados_json.get('data', {})
    return DolarDados(
        base=dados.get('base', ''),
        moeda=dados.get('currency', ''),
        valor=float(dados.get('amount', 0.0)),
        data_insercao=datetime.now(timezone.utc),
        timestamp=None
    )

def salvar_dados_sqlalchemy(dados):
    with Session() as session:
        session.add(dados)
        session.commit()
        print("✅ Dados salvos no PostgreSQL!")

if __name__ == "__main__":
    while True:
        try:
            dados_json = extrair_dados_dolar()
            dados_tratados = tratar_dados_dolar(dados_json)
            print("📊 Dados Tratados:", {
                'base': dados_tratados.base,
                'moeda': dados_tratados.moeda,
                'valor': dados_tratados.valor,
                'data_insercao': dados_tratados.data_insercao,
                'timestamp': dados_tratados.timestamp
            })
            salvar_dados_sqlalchemy(dados_tratados)
        except Exception as e:
            print(f"❌ Erro: {e}")
            print(f"🔍 DATABASE_URL: {DATABASE_URL}")
        print("⏳ Aguardando 15 segundos...\n")
        sleep(15)
