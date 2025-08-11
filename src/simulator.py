import requests
import json
import time
import random

# O endereço da API
API_URL = "http://localhost:5000/api/dados-sensor"

# Função que com base na temperatura informa se o CIP está ativo ou inativo
def status_cip(temperatura):
    if temperatura > 20.0:
        return "true"
    else:
        return "false"

print(f"Enviando dados para: {API_URL}")
cip_id = 1 
count_cip = 0
while True:
    try:
        sensor_id = "estacao_cip"
        
        # Gera dados aleatórios
        temperatura = round(random.uniform(20.0, 26.0), 2)
        pressao = round(random.uniform(900.0, 1100.0), 2)
        concentracao = round(random.uniform(0.0, 100.0), 2)

        # Monta o JSON com os dados do sensor
        dados_sensor = {
            "id_sensor": sensor_id,
            "cip_id": str(cip_id),
            "status_cip": status_cip(temperatura),
            "temperature": temperatura,
            "pressure": pressao,
            "concentration": concentracao
        }
        
        # Envia os dados para a API usando uma requisição POST
        response = requests.post(API_URL, json=dados_sensor)
        print(f"Sensor: {sensor_id}, Dados: {dados_sensor}, Status: {response.status_code}")
        
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: A API está no ar? Detalhe: {e}")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    time.sleep(5)
    count_cip += 1
    if count_cip >= 120:
        count_cip = 0
        cip_id += 1
        time.sleep(300)