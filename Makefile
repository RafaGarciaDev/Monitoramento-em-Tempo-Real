.PHONY: help init build up down restart logs clean

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## Inicializa o projeto (primeira execução)
	@echo "Inicializando projeto..."
	@mkdir -p airflow/logs airflow/plugins airflow/dags
	@echo "AIRFLOW_UID=$$(id -u)" > .env
	@cat .env.example >> .env
	@docker-compose up airflow-init
	@echo "Iniciando serviços..."
	@docker-compose up -d
	@echo ""
	@echo "✅ Projeto inicializado com sucesso!"
	@echo ""
	@echo "Aguarde 2-3 minutos para todos os serviços ficarem prontos..."
	@echo ""
	@echo "📊 Acesse os serviços:"
	@echo "  Airflow:      http://localhost:8080 (airflow/airflow)"
	@echo "  Grafana:      http://localhost:3000 (admin/admin)"
	@echo "  Prometheus:   http://localhost:9090"
	@echo "  AlertManager: http://localhost:9093"

build: ## Build de todos os containers
	docker-compose build

up: ## Inicia todos os serviços
	docker-compose up -d

down: ## Para todos os serviços
	docker-compose down

restart: ## Reinicia todos os serviços
	docker-compose restart

logs: ## Mostra logs de todos os serviços
	docker-compose logs -f

logs-airflow: ## Mostra logs do Airflow
	docker-compose logs -f airflow-webserver airflow-scheduler airflow-worker

logs-prometheus: ## Mostra logs do Prometheus
	docker-compose logs -f prometheus

logs-grafana: ## Mostra logs do Grafana
	docker-compose logs -f grafana

ps: ## Lista containers em execução
	docker-compose ps

stats: ## Mostra estatísticas de uso dos containers
	docker stats

clean: ## Remove containers, volumes e imagens
	docker-compose down -v --rmi all
	rm -rf airflow/logs/*

clean-logs: ## Limpa apenas os logs
	rm -rf airflow/logs/*

# Airflow commands
airflow-cli: ## Acessa CLI do Airflow
	docker-compose run --rm airflow-cli bash

airflow-db-upgrade: ## Upgrade do banco de dados do Airflow
	docker-compose run --rm airflow-cli db upgrade

create-user: ## Cria um novo usuário admin no Airflow
	docker-compose run --rm airflow-cli users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com \
		--password admin

list-dags: ## Lista todos os DAGs
	docker-compose run --rm airflow-cli dags list

trigger-dag: ## Trigger manual de um DAG (use: make trigger-dag DAG=dag_name)
	docker-compose run --rm airflow-cli dags trigger $(DAG)

test-dag: ## Testa um DAG sem executá-lo
	docker-compose run --rm airflow-cli dags test $(DAG)

# Monitoring commands
check-health: ## Verifica saúde de todos os serviços
	@echo "Verificando saúde dos serviços..."
	@curl -s http://localhost:8080/health | jq .
	@curl -s http://localhost:9090/-/healthy
	@curl -s http://localhost:3000/api/health | jq .

view-alerts: ## Ver alertas ativos no Prometheus
	@curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts'

view-targets: ## Ver targets do Prometheus
	@curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

export-metrics: ## Exporta métricas do Prometheus
	@mkdir -p exports
	@curl -s http://localhost:9090/api/v1/query?query=up > exports/metrics_$(shell date +%Y%m%d_%H%M%S).json
	@echo "Métricas exportadas para exports/"

# Database commands
db-shell: ## Acessa shell do PostgreSQL
	docker-compose exec postgres psql -U airflow -d airflow

db-backup: ## Backup do banco de dados
	@mkdir -p backups
	docker-compose exec -T postgres pg_dump -U airflow airflow > backups/airflow_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup criado em backups/"

db-restore: ## Restaura backup (use: make db-restore FILE=backup.sql)
	docker-compose exec -T postgres psql -U airflow airflow < $(FILE)

# Development commands
install-deps: ## Instala dependências Python adicionais
	docker-compose exec airflow-worker pip install $(PACKAGE)

format-dags: ## Formata código dos DAGs com black
	docker-compose exec airflow-worker black /opt/airflow/dags/

lint-dags: ## Verifica código dos DAGs com flake8
	docker-compose exec airflow-worker flake8 /opt/airflow/dags/

test-dags: ## Testa todos os DAGs
	docker-compose exec airflow-worker python -m pytest /opt/airflow/tests/

# Wait for services
wait-healthy: ## Aguarda todos os serviços ficarem saudáveis
	@echo "Aguardando serviços ficarem prontos..."
	@timeout 180 bash -c 'until docker-compose ps | grep -q "(healthy)"; do sleep 5; done' || echo "Timeout aguardando serviços"
	@echo "Serviços prontos!"
