import requests
import json
import time
import random
from datetime import datetime, timedelta

# O endereço da API
API_URL = "http://localhost:5000/api/dados-sensor"

# Função que determina o status do CIP baseado no tempo de espera
def status_cip(cip_mudou_recentemente):
    if cip_mudou_recentemente:
        return "false"
    else:
        return "true"

print(f"Enviando dados para: {API_URL}")
cip_id = 1 
count_cip = 0
tempo_mudanca_cip = None  # Controla quando o CIP mudou
TEMPO_ESPERA_MINUTOS = 3  # Tempo de espera em minutos

while True:
    try:
        sensor_id = "estacao_cip"
        
        # Verifica se o CIP mudou recentemente (nos últimos 3 minutos)
        cip_mudou_recentemente = False
        if tempo_mudanca_cip:
            tempo_atual = datetime.now()
            tempo_espera = tempo_mudanca_cip + timedelta(minutes=TEMPO_ESPERA_MINUTOS)
            cip_mudou_recentemente = tempo_atual < tempo_espera
        
        # Gera dados aleatórios
        temperatura = round(random.uniform(70.0, 100.0), 2)
        pressao = round(random.uniform(1.5, 3.0), 2)
        concentracao = round(random.uniform(0.4, 2.5), 2)

        # Monta o JSON com os dados do sensor
        dados_sensor = {
            "id_sensor": sensor_id,
            "cip_id": str(cip_id),
            "status_cip": status_cip(cip_mudou_recentemente)
            ,
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
    
    # Quando atinge 120 ciclos (10 minutos), muda o CIP ID
    if count_cip >= 120:
        count_cip = 0
        cip_id += 1
        tempo_mudanca_cip = datetime.now()  # Marca o momento da mudança
        print(f"CIP mudou para ID {cip_id}. Status será 'false' pelos próximos {TEMPO_ESPERA_MINUTOS} minutos.")