# 🚀 Guia de Início Rápido

## Requisitos Mínimos

- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM
- 20GB disco livre

## Instalação em 3 Passos

### 1️⃣ Clone e Configure

```bash
git clone https://github.com/seu-usuario/data-pipeline-monitoring.git
cd data-pipeline-monitoring
```

### 2️⃣ Inicialize o Projeto

```bash
make init
```

Este comando irá:
- Criar estrutura de diretórios
- Configurar variáveis de ambiente
- Inicializar banco de dados do Airflow
- Iniciar todos os serviços

### 3️⃣ Aguarde e Acesse

Aguarde 2-3 minutos para todos os serviços ficarem prontos.

## 🌐 Acessando os Serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Airflow** | http://localhost:8080 | airflow / airflow |
| **Grafana** | http://localhost:3000 | admin / admin |
| **Prometheus** | http://localhost:9090 | - |
| **AlertManager** | http://localhost:9093 | - |

## 🎯 Primeiros Passos no Airflow

1. Acesse http://localhost:8080
2. Login: `airflow` / `airflow`
3. Vá para **DAGs**
4. Ative os DAGs:
   - `monitored_etl_pipeline`
   - `data_quality_monitoring`
   - `sla_monitoring`
5. Clique em ▶️ para executar manualmente

## 📊 Visualizando Métricas no Grafana

1. Acesse http://localhost:3000
2. Login: `admin` / `admin`
3. Vá para **Dashboards**
4. Explore os dashboards pré-configurados:
   - Pipeline Overview
   - Data Quality
   - SLA Tracking
   - Performance Analysis

## 🔔 Configurando Alertas

### Slack

Edite `monitoring/alertmanager/alertmanager.yml`:

```yaml
slack_configs:
  - api_url: 'SEU_WEBHOOK_URL'
    channel: '#data-alerts'
```

### Email

Edite `.env`:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
```

## 🛠️ Comandos Úteis

```bash
# Ver logs
make logs-airflow

# Ver status
make ps

# Verificar saúde
make check-health

# Listar DAGs
make list-dags

# Executar DAG manualmente
make trigger-dag DAG=monitored_etl_pipeline

# Backup do banco
make db-backup

# Parar tudo
make down

# Limpar e recomeçar
make clean
make init
```

## 🐛 Troubleshooting

### Serviços não iniciam

```bash
# Ver logs
docker-compose logs

# Recriar containers
make clean
make init
```

### Porta em uso

Edite `docker-compose.yml` e altere as portas:

```yaml
ports:
  - "8081:8080"  # Airflow
  - "3001:3000"  # Grafana
```

### Sem espaço em disco

```bash
# Limpar logs antigos
make clean-logs

# Limpar volumes não utilizados
docker volume prune
```

## 📚 Próximos Passos

1. ✅ Explore os DAGs de exemplo
2. ✅ Configure alertas para seu time
3. ✅ Customize os dashboards no Grafana
4. ✅ Crie seus próprios DAGs
5. ✅ Configure integração com suas fontes de dados

## 🆘 Precisa de Ajuda?

- 📖 Leia o [README.md](README.md) completo
- 🐛 Abra uma [issue](https://github.com/seu-usuario/data-pipeline-monitoring/issues)
- 💬 Entre em contato

## 🎉 Tudo Pronto!

Seu ambiente de monitoramento de pipelines está configurado!

Próximo passo: Explore os dashboards no Grafana e acompanhe a execução dos DAGs no Airflow.

Happy Data Engineering! 🚀
