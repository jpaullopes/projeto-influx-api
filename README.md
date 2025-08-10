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


