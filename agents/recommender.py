from typing import Dict, Any, List

class RecommenderAgent:
    """Agent responsible for generating recommendations"""
    
    def __init__(self):
        self.name = "Recommender"
    
    def generate_recommendations(self, analysis_results: Dict[str, Any],
                                insights: List[str]) -> List[Dict[str, str]]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Based on summary
        if "summary" in analysis_results:
            recommendations.extend(self._recommend_from_summary(analysis_results["summary"]))
        
        # Based on correlation
        if "correlation" in analysis_results:
            recommendations.extend(self._recommend_from_correlation(analysis_results["correlation"]))
        
        # Based on trend
        if "trend" in analysis_results:
            recommendations.extend(self._recommend_from_trend(analysis_results["trend"]))
        
        # Based on anomalies
        if "anomaly" in analysis_results:
            recommendations.extend(self._recommend_from_anomaly(analysis_results["anomaly"]))
        
        # Prioritize recommendations
        return self._prioritize_recommendations(recommendations)
    
    def _recommend_from_summary(self, summary: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommendations from summary"""
        recommendations = []
        
        missing = summary.get("missing_values", {})
        total_missing = sum(missing.values())
        
        if total_missing > 0:
            recommendations.append({
                "priority": "high",
                "action": "Data Quality",
                "recommendation": "Address missing values through imputation or collection of additional data"
            })
        
        return recommendations
    
    def _recommend_from_correlation(self, correlation: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommendations from correlation"""
        recommendations = []
        
        strong_corr = correlation.get("strong_correlations", [])
        
        if strong_corr:
            recommendations.append({
                "priority": "medium",
                "action": "Feature Engineering",
                "recommendation": "Leverage strong correlations for predictive modeling or feature selection"
            })
        
        return recommendations
    
    def _recommend_from_trend(self, trend: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommendations from trend"""
        recommendations = []
        
        trend_analysis = trend.get("trend_analysis", {})
        growth_analysis = trend.get("growth_analysis", {})
        
        trend_direction = trend_analysis.get("trend", "stable")
        growth_pct = growth_analysis.get("total_growth_percent", 0)
        
        if trend_direction == "increasing" and growth_pct > 20:
            recommendations.append({
                "priority": "high",
                "action": "Capitalize on Growth",
                "recommendation": "Strong positive trend detected - consider scaling operations or investments"
            })
        elif trend_direction == "decreasing" and growth_pct < -20:
            recommendations.append({
                "priority": "high",
                "action": "Address Decline",
                "recommendation": "Negative trend detected - investigate root causes and implement corrective measures"
            })
        
        return recommendations
    
    def _recommend_from_anomaly(self, anomaly: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommendations from anomaly detection"""
        recommendations = []
        
        count = anomaly.get("anomaly_count", 0)
        percentage = anomaly.get("anomaly_percentage", 0)
        
        if percentage > 5:
            recommendations.append({
                "priority": "high",
                "action": "Investigate Anomalies",
                "recommendation": f"High anomaly rate ({percentage:.1f}%) - investigate data quality or unusual events"
            })
        elif count > 0:
            recommendations.append({
                "priority": "low",
                "action": "Monitor Outliers",
                "recommendation": "Review detected anomalies for potential opportunities or issues"
            })
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Sort recommendations by priority"""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(recommendations, key=lambda x: priority_order.get(x["priority"], 3))
