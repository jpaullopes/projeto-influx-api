# API de Monitoramento de Sensores com InfluxDB e Grafana

![Backend](https://img.shields.io/badge/backend-Flask-blue)
![Database](https://img.shields.io/badge/database-InfluxDB-blueviolet)
![Visualization](https://img.shields.io/badge/visualization-Grafana-orange)
![Container](https://img.shields.io/badge/container-Docker-lightgrey)
![Simulator](https://img.shields.io/badge/simulator-included-success)


Solução enxuta e prática para receber dados de sensores via HTTP, armazenar no InfluxDB e visualizar no Grafana. O projeto serviu também como forma aprendizado sobre InfluxDB e uma contrução de API relacionada à ele e sua conexão com o Grafana.

## 📝 Descrição

Esta API em Flask expõe um endpoint para receber leituras de sensores (JSON) e persiste os dados no InfluxDB. Um simulador acompanha o projeto para facilitar testes locais, enviando dados periódicos à API.

## ✨ Funcionalidades

- Recebimento de dados via POST (JSON)
- Escrita no InfluxDB (bucket `sensores`, org `minha-org`)
- Visualização via Grafana
- Simulador de sensores incluso (`src/simulator.py`)

## 🚀 Tecnologias Utilizadas

- Python 3.8+, Flask, python-dotenv
- influxdb-client (InfluxDB 2.7)
- Docker & Docker Compose
- Grafana

## ⚙️ Como Usar

1) Clone o repositório
```bash
git clone https://github.com/jpaullopes/projeto-influx-api.git
cd projeto-influx-api
```

2) Suba InfluxDB e Grafana
```bash
docker-compose up -d
```

3) Configure variáveis de ambiente (arquivo `.env` na raiz)
```env
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=meu-token-super-secreto
INFLUX_ORG=minha-org
INFLUX_BUCKET=sensores
```

4) Prepare o ambiente Python e instale dependências
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

5) Inicie a API
```bash
python src/app.py
```

6) (Opcional) Execute o simulador de sensores
```bash
python src/simulator.py
```

## 🌐 Acesso aos Serviços

- API: http://localhost:5000/api/dados-sensor
- InfluxDB UI: http://localhost:8086 (admin / admin12345)
- Grafana UI: http://localhost:3000 (admin / admin)

## ❗ Dicas e Troubleshooting

- Certifique-se de que o token no `.env` coincide com `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` do `docker-compose.yml`.
- Se as portas 5000, 3000 ou 8086 estiverem ocupadas, ajuste mapeamentos em `docker-compose.yml`.


## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.


