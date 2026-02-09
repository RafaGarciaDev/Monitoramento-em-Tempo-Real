# 📊 Monitoramento de Data Pipelines

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Sistema completo de monitoramento e observabilidade para data pipelines com Apache Airflow, incluindo alertas em tempo real, dashboards interativos, rastreamento de SLA e análise de performance.

## 🎯 Sobre o Projeto

Este projeto demonstra a implementação de um sistema robusto de monitoramento para data pipelines, essencial para garantir a confiabilidade e performance de processos de ETL/ELT em produção.

### Recursos Principais

- **📈 Monitoramento em Tempo Real**: Métricas ao vivo de execução de pipelines
- **🚨 Sistema de Alertas**: Notificações via Slack/Email para falhas e SLA
- **📊 Dashboards Interativos**: Visualizações customizadas no Grafana
- **🔍 Rastreamento de Qualidade**: Validação de dados e qualidade
- **⏱️ Análise de Performance**: Identificação de gargalos e otimizações
- **📝 Logs Centralizados**: Agregação e busca eficiente de logs
- **🎯 SLA Tracking**: Monitoramento de acordos de nível de serviço
- **🔄 Pipeline Lineage**: Rastreamento de dependências entre pipelines

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
│         (PostgreSQL, APIs, CSV, S3, BigQuery)               │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Apache Airflow                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Pipeline 1│  │Pipeline 2│  │Pipeline 3│  │Pipeline N│   │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘   │
│        └─────────────┼─────────────┼─────────────┘         │
│                      │             │                        │
│              ┌───────▼─────────────▼───────┐               │
│              │   Metrics Exporter          │               │
│              │   - StatsD                  │               │
│              │   - Prometheus              │               │
│              └───────┬─────────────────────┘               │
└──────────────────────┼─────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────▼────┐   ┌───▼────┐   ┌───▼────┐
    │Prometheu│   │ Loki   │   │ElasticS│
    │   s     │   │(Logs)  │   │  earch │
    └────┬────┘   └───┬────┘   └───┬────┘
         │             │             │
         └─────────┬───┴─────────────┘
                   │
              ┌────▼────┐
              │ Grafana │
              │Dashboard│
              └─────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
    ┌────▼───┐ ┌──▼───┐ ┌──▼───┐
    │ Slack  │ │Email │ │PagerD│
    │        │ │      │ │ uty  │
    └────────┘ └──────┘ └──────┘
```

## 🚀 Tecnologias Utilizadas

### Core
- **Apache Airflow 2.8**: Orquestração de pipelines
- **PostgreSQL 15**: Backend do Airflow e data warehouse
- **Redis 7**: Celery broker para execução distribuída

### Monitoramento
- **Prometheus**: Coleta e armazenamento de métricas
- **Grafana**: Visualização e dashboards
- **Loki**: Agregação de logs
- **AlertManager**: Gerenciamento de alertas

### Qualidade de Dados
- **Great Expectations**: Validação de qualidade de dados
- **dbt**: Transformação e testes de dados

### Infraestrutura
- **Docker & Docker Compose**: Containerização
- **Nginx**: Reverse proxy
- **Python 3.11**: Scripts e operators customizados

## 📦 Estrutura do Projeto

```
data-pipeline-monitoring/
│
├── airflow/                      # Apache Airflow
│   ├── dags/                     # DAGs de exemplo
│   │   ├── example_etl.py       # Pipeline ETL simples
│   │   ├── data_quality.py      # Pipeline com validação
│   │   ├── ml_pipeline.py       # Pipeline de ML
│   │   └── monitoring_dag.py    # Auto-monitoramento
│   ├── plugins/                  # Plugins customizados
│   │   ├── operators/           # Operators personalizados
│   │   ├── sensors/             # Sensors customizados
│   │   └── hooks/               # Hooks para integrações
│   ├── config/
│   │   └── airflow.cfg          # Configuração do Airflow
│   └── requirements.txt
│
├── monitoring/                   # Stack de monitoramento
│   ├── prometheus/
│   │   ├── prometheus.yml       # Config Prometheus
│   │   ├── alerts.yml          # Regras de alerta
│   │   └── rules.yml           # Recording rules
│   ├── grafana/
│   │   ├── dashboards/         # Dashboards JSON
│   │   │   ├── pipeline-overview.json
│   │   │   ├── data-quality.json
│   │   │   └── sla-tracking.json
│   │   ├── datasources/        # Data sources
│   │   └── provisioning/       # Provisionamento
│   ├── loki/
│   │   └── loki-config.yml     # Config Loki
│   └── alertmanager/
│       └── alertmanager.yml    # Config alertas
│
├── data-quality/                 # Validação de qualidade
│   ├── great_expectations/
│   │   ├── expectations/       # Expectativas de dados
│   │   └── checkpoints/        # Checkpoints
│   └── dbt/
│       ├── models/             # Modelos dbt
│       └── tests/              # Testes de dados
│
├── scripts/                      # Scripts utilitários
│   ├── metrics_exporter.py     # Exportador de métricas
│   ├── alert_handler.py        # Handler de alertas
│   ├── sla_checker.py          # Verificador de SLA
│   └── data_profiler.py        # Profiler de dados
│
├── tests/                        # Testes
│   ├── dags/                   # Testes de DAGs
│   ├── integration/            # Testes de integração
│   └── unit/                   # Testes unitários
│
├── docker-compose.yml           # Orquestração
├── .env.example                # Variáveis de ambiente
├── Makefile                    # Comandos úteis
└── README.md
```

## 🔧 Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM (mínimo)
- 20GB disco disponível

## 📥 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/data-pipeline-monitoring.git
cd data-pipeline-monitoring
```

