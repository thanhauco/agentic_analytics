import pandas as pd
import numpy as np
from typing import Union, Dict, Any

class DataTools:
    """Tools for data loading and preprocessing"""
    
    @staticmethod
    def load_data(source: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """Load data from various sources"""
        if isinstance(source, pd.DataFrame):
            return source
        elif isinstance(source, str):
            if source.endswith('.csv'):
                return pd.read_csv(source)
            elif source.endswith('.json'):
                return pd.read_json(source)
            elif source.endswith(('.xls', '.xlsx')):
                return pd.read_excel(source)
        raise ValueError(f"Unsupported data source: {source}")
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """Get comprehensive data summary"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning"""
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Fill numeric missing values with median
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
        
        # Fill categorical missing values with mode
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown', inplace=True)
        
        return df_clean
    
    @staticmethod
    def generate_sample_data(rows: int = 1000) -> pd.DataFrame:
        """Generate sample sales data for testing"""
        np.random.seed(42)
        
        dates = pd.date_range('2024-01-01', periods=rows, freq='D')
        products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
        regions = ['North', 'South', 'East', 'West']
        
        data = {
            'date': np.random.choice(dates, rows),
            'product': np.random.choice(products, rows),
            'region': np.random.choice(regions, rows),
            'sales': np.random.randint(100, 10000, rows),
            'quantity': np.random.randint(1, 100, rows),
            'customer_satisfaction': np.random.uniform(1, 5, rows)
        }
        
        df = pd.DataFrame(data)
        df['revenue'] = df['sales'] * np.random.uniform(0.8, 1.2, rows)
        
        return df
