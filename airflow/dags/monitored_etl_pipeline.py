"""
DAG de exemplo com monitoramento completo
Demonstra integração com métricas, alertas e qualidade de dados
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import datetime, timedelta
import logging
import random
import time

# Configuração padrão
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'sla': timedelta(hours=2),
    'execution_timeout': timedelta(hours=1),
}

# Definição do DAG
dag = DAG(
    'monitored_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL com monitoramento e observabilidade',
    schedule_interval='0 */6 * * *',  # A cada 6 horas
    start_date=days_ago(1),
    catchup=False,
    tags=['production', 'etl', 'monitored', 'critical'],
    max_active_runs=1,
)

# Funções das tasks

def extract_data(**context):
    """
    Extrai dados de múltiplas fontes
    Simula extração com métricas e logging
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Starting data extraction...")
    start_time = time.time()
    
    # Simula extração de diferentes fontes
    sources = {
        'database': random.randint(8000, 12000),
        'api': random.randint(1000, 3000),
        'files': random.randint(500, 1500),
    }
    
    total_rows = sum(sources.values())
    
    # Log métricas
    for source, rows in sources.items():
        logger.info(f"Extracted {rows} rows from {source}")
    
    duration = time.time() - start_time
    
    # Push para XCom
    context['task_instance'].xcom_push(
        key='extraction_metrics',
        value={
            'total_rows': total_rows,
            'sources': sources,
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat()
        }
    )
    
    logger.info(f"Extraction completed: {total_rows} total rows in {duration:.2f}s")
    
    # Simula processamento
    time.sleep(random.uniform(1, 3))
    
    return total_rows


def validate_data_quality(**context):
    """
    Valida qualidade dos dados extraídos
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Starting data quality validation...")
    
    # Recupera métricas de extração
    ti = context['task_instance']
    extraction_metrics = ti.xcom_pull(
        task_ids='extract_data',
        key='extraction_metrics'
    )
    
    total_rows = extraction_metrics['total_rows']
    
    # Simula validações
    validations = {
        'null_check': random.uniform(0.95, 1.0),
        'schema_check': random.uniform(0.98, 1.0),
        'range_check': random.uniform(0.90, 1.0),
        'uniqueness_check': random.uniform(0.85, 1.0),
    }
    
    failed_validations = []
    for check, pass_rate in validations.items():
        logger.info(f"{check}: {pass_rate*100:.2f}% passed")
        if pass_rate < 0.95:
            failed_validations.append(check)
    
    quality_score = sum(validations.values()) / len(validations)
    
    # Push métricas de qualidade
    ti.xcom_push(
        key='quality_metrics',
        value={
            'quality_score': quality_score,
            'validations': validations,
            'failed_checks': failed_validations,
            'rows_validated': total_rows
        }
    )
    
    logger.info(f"Quality validation completed. Score: {quality_score*100:.2f}%")
    
    # Falha se qualidade muito baixa
    if quality_score < 0.85:
        raise ValueError(f"Data quality too low: {quality_score*100:.2f}%")
    
    time.sleep(random.uniform(0.5, 2))
    
    return quality_score


def transform_data(**context):
    """
    Transforma e limpa os dados
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Starting data transformation...")
    start_time = time.time()
    
    ti = context['task_instance']
    extraction_metrics = ti.xcom_pull(
        task_ids='extract_data',
        key='extraction_metrics'
    )
    
    total_rows = extraction_metrics['total_rows']
    
    # Simula transformações
    transformations = [
        'deduplication',
        'normalization',
        'enrichment',
        'aggregation',
        'cleaning'
    ]
    
    rows_after_transform = int(total_rows * random.uniform(0.85, 0.95))
    
    for transform in transformations:
        logger.info(f"Applying transformation: {transform}")
        time.sleep(random.uniform(0.2, 0.5))
    
    duration = time.time() - start_time
    
    ti.xcom_push(
        key='transform_metrics',
        value={
            'rows_before': total_rows,
            'rows_after': rows_after_transform,
            'transformations_applied': transformations,
            'duration_seconds': duration,
            'reduction_rate': (total_rows - rows_after_transform) / total_rows
        }
    )
    
    logger.info(f"Transformation completed: {rows_after_transform} rows in {duration:.2f}s")
    
    return rows_after_transform


