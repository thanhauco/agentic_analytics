import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, List, Tuple

class AnalysisTools:
    """Tools for statistical analysis"""
    
    @staticmethod
    def descriptive_statistics(df: pd.DataFrame, column: str) -> Dict[str, float]:
        """Calculate descriptive statistics for a column"""
        series = df[column]
        return {
            "mean": series.mean(),
            "median": series.median(),
            "std": series.std(),
            "min": series.min(),
            "max": series.max(),
            "q25": series.quantile(0.25),
            "q75": series.quantile(0.75),
            "skewness": series.skew(),
            "kurtosis": series.kurtosis()
        }
    
    @staticmethod
    def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.corr()
    
    @staticmethod
    def trend_analysis(df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, Any]:
        """Analyze trends over time"""
        df_sorted = df.sort_values(date_col)
        
        # Convert dates to numeric for regression
        df_sorted['date_numeric'] = pd.to_datetime(df_sorted[date_col]).astype(np.int64) // 10**9
        
        X = df_sorted['date_numeric'].values.reshape(-1, 1)
        y = df_sorted[value_col].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        trend = "increasing" if model.coef_[0] > 0 else "decreasing"
        
        return {
            "trend": trend,
            "slope": float(model.coef_[0]),
            "intercept": float(model.intercept_),
            "r_squared": float(model.score(X, y))
        }
    
    @staticmethod
    def detect_anomalies(df: pd.DataFrame, column: str, threshold: float = 3.0) -> List[int]:
        """Detect anomalies using z-score method"""
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        anomaly_indices = np.where(z_scores > threshold)[0]
        return anomaly_indices.tolist()
    
    @staticmethod
    def group_analysis(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
        """Perform group-wise analysis"""
        return df.groupby(group_col)[value_col].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
    
    @staticmethod
    def calculate_growth_rate(df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, float]:
        """Calculate growth rates"""
        df_sorted = df.sort_values(date_col)
        
        first_value = df_sorted[value_col].iloc[0]
        last_value = df_sorted[value_col].iloc[-1]
        
        total_growth = ((last_value - first_value) / first_value) * 100
        
        return {
            "total_growth_percent": round(total_growth, 2),
            "first_value": float(first_value),
            "last_value": float(last_value)
        }