### 2. Configure variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

### 3. Inicie os serviços

```bash
# Método 1: Usando Makefile
make init

# Método 2: Docker Compose direto
docker-compose up -d

# Aguarde inicialização (pode levar 2-3 minutos)
make wait-healthy
```

### 4. Acesse os serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Airflow UI** | http://localhost:8080 | airflow/airflow |
| **Grafana** | http://localhost:3000 | admin/admin |
| **Prometheus** | http://localhost:9090 | - |
| **AlertManager** | http://localhost:9093 | - |

## 📊 Dashboards Disponíveis

### 1. Pipeline Overview
- Total de pipelines ativos
- Taxa de sucesso/falha
- Tempo médio de execução
- Pipelines em execução
- Histórico de execuções

### 2. Data Quality Dashboard
- Testes de qualidade executados
- Taxa de aprovação
- Anomalias detectadas
- Validações por dataset
- Tendências de qualidade

### 3. SLA Tracking
- Cumprimento de SLAs
- Pipelines em risco
- Tempo até deadline
- Histórico de violações
- Previsões de atraso

### 4. Performance Analysis
- CPU e memória por pipeline
- I/O de disco
- Tempo por task
- Gargalos identificados
- Recomendações de otimização

## 🚨 Sistema de Alertas

### Alertas Configurados

1. **Pipeline Failure**: Falha em qualquer pipeline
2. **SLA Violation**: Violação de SLA
3. **Data Quality Issues**: Problemas de qualidade
4. **Performance Degradation**: Degradação de performance
5. **Resource Exhaustion**: Recursos esgotando
6. **Long Running Tasks**: Tasks demorando muito

### Configuração de Notificações

#### Slack

```yaml
# monitoring/alertmanager/alertmanager.yml
receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#data-alerts'
        title: 'Pipeline Alert'
```

#### Email

```yaml
receivers:
  - name: 'email'
    email_configs:
      - to: 'team@example.com'
        from: 'airflow@example.com'
        smarthost: 'smtp.gmail.com:587'
```

## 📈 Métricas Coletadas

### Métricas de Pipeline
- `airflow_dag_run_total`: Total de execuções por DAG
- `airflow_dag_run_duration_seconds`: Duração das execuções
- `airflow_task_duration_seconds`: Duração por task
- `airflow_task_failures_total`: Total de falhas
- `airflow_scheduler_heartbeat`: Heartbeat do scheduler

### Métricas de Qualidade
- `data_quality_tests_total`: Total de testes
- `data_quality_failures_total`: Testes falhados
- `data_completeness_ratio`: Completude dos dados
- `data_freshness_seconds`: Frescor dos dados
- `schema_violations_total`: Violações de schema

### Métricas de Performance
- `pipeline_cpu_usage_percent`: Uso de CPU
- `pipeline_memory_usage_bytes`: Uso de memória
- `pipeline_io_operations_total`: Operações de I/O
- `pipeline_rows_processed_total`: Linhas processadas

