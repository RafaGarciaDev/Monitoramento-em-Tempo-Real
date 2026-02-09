"""
DAG focado em Data Quality Monitoring
Valida múltiplas dimensões de qualidade de dados
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging
import random

default_args = {
    'owner': 'data-quality-team',
    'depends_on_past': False,
    'email': ['quality@example.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'data_quality_monitoring',
    default_args=default_args,
    description='Monitoramento contínuo de qualidade de dados',
    schedule_interval='0 */2 * * *',  # A cada 2 horas
    start_date=days_ago(1),
    catchup=False,
    tags=['data-quality', 'monitoring', 'validation'],
)


def check_completeness(**context):
    """Verifica completude dos dados"""
    logger = logging.getLogger(__name__)
    
    total_records = random.randint(5000, 10000)
    null_records = random.randint(0, int(total_records * 0.05))
    
    completeness = (total_records - null_records) / total_records
    
    logger.info(f"Completeness check: {completeness*100:.2f}%")
    
    context['task_instance'].xcom_push(
        key='completeness_score',
        value=completeness
    )
    
    return completeness > 0.95


def check_accuracy(**context):
    """Verifica acurácia dos dados"""
    logger = logging.getLogger(__name__)
    
    accuracy_score = random.uniform(0.92, 0.99)
    
    logger.info(f"Accuracy check: {accuracy_score*100:.2f}%")
    
    context['task_instance'].xcom_push(
        key='accuracy_score',
        value=accuracy_score
    )
    
    return accuracy_score > 0.95


def check_consistency(**context):
    """Verifica consistência entre datasets"""
    logger = logging.getLogger(__name__)
    
    consistency_score = random.uniform(0.88, 0.98)
    
    logger.info(f"Consistency check: {consistency_score*100:.2f}%")
    
    context['task_instance'].xcom_push(
        key='consistency_score',
        value=consistency_score
    )
    
    return consistency_score > 0.90


def check_timeliness(**context):
    """Verifica atualidade dos dados"""
    logger = logging.getLogger(__name__)
    
    delay_hours = random.uniform(0, 6)
    is_timely = delay_hours < 4
    
    logger.info(f"Data delay: {delay_hours:.2f} hours")
    
    context['task_instance'].xcom_push(
        key='timeliness_delay',
        value=delay_hours
    )
    
    return is_timely


def check_uniqueness(**context):
    """Verifica unicidade dos registros"""
    logger = logging.getLogger(__name__)
    
    total_records = 10000
    duplicates = random.randint(0, 200)
    
    uniqueness = (total_records - duplicates) / total_records
    
    logger.info(f"Uniqueness check: {uniqueness*100:.2f}% ({duplicates} duplicates)")
    
    context['task_instance'].xcom_push(
        key='uniqueness_score',
        value=uniqueness
    )
    
    return uniqueness > 0.98


def calculate_dq_score(**context):
    """Calcula score geral de qualidade"""
    logger = logging.getLogger(__name__)
    
    ti = context['task_instance']
    
    completeness = ti.xcom_pull(task_ids='check_completeness', key='completeness_score')
    accuracy = ti.xcom_pull(task_ids='check_accuracy', key='accuracy_score')
    consistency = ti.xcom_pull(task_ids='check_consistency', key='consistency_score')
    uniqueness = ti.xcom_pull(task_ids='check_uniqueness', key='uniqueness_score')
    
    # Peso balanceado
    dq_score = (
        completeness * 0.25 +
        accuracy * 0.30 +
        consistency * 0.20 +
        uniqueness * 0.25
    )
    
    logger.info(f"Overall Data Quality Score: {dq_score*100:.2f}%")
    
    if dq_score < 0.90:
        logger.warning(f"Data quality below threshold: {dq_score*100:.2f}%")
    
    return dq_score


# Tasks
completeness = PythonOperator(
    task_id='check_completeness',
    python_callable=check_completeness,
    dag=dag,
)

accuracy = PythonOperator(
    task_id='check_accuracy',
    python_callable=check_accuracy,
    dag=dag,
)

consistency = PythonOperator(
    task_id='check_consistency',
    python_callable=check_consistency,
    dag=dag,
)

timeliness = PythonOperator(
    task_id='check_timeliness',
    python_callable=check_timeliness,
    dag=dag,
)

uniqueness = PythonOperator(
    task_id='check_uniqueness',
    python_callable=check_uniqueness,
    dag=dag,
)

dq_score = PythonOperator(
    task_id='calculate_dq_score',
    python_callable=calculate_dq_score,
    dag=dag,
)

# Flow
[completeness, accuracy, consistency, timeliness, uniqueness] >> dq_score
