# API de Monitoramento de Estação CIP com InfluxDB e Grafana

Este projeto implementa uma solução completa para o monitoramento de dados de uma Estação CIP (Clean-in-Place). Consiste numa API RESTful desenvolvida em Python (Flask) que recebe dados de sensores, os processa e armazena numa base de dados de séries temporais (InfluxDB). A visualização dos dados é feita em tempo real através de dashboards no Grafana.

## Arquitetura do Projeto

O fluxo de dados segue a seguinte arquitetura:

```
[Simulador de Sensores] --(JSON via POST)--> [API Python/Flask] --(Line Protocol)--> [InfluxDB] <-- (Flux Query)-- [Grafana]
```

## Tecnologias Utilizadas

  - **Backend:** Python 3, Flask
  - **Base de Dados:** InfluxDB v2
  - **Visualização:** Grafana
  - **Orquestração de Contentores:** Docker, Docker Compose
  - **Comunicação:** REST API (JSON)

## Pré-requisitos

Antes de começar, garanta que você tem as seguintes ferramentas instaladas na sua máquina:

  - [Docker](https://www.docker.com/products/docker-desktop/)
  - [Docker Compose](https://docs.docker.com/compose/install/)
  - [Python 3.8+](https://www.python.org/downloads/)

## Como Executar o Projeto

Siga os passos abaixo para colocar toda a stack a funcionar.

**1. Clonar o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_SEU_REPOSITORIO>
```

**2. Configurar Variáveis de Ambiente**
Este projeto usa um ficheiro `.env` para gerir as credenciais. Crie uma cópia do ficheiro de exemplo:

```bash
# No Windows (use copy)
copy .env.example .env

# No Linux/macOS
cp .env.example .env
```

*O ficheiro `.env.example` já contém os valores padrão que configurámos no `docker-compose.yml`.*

**3. Iniciar os Serviços (InfluxDB e Grafana)**
Este comando vai iniciar os contentores do InfluxDB e Grafana em background.

```bash
docker-compose up -d
```

**4. Configurar o Ambiente Python**
Crie e ative um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente
# No Windows:
.\.venv\Scripts\activate
# No Linux/macOS:
source .venv/bin/activate
```

**5. Instalar as Dependências Python**
Instale todas as bibliotecas necessárias a partir do ficheiro `requirements.txt`.

```bash
pip install -r requirements.txt
```

**6. Executar a API**
Num terminal com o ambiente virtual ativado, inicie a API Flask.

```bash
python app.py
```

*A API estará a ouvir por pedidos na porta 5000.*

**7. Executar o Simulador de Sensores**
Abra **um novo terminal**, ative o ambiente virtual novamente e inicie o script que simula o envio de dados.

```bash
# Ative o ambiente virtual neste novo terminal
source .venv/bin/activate

# Inicie o simulador
python simulator.py
```

*Você começará a ver logs de dados a serem enviados a cada 5 segundos.*

## Estrutura dos Dados

### Endpoint da API

  - **URL:** `/api/dados-sensor`
  - **Método:** `POST`
  - **Formato do Corpo (JSON):**
    ```json
    {
        "id_sensor": "nome-do-sensor",
        "temperature": 25.5,
        "pressure": 1.2,
        "concentration": 7.1
    }
    ```

### Schema no InfluxDB

Os dados JSON são mapeados para o InfluxDB da seguinte forma:

  - **Bucket:** `sensores`
  - **Measurement:** `manitoramento_cip`
  - **Tags:**
      - `local`: (vem de `id_sensor`)
  - **Fields:**
      - `temperature`: (float)
      - `pressure`: (float)
      - `concentration`: (float)

## Aceder aos Serviços

Depois de executar todos os passos, os serviços estarão disponíveis nos seguintes endereços:

  - **InfluxDB UI:** [http://localhost:8086](https://www.google.com/search?q=http://localhost:8086)

      - **Utilizador:** `admin`
      - **Palavra-passe:** `admin12345`

  - **Grafana UI:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)

      - **Utilizador:** `admin`
      - **Palavra-passe:** `admin`

  - **API Endpoint:** `http://localhost:5000/api/dados-sensor`

