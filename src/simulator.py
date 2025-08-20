import requests
import json
import time
import random
import math
from datetime import datetime, timedelta

# O endereço da API
API_URL = "http://localhost:8000/api/v1/temperature_reading"

# Definição das fases do CIP e suas características
class CIPPhases:
    PRE_RINSE = "pre_rinse"
    ALKALINE_WASH = "alkaline_wash"
    INTERMEDIATE_RINSE = "intermediate_rinse"
    ACID_WASH = "acid_wash"
    FINAL_RINSE = "final_rinse"
    SANITIZATION = "sanitization"

# Configurações de cada fase do CIP (em segundos)
PHASE_CONFIG = {
    CIPPhases.PRE_RINSE: {
        "duration": 300,  # 5 minutos
        "temp_range": (20, 25),
        "pressure_range": (1.2, 1.8),
        "concentration_range": (0.0, 0.1)
    },
    CIPPhases.ALKALINE_WASH: {
        "duration": 900,  # 15 minutos
        "temp_range": (75, 85),
        "pressure_range": (2.5, 3.0),
        "concentration_range": (2.0, 2.5)
    },
    CIPPhases.INTERMEDIATE_RINSE: {
        "duration": 240,  # 4 minutos
        "temp_range": (65, 75),
        "pressure_range": (1.8, 2.2),
        "concentration_range": (0.0, 0.2)
    },
    CIPPhases.ACID_WASH: {
        "duration": 600,  # 10 minutos
        "temp_range": (70, 80),
        "pressure_range": (2.2, 2.8),
        "concentration_range": (1.8, 2.2)
    },
    CIPPhases.FINAL_RINSE: {
        "duration": 360,  # 6 minutos
        "temp_range": (20, 30),
        "pressure_range": (1.5, 2.0),
        "concentration_range": (0.0, 0.1)
    },
    CIPPhases.SANITIZATION: {
        "duration": 480,  # 8 minutos
        "temp_range": (50, 60),
        "pressure_range": (1.8, 2.4),
        "concentration_range": (0.8, 1.2)
    }
}

# Ordem das fases do CIP
PHASE_ORDER = [
    CIPPhases.PRE_RINSE,
    CIPPhases.ALKALINE_WASH,
    CIPPhases.INTERMEDIATE_RINSE,
    CIPPhases.ACID_WASH,
    CIPPhases.FINAL_RINSE,
    CIPPhases.SANITIZATION
]

class CIPSimulator:
    def __init__(self):
        self.cip_id = 1
        self.current_phase_index = 0
        self.phase_start_time = datetime.now()
        self.previous_temp = 20.0
        self.previous_pressure = 1.5
        self.previous_concentration = 0.0
        
    def get_current_phase(self):
        return PHASE_ORDER[self.current_phase_index]
    
    def get_phase_progress(self):
        """Retorna o progresso da fase atual (0.0 a 1.0)"""
        current_time = datetime.now()
        elapsed = (current_time - self.phase_start_time).total_seconds()
        phase_duration = PHASE_CONFIG[self.get_current_phase()]["duration"]
        return min(elapsed / phase_duration, 1.0)
    
    def should_advance_phase(self):
        """Verifica se deve avançar para a próxima fase"""
        return self.get_phase_progress() >= 1.0
    
    def advance_phase(self):
        """Avança para a próxima fase ou próximo CIP"""
        self.current_phase_index += 1
        if self.current_phase_index >= len(PHASE_ORDER):
            # Completa o CIP, inicia o próximo
            self.current_phase_index = 0
            self.cip_id += 1
            print(f"CIP {self.cip_id - 1} completado. Iniciando CIP {self.cip_id}")
        
        self.phase_start_time = datetime.now()
        current_phase = self.get_current_phase()
        print(f"Iniciando fase: {current_phase}")
    
    def generate_realistic_value(self, target_range, previous_value, transition_speed=0.1):
        """Gera valores realistas com transições graduais"""
        target_min, target_max = target_range
        target_value = random.uniform(target_min, target_max)
        
        # Aplica transição gradual
        if abs(target_value - previous_value) > (target_max - target_min) * 0.3:
            # Se a diferença for muito grande, faz transição gradual
            if target_value > previous_value:
                new_value = previous_value + (target_max - target_min) * transition_speed
            else:
                new_value = previous_value - (target_max - target_min) * transition_speed
            
            # Garante que não ultrapasse os limites
            new_value = max(target_min, min(target_max, new_value))
        else:
            new_value = target_value
        
        # Adiciona pequena variação aleatória
        variation = random.uniform(-0.02, 0.02) * (target_max - target_min)
        return round(new_value + variation, 2)
    
    def get_sensor_data(self):
        """Gera dados do sensor baseado na fase atual do CIP"""
        current_phase = self.get_current_phase()
        config = PHASE_CONFIG[current_phase]
        
        # Gera valores realistas com transições graduais
        temperature = self.generate_realistic_value(
            config["temp_range"], 
            self.previous_temp, 
            0.15
        )
        
        pressure = self.generate_realistic_value(
            config["pressure_range"], 
            self.previous_pressure, 
            0.12
        )
        
        concentration = self.generate_realistic_value(
            config["concentration_range"], 
            self.previous_concentration, 
            0.08
        )
        
        # Atualiza valores anteriores
        self.previous_temp = temperature
        self.previous_pressure = pressure
        self.previous_concentration = concentration
        
        return temperature, pressure, concentration

