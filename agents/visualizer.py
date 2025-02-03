import pandas as pd
from typing import Dict, Any, Optional
from tools.viz_tools import VizTools

class VisualizerAgent:
    """Agent responsible for creating visualizations"""
    
    def __init__(self):
        self.viz_tools = VizTools()
        self.name = "Visualizer"
    
    def create_visualization(self, df: pd.DataFrame, viz_type: str, **kwargs) -> Dict[str, Any]:
        """Create visualization based on type"""
        
        try:
            if viz_type == "line":
                fig = self.viz_tools.create_line_chart(df, **kwargs)
            
            elif viz_type == "bar":
                fig = self.viz_tools.create_bar_chart(df, **kwargs)
            
            elif viz_type == "scatter":
                fig = self.viz_tools.create_scatter_plot(df, **kwargs)
            
            elif viz_type == "heatmap":
                fig = self.viz_tools.create_heatmap(df, **kwargs)
            
            elif viz_type == "distribution":
                fig = self.viz_tools.create_distribution_plot(df, **kwargs)
            
            else:
                return {"error": f"Unknown visualization type: {viz_type}"}
            
            return {
                "status": "success",
                "viz_type": viz_type,
                "figure": fig
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def suggest_visualization(self, df: pd.DataFrame, analysis_goal: str) -> str:
        """Suggest appropriate visualization type"""
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if "trend" in analysis_goal.lower() or "time" in analysis_goal.lower():
            return "line"
        
        elif "correlation" in analysis_goal.lower():
            return "heatmap"
        
        elif "distribution" in analysis_goal.lower():
            return "distribution"
        
        elif "compare" in analysis_goal.lower() or "comparison" in analysis_goal.lower():
            return "bar"
        
        elif len(numeric_cols) >= 2:
            return "scatter"
        
        else:
            return "bar"
