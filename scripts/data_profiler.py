#!/usr/bin/env python3
"""
Script de Data Profiling
Analisa características dos dados e gera relatório de qualidade
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProfiler:
    """Profiler para análise de qualidade de dados"""
    
    def __init__(self, df: pd.DataFrame, dataset_name: str):
        self.df = df
        self.dataset_name = dataset_name
        self.profile = {}
    
    def analyze_completeness(self):
        """Analisa completude dos dados"""
        logger.info("Analyzing data completeness...")
        
        total_cells = self.df.size
        null_cells = self.df.isnull().sum().sum()
        
        completeness = {
            'total_cells': int(total_cells),
            'null_cells': int(null_cells),
            'completeness_ratio': float((total_cells - null_cells) / total_cells),
            'columns': {}
        }
        
        for col in self.df.columns:
            null_count = self.df[col].isnull().sum()
            completeness['columns'][col] = {
                'null_count': int(null_count),
                'null_percentage': float(null_count / len(self.df) * 100)
            }
        
        self.profile['completeness'] = completeness
        return completeness
    
    def analyze_uniqueness(self):
        """Analisa unicidade dos dados"""
        logger.info("Analyzing data uniqueness...")
        
        uniqueness = {
            'total_rows': len(self.df),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'columns': {}
        }
        
        for col in self.df.columns:
            unique_count = self.df[col].nunique()
            uniqueness['columns'][col] = {
                'unique_values': int(unique_count),
                'uniqueness_ratio': float(unique_count / len(self.df))
            }
        
        self.profile['uniqueness'] = uniqueness
        return uniqueness
    
    def analyze_distributions(self):
        """Analisa distribuições numéricas"""
        logger.info("Analyzing data distributions...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        distributions = {}
        
        for col in numeric_cols:
            distributions[col] = {
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'q25': float(self.df[col].quantile(0.25)),
                'q75': float(self.df[col].quantile(0.75)),
            }
        
        self.profile['distributions'] = distributions
        return distributions
    
    def detect_anomalies(self):
        """Detecta anomalias nos dados"""
        logger.info("Detecting anomalies...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        anomalies = {}
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[
                (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            ]
            
            anomalies[col] = {
                'outlier_count': len(outliers),
                'outlier_percentage': float(len(outliers) / len(self.df) * 100),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }
        
        self.profile['anomalies'] = anomalies
        return anomalies
    
    def calculate_quality_score(self):
        """Calcula score geral de qualidade"""
        logger.info("Calculating overall quality score...")
        
        # Peso para cada dimensão
        completeness_score = self.profile['completeness']['completeness_ratio'] * 0.30
        
        duplicate_ratio = (
            self.profile['uniqueness']['duplicate_rows'] / 
            self.profile['uniqueness']['total_rows']
        )
        uniqueness_score = (1 - duplicate_ratio) * 0.30
        
        # Score de anomalias (média de outliers)
        anomaly_scores = []
        for col, data in self.profile['anomalies'].items():
            anomaly_scores.append(1 - (data['outlier_percentage'] / 100))
        
        anomaly_score = np.mean(anomaly_scores) * 0.40 if anomaly_scores else 0.40
        
        total_score = completeness_score + uniqueness_score + anomaly_score
        
        self.profile['quality_score'] = {
            'overall': float(total_score),
            'completeness_contribution': float(completeness_score),
            'uniqueness_contribution': float(uniqueness_score),
            'anomaly_contribution': float(anomaly_score),
            'grade': self._get_grade(total_score)
        }
        
        return total_score
    
    def _get_grade(self, score):
        """Converte score em grade"""
        if score >= 0.95:
            return 'A+'
        elif score >= 0.90:
            return 'A'
        elif score >= 0.85:
            return 'B+'
        elif score >= 0.80:
            return 'B'
        elif score >= 0.75:
            return 'C+'
        elif score >= 0.70:
            return 'C'
        else:
            return 'F'
    
    def generate_report(self):
        """Gera relatório completo"""
        logger.info("Generating comprehensive report...")
        
        self.analyze_completeness()
        self.analyze_uniqueness()
        self.analyze_distributions()
        self.detect_anomalies()
        self.calculate_quality_score()
        
        self.profile['metadata'] = {
            'dataset_name': self.dataset_name,
            'generated_at': datetime.now().isoformat(),
            'row_count': len(self.df),
            'column_count': len(self.df.columns),
            'columns': list(self.df.columns),
            'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        }
        
        return self.profile
    
    def export_report(self, filepath='data_quality_report.json'):
        """Exporta relatório para JSON"""
        logger.info(f"Exporting report to {filepath}")
        
        with open(filepath, 'w') as f:
            json.dump(self.profile, f, indent=2)
        
        logger.info("Report exported successfully")
    
    def print_summary(self):
        """Imprime resumo do relatório"""
        print("\n" + "="*50)
        print(f"Data Quality Report: {self.dataset_name}")
        print("="*50)
        
        print(f"\nDataset: {self.profile['metadata']['row_count']} rows x {self.profile['metadata']['column_count']} columns")
        print(f"Overall Quality Score: {self.profile['quality_score']['overall']:.2%}")
        print(f"Grade: {self.profile['quality_score']['grade']}")
        
        print(f"\nCompleteness: {self.profile['completeness']['completeness_ratio']:.2%}")
        print(f"Null cells: {self.profile['completeness']['null_cells']:,}")
        
        print(f"\nDuplicate rows: {self.profile['uniqueness']['duplicate_rows']:,}")
        
        print("\nTop columns with null values:")
        null_cols = sorted(
            self.profile['completeness']['columns'].items(),
            key=lambda x: x[1]['null_percentage'],
            reverse=True
        )[:5]
        
        for col, data in null_cols:
            if data['null_percentage'] > 0:
                print(f"  - {col}: {data['null_percentage']:.2f}%")
        
        print("\nColumns with most outliers:")
        outlier_cols = sorted(
            self.profile['anomalies'].items(),
            key=lambda x: x[1]['outlier_percentage'],
            reverse=True
        )[:5]
        
        for col, data in outlier_cols:
            if data['outlier_percentage'] > 0:
                print(f"  - {col}: {data['outlier_percentage']:.2f}%")
        
        print("\n" + "="*50 + "\n")


def main():
    """Função principal para teste"""
    
    # Gera dados de exemplo
    np.random.seed(42)
    
    df = pd.DataFrame({
        'id': range(1, 1001),
        'value': np.random.normal(100, 15, 1000),
        'category': np.random.choice(['A', 'B', 'C', None], 1000, p=[0.4, 0.3, 0.2, 0.1]),
        'amount': np.random.uniform(10, 1000, 1000),
        'date': pd.date_range('2024-01-01', periods=1000, freq='H')
    })
    
    # Adiciona alguns outliers
    df.loc[np.random.choice(df.index, 20), 'value'] = np.random.uniform(200, 300, 20)
    
    # Adiciona duplicatas
    df = pd.concat([df, df.sample(10)])
    
    # Executa profiling
    profiler = DataProfiler(df, 'Example Dataset')
    report = profiler.generate_report()
    profiler.print_summary()
    profiler.export_report()


if __name__ == '__main__':
    main()