# Função que determina o status do CIP baseado no tempo de espera
def status_cip(cip_mudou_recentemente):
    if cip_mudou_recentemente:
        return "false"
    else:
        return "true"

print(f"Enviando dados para: {API_URL}")
cip_simulator = CIPSimulator()
tempo_mudanca_cip = None  # Controla quando o CIP mudou
TEMPO_ESPERA_MINUTOS = 3  # Tempo de espera em minutos

while True:
    try:
        sensor_id = "estacao_cip"
        
        # Verifica se deve avançar para a próxima fase
        if cip_simulator.should_advance_phase():
            old_cip_id = cip_simulator.cip_id
            cip_simulator.advance_phase()
            
            # Se mudou de CIP, marca o tempo para controle de status
            if cip_simulator.cip_id != old_cip_id:
                tempo_mudanca_cip = datetime.now()
        
        # Verifica se o CIP mudou recentemente (nos últimos 3 minutos)
        cip_mudou_recentemente = False
        if tempo_mudanca_cip:
            tempo_atual = datetime.now()
            tempo_espera = tempo_mudanca_cip + timedelta(minutes=TEMPO_ESPERA_MINUTOS)
            cip_mudou_recentemente = tempo_atual < tempo_espera
        
        # Gera dados realistas baseado na fase atual do CIP
        temperatura, pressao, concentracao = cip_simulator.get_sensor_data()

        # Monta o JSON com os dados do sensor (mantém formato original)
        dados_sensor = {
            "id_sensor": sensor_id,
            "cip_id": str(cip_simulator.cip_id),
            "status_cip": status_cip(cip_mudou_recentemente),
            "temperature": temperatura,
            "pressure": pressao,
            "concentration": concentracao
        }
        
        # Headers necessários para a API
        headers = {
            "X-API-Key": "api_key",
            "Content-Type": "application/json"
        }
        
        # Envia os dados para a API usando uma requisição POST
        response = requests.post(API_URL, json=dados_sensor, headers=headers)
        
        # Mostra informações mais detalhadas
        current_phase = cip_simulator.get_current_phase()
        progress = cip_simulator.get_phase_progress()
        print(response.headers)
        print(response.content)
        print(response.text)
        print(f"CIP {cip_simulator.cip_id} | Fase: {current_phase} ({progress:.1%}) | "
              f"T:{temperatura}°C P:{pressao}bar C:{concentracao}% | Status: {response.status_code}")
        
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: A API está no ar? Detalhe: {e}")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    time.sleep(5)