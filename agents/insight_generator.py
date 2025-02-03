from typing import Dict, Any, List

class InsightGeneratorAgent:
    """Agent responsible for generating natural language insights"""
    
    def __init__(self):
        self.name = "InsightGenerator"
    
    def generate_insights(self, analysis_results: Dict[str, Any], 
                         context: str = "") -> List[str]:
        """Generate insights from analysis results"""
        
        insights = []
        
        # Summary insights
        if "summary" in analysis_results:
            insights.extend(self._generate_summary_insights(analysis_results["summary"]))
        
        # Correlation insights
        if "correlation" in analysis_results:
            insights.extend(self._generate_correlation_insights(analysis_results["correlation"]))
        
        # Trend insights
        if "trend" in analysis_results:
            insights.extend(self._generate_trend_insights(analysis_results["trend"]))
        
        # Group insights
        if "group" in analysis_results:
            insights.extend(self._generate_group_insights(analysis_results["group"]))
        
        # Anomaly insights
        if "anomaly" in analysis_results:
            insights.extend(self._generate_anomaly_insights(analysis_results["anomaly"]))
        
        return insights
    
    def _generate_summary_insights(self, summary: Dict[str, Any]) -> List[str]:
        """Generate insights from summary statistics"""
        insights = []
        
        shape = summary.get("shape", (0, 0))
        insights.append(f"📊 Dataset contains {shape[0]:,} rows and {shape[1]} columns")
        
        missing = summary.get("missing_values", {})
        total_missing = sum(missing.values())
        if total_missing > 0:
            insights.append(f"⚠️ Found {total_missing:,} missing values across the dataset")
        
        return insights
    
    def _generate_correlation_insights(self, correlation: Dict[str, Any]) -> List[str]:
        """Generate insights from correlation analysis"""
        insights = []
        
        strong_corr = correlation.get("strong_correlations", [])
        if strong_corr:
            for corr in strong_corr[:3]:  # Top 3
                direction = "positive" if corr["correlation"] > 0 else "negative"
                insights.append(
                    f"🔗 Strong {direction} correlation ({corr['correlation']:.2f}) "
                    f"between {corr['var1']} and {corr['var2']}"
                )
        else:
            insights.append("📉 No strong correlations detected between variables")
        
        return insights
    
    def _generate_trend_insights(self, trend: Dict[str, Any]) -> List[str]:
        """Generate insights from trend analysis"""
        insights = []
        
        trend_analysis = trend.get("trend_analysis", {})
        growth_analysis = trend.get("growth_analysis", {})
        
        trend_direction = trend_analysis.get("trend", "stable")
        r_squared = trend_analysis.get("r_squared", 0)
        
        insights.append(f"📈 Data shows an {trend_direction} trend (R² = {r_squared:.3f})")
        
        growth_pct = growth_analysis.get("total_growth_percent", 0)
        if abs(growth_pct) > 10:
            direction = "increased" if growth_pct > 0 else "decreased"
            insights.append(f"💹 Overall {direction} by {abs(growth_pct):.1f}%")
        
        return insights
    
    def _generate_group_insights(self, group: Dict[str, Any]) -> List[str]:
        """Generate insights from group analysis"""
        insights = []
        
        best = group.get("best_performing")
        worst = group.get("worst_performing")
        
        if best and worst:
            insights.append(f"🏆 Best performing group: {best}")
            insights.append(f"📉 Lowest performing group: {worst}")
        
        return insights
    
    def _generate_anomaly_insights(self, anomaly: Dict[str, Any]) -> List[str]:
        """Generate insights from anomaly detection"""
        insights = []
        
        count = anomaly.get("anomaly_count", 0)
        percentage = anomaly.get("anomaly_percentage", 0)
        
        if count > 0:
            insights.append(f"🚨 Detected {count} anomalies ({percentage:.1f}% of data)")
        else:
            insights.append("✅ No significant anomalies detected")
        
        return insights