def load_data(**context):
    """
    Carrega dados no destino
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Starting data load...")
    start_time = time.time()
    
    ti = context['task_instance']
    transform_metrics = ti.xcom_pull(
        task_ids='transform_data',
        key='transform_metrics'
    )
    
    rows_to_load = transform_metrics['rows_after']
    
    # Simula carga em batches
    batch_size = 1000
    batches = rows_to_load // batch_size
    
    loaded_rows = 0
    failed_rows = 0
    
    for batch in range(batches):
        try:
            # Simula carga
            time.sleep(random.uniform(0.1, 0.3))
            loaded_rows += batch_size
            
            if batch % 10 == 0:
                logger.info(f"Loaded {loaded_rows}/{rows_to_load} rows")
        
        except Exception as e:
            logger.error(f"Error loading batch {batch}: {e}")
            failed_rows += batch_size
    
    duration = time.time() - start_time
    success_rate = loaded_rows / rows_to_load if rows_to_load > 0 else 0
    
    ti.xcom_push(
        key='load_metrics',
        value={
            'rows_loaded': loaded_rows,
            'rows_failed': failed_rows,
            'duration_seconds': duration,
            'success_rate': success_rate,
            'throughput_rows_per_second': loaded_rows / duration if duration > 0 else 0
        }
    )
    
    logger.info(f"Load completed: {loaded_rows} rows in {duration:.2f}s")
    logger.info(f"Success rate: {success_rate*100:.2f}%")
    
    if success_rate < 0.95:
        raise ValueError(f"Load success rate too low: {success_rate*100:.2f}%")
    
    return loaded_rows


def send_metrics(**context):
    """
    Envia métricas consolidadas para sistema de monitoramento
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Consolidating and sending metrics...")
    
    ti = context['task_instance']
    
    # Coleta todas as métricas
    extraction_metrics = ti.xcom_pull(task_ids='extract_data', key='extraction_metrics')
    quality_metrics = ti.xcom_pull(task_ids='validate_quality', key='quality_metrics')
    transform_metrics = ti.xcom_pull(task_ids='transform_data', key='transform_metrics')
    load_metrics = ti.xcom_pull(task_ids='load_data', key='load_metrics')
    
    # Consolida métricas
    pipeline_metrics = {
        'dag_id': context['dag'].dag_id,
        'execution_date': context['execution_date'].isoformat(),
        'extraction': extraction_metrics,
        'quality': quality_metrics,
        'transformation': transform_metrics,
        'load': load_metrics,
        'total_duration': (
            extraction_metrics['duration_seconds'] +
            transform_metrics['duration_seconds'] +
            load_metrics['duration_seconds']
        )
    }
    
    # Aqui você enviaria para Prometheus/StatsD
    # Por enquanto, apenas log
    logger.info(f"Pipeline metrics: {pipeline_metrics}")
    
    # Simula envio de métricas
    time.sleep(0.5)
    
    logger.info("Metrics sent successfully")
    
    return True


def check_sla(**context):
    """
    Verifica se o SLA foi cumprido
    """
    logger = logging.getLogger(__name__)
    
    ti = context['task_instance']
    extraction_metrics = ti.xcom_pull(task_ids='extract_data', key='extraction_metrics')
    transform_metrics = ti.xcom_pull(task_ids='transform_data', key='transform_metrics')
    load_metrics = ti.xcom_pull(task_ids='load_data', key='load_metrics')
    
    total_duration = (
        extraction_metrics['duration_seconds'] +
        transform_metrics['duration_seconds'] +
        load_metrics['duration_seconds']
    )
    
    sla_seconds = default_args['sla'].total_seconds()
    
    logger.info(f"Total pipeline duration: {total_duration:.2f}s")
    logger.info(f"SLA: {sla_seconds}s")
    
    if total_duration > sla_seconds:
        logger.warning(f"SLA VIOLATED! Duration: {total_duration:.2f}s > SLA: {sla_seconds}s")
        # Aqui você enviaria um alerta
    else:
        logger.info(f"SLA met. Margin: {sla_seconds - total_duration:.2f}s")
    
    return total_duration < sla_seconds


# Definição das tasks
extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

validate = PythonOperator(
    task_id='validate_quality',
    python_callable=validate_data_quality,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

metrics = PythonOperator(
    task_id='send_metrics',
    python_callable=send_metrics,
    dag=dag,
)

sla_check = PythonOperator(
    task_id='check_sla',
    python_callable=check_sla,
    dag=dag,
)

# Health check
health_check = BashOperator(
    task_id='health_check',
    bash_command='echo "Pipeline health check passed"',
    dag=dag,
)

# Definição do fluxo
extract >> validate >> transform >> load >> [metrics, sla_check]
health_check >> extract