## 🔍 Exemplo de DAG com Monitoramento

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging

# Configuração de SLA
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'sla': timedelta(hours=2),  # SLA de 2 horas
}

dag = DAG(
    'monitored_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL com monitoramento completo',
    schedule_interval='0 */6 * * *',  # A cada 6 horas
    start_date=days_ago(1),
    catchup=False,
    tags=['etl', 'production', 'monitored'],
)

def extract_data(**context):
    """Extrai dados com métricas"""
    from prometheus_client import Counter, Histogram
    import time
    
    # Métricas
    rows_extracted = Counter('rows_extracted_total', 'Total rows extracted')
    extraction_duration = Histogram('extraction_duration_seconds', 'Extraction time')
    
    start_time = time.time()
    
    # Lógica de extração
    rows = 10000
    rows_extracted.inc(rows)
    
    duration = time.time() - start_time
    extraction_duration.observe(duration)
    
    logging.info(f"Extracted {rows} rows in {duration:.2f}s")
    return rows

def validate_quality(**context):
    """Valida qualidade dos dados"""
    # Integração com Great Expectations
    pass

extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

validate = PythonOperator(
    task_id='validate_quality',
    python_callable=validate_quality,
    dag=dag,
)

extract >> validate
```

## 🧪 Testes

```bash
# Testar DAGs
make test-dags

# Testes unitários
make test-unit

# Testes de integração
make test-integration

# Validar configuração do Airflow
make validate-airflow
```

## 🛠️ Comandos Úteis

```bash
# Visualizar logs
make logs                    # Todos os serviços
make logs-airflow           # Apenas Airflow
make logs-prometheus        # Apenas Prometheus

# Gerenciar serviços
make start                  # Iniciar
make stop                   # Parar
make restart                # Reiniciar
make clean                  # Limpar tudo

# Monitoramento
make check-health          # Verificar saúde
make stats                 # Estatísticas de recursos
make export-metrics        # Exportar métricas

# Desenvolvimento
make shell-airflow         # Shell do Airflow
make airflow-db-upgrade    # Upgrade do DB
make create-user           # Criar usuário
```

## 📊 Análise de Performance

### Identificar Gargalos

1. Acesse Grafana → Performance Analysis Dashboard
2. Filtre por pipeline específico
3. Analise:
   - Tempo por task
   - Uso de recursos
   - I/O operations
   - Network latency

### Otimizações Comuns

- **Paralelização**: Aumentar `max_active_tasks_per_dag`
- **Pool Management**: Criar pools dedicados
- **Recursos**: Ajustar CPU/memória por task
- **Retry Logic**: Otimizar estratégia de retry
- **Caching**: Implementar cache de resultados

## 🔐 Segurança e Boas Práticas

- ✅ Secrets gerenciados via variáveis de ambiente
- ✅ RBAC habilitado no Airflow
- ✅ SSL/TLS em produção
- ✅ Backup automático de metadados
- ✅ Auditoria de acessos
- ✅ Rotação de credenciais

## 🚀 Deploy em Produção

### Kubernetes (Recomendado)

```bash
# Usar Helm Chart oficial do Airflow
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  --values production-values.yaml
```

### Cloud Providers

- **AWS**: Amazon MWAA (Managed Workflows for Apache Airflow)
- **GCP**: Cloud Composer
- **Azure**: Data Factory + Airflow

## 📈 Roadmap

- [ ] Integração com dbt Cloud
- [ ] ML Pipeline monitoring
- [ ] Cost tracking e otimização
- [ ] Data lineage visualization
- [ ] Auto-scaling baseado em carga
- [ ] Disaster recovery automation

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Seu Nome**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [seu-perfil](https://linkedin.com/in/seu-perfil)
- Email: seu-email@example.com

## 🙏 Agradecimentos

- Apache Airflow Community
- Prometheus & Grafana Teams
- Great Expectations Team

## 📚 Recursos Adicionais

- [Documentação Airflow](https://airflow.apache.org/docs/)
- [Guia Prometheus](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [Great Expectations](https://docs.greatexpectations.io/)

---

⭐ Se este projeto foi útil, considere dar uma estrela!

**Nota**: Este projeto é uma demonstração para portfólio. Para uso em produção, considere aspectos adicionais de segurança, escalabilidade e conformidade.
