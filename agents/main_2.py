from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.postgres import PostgresTools
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize PostgresTools with connection details
postgres_tools = PostgresTools(
    host="dpg-d0sv8bje5dus73bkeav0-a.oregon-postgres.render.com",
    port=5432,
    db_name="dbname_i3fy",
    user="dbname_i3fy_user",
    password="yq0m4bUGb3KEVfCNQ4orzUcg8sJIf0Ev",
    table_schema="public",
)

# Create an agent with the PostgresTools
agent = Agent(tools=[postgres_tools],
              model=Groq(id="llama-3.3-70b-versatile"))

agent.print_response("Fale todas as tabelas do banco de dados", markdown=True)

agent.print_response("""
Faça uma analise super complexa sobre o bitcoin usando os dados da tabela agents_bitcoin
""")
