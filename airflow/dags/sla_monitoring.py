"""
DAG para monitoramento de SLA de pipelines
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging

default_args = {
    'owner': 'sre-team',
    'depends_on_past': False,
    'email': ['sre@example.com'],
    'email_on_failure': True,
    'retries': 1,
}

dag = DAG(
    'sla_monitoring',
    default_args=default_args,
    description='Monitora SLAs de todos os pipelines',
    schedule_interval='*/15 * * * *',  # A cada 15 minutos
    start_date=days_ago(1),
    catchup=False,
    tags=['monitoring', 'sla', 'alerting'],
)


def check_pipeline_slas(**context):
    """Verifica SLAs de todos os pipelines críticos"""
    logger = logging.getLogger(__name__)
    
    # Simulação de verificação de SLAs
    pipelines = {
        'monitored_etl_pipeline': {'sla_hours': 2, 'current_duration': 1.5, 'status': 'OK'},
        'data_quality_monitoring': {'sla_hours': 1, 'current_duration': 0.8, 'status': 'OK'},
        'ml_training_pipeline': {'sla_hours': 4, 'current_duration': 4.2, 'status': 'VIOLATED'},
    }
    
    violations = []
    
    for pipeline, data in pipelines.items():
        if data['status'] == 'VIOLATED':
            violations.append(pipeline)
            logger.warning(
                f"SLA VIOLATION: {pipeline} - "
                f"Duration: {data['current_duration']}h > SLA: {data['sla_hours']}h"
            )
        else:
            logger.info(
                f"SLA OK: {pipeline} - "
                f"Duration: {data['current_duration']}h < SLA: {data['sla_hours']}h"
            )
    
    if violations:
        logger.error(f"Total violations: {len(violations)}")
    
    return len(violations) == 0


sla_check = PythonOperator(
    task_id='check_pipeline_slas',
    python_callable=check_pipeline_slas,
    dag=dag,
)
