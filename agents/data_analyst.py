import pandas as pd
from typing import Dict, Any
from tools.data_tools import DataTools
from tools.analysis_tools import AnalysisTools

class DataAnalystAgent:
    """Agent responsible for data analysis tasks"""
    
    def __init__(self):
        self.data_tools = DataTools()
        self.analysis_tools = AnalysisTools()
        self.name = "DataAnalyst"
    
    def analyze(self, df: pd.DataFrame, analysis_type: str, **kwargs) -> Dict[str, Any]:
        """Perform analysis based on type"""
        
        if analysis_type == "summary":
            return self._analyze_summary(df)
        
        elif analysis_type == "correlation":
            return self._analyze_correlation(df)
        
        elif analysis_type == "trend":
            return self._analyze_trend(df, **kwargs)
        
        elif analysis_type == "group":
            return self._analyze_groups(df, **kwargs)
        
        elif analysis_type == "anomaly":
            return self._detect_anomalies(df, **kwargs)
        
        else:
            return {"error": f"Unknown analysis type: {analysis_type}"}
    
    def _analyze_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate data summary"""
        summary = self.data_tools.get_data_summary(df)
        
        # Add descriptive stats for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        stats = {}
        for col in numeric_cols:
            stats[col] = self.analysis_tools.descriptive_statistics(df, col)
        
        summary['detailed_statistics'] = stats
        return summary
    
    def _analyze_correlation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations"""
        corr_matrix = self.analysis_tools.correlation_analysis(df)
        
        # Find strong correlations
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_corr.append({
                        "var1": corr_matrix.columns[i],
                        "var2": corr_matrix.columns[j],
                        "correlation": round(corr_value, 3)
                    })
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_corr
        }
    
    def _analyze_trend(self, df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, Any]:
        """Analyze trends"""
        trend_result = self.analysis_tools.trend_analysis(df, date_col, value_col)
        growth_result = self.analysis_tools.calculate_growth_rate(df, date_col, value_col)
        
        return {
            "trend_analysis": trend_result,
            "growth_analysis": growth_result
        }
    
    def _analyze_groups(self, df: pd.DataFrame, group_col: str, value_col: str) -> Dict[str, Any]:
        """Analyze by groups"""
        group_stats = self.analysis_tools.group_analysis(df, group_col, value_col)
        
        return {
            "group_statistics": group_stats.to_dict(),
            "best_performing": group_stats['mean'].idxmax(),
            "worst_performing": group_stats['mean'].idxmin()
        }
    
    def _detect_anomalies(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Detect anomalies"""
        anomaly_indices = self.analysis_tools.detect_anomalies(df, column)
        
        return {
            "anomaly_count": len(anomaly_indices),
            "anomaly_indices": anomaly_indices,
            "anomaly_percentage": round(len(anomaly_indices) / len(df) * 100, 2)
        }
