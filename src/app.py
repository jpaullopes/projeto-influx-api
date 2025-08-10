import os
import flask
import influxdb_client
import influxdb_client.client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import datetime

import influxdb_client.client.write_api

# Carregando variáveis de ambinete do .env
load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

# Iniciando a aplicação Flask
app = flask.Flask(__name__)

# Cliente de conexão com o InfluxDB
try: 
    client = influxdb_client.InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN,org=INFLUX_ORG)
    write_api = influxdb_client.client.write_api(write_options=SYNCHRONOUS)
except Exception as e:
    print(f"Erro ao conectar ao InfluxDB: {e}")

@app.route('/api/dados-sensor', methods=['POST'])
def receber_dados():
    dados = flask.request.get_json()
    print(f"Dados recebido: {dados}")

    try:
        ponto = influxdb_client.Point("manitoramento_cip") \
        .tag("local", dados.get("id_sennsor")) \
        .fild("temperature", float(dados.get("temperature"))) \
        .fild("")