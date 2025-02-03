import pandas as pd
from typing import Dict, Any, List
from agents.data_analyst import DataAnalystAgent
from agents.visualizer import VisualizerAgent
from agents.insight_generator import InsightGeneratorAgent
from agents.recommender import RecommenderAgent
from memory.memory_system import MemorySystem

class OrchestratorAgent:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        self.data_analyst = DataAnalystAgent()
        self.visualizer = VisualizerAgent()
        self.insight_generator = InsightGeneratorAgent()
        self.recommender = RecommenderAgent()
        self.memory = MemorySystem()
        self.name = "Orchestrator"
    
    def process_query(self, query: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Process user query and coordinate agents"""
        
        print(f"\n🤖 Orchestrator: Processing query: '{query}'")
        
        # Check memory for relevant past analyses
        relevant_memories = self.memory.get_relevant_memories(query)
        
        # Parse query and create execution plan
        plan = self._create_execution_plan(query, df)
        
        print(f"📋 Execution Plan: {plan['description']}")
        
        # Execute analysis
        analysis_results = {}
        agents_used = []
        
        for task in plan['tasks']:
            agent_name = task['agent']
            agents_used.append(agent_name)
            
            if agent_name == "DataAnalyst":
                print(f"  🔬 {agent_name}: {task['action']}")
                result = self.data_analyst.analyze(df, task['analysis_type'], **task.get('params', {}))
                analysis_results[task['analysis_type']] = result
            
            elif agent_name == "Visualizer":
                print(f"  📊 {agent_name}: {task['action']}")
                result = self.visualizer.create_visualization(df, task['viz_type'], **task.get('params', {}))
                analysis_results['visualization'] = result
        
        # Generate insights
        print(f"  💡 InsightGenerator: Generating insights")
        insights = self.insight_generator.generate_insights(analysis_results)
        
        # Generate recommendations
        print(f"  🎯 Recommender: Generating recommendations")
        recommendations = self.recommender.generate_recommendations(analysis_results, insights)
        
        # Store in memory
        self.memory.add_memory(query, agents_used, analysis_results, "\n".join(insights))
        
        # Compile final response
        response = {
            "query": query,
            "execution_plan": plan,
            "analysis_results": analysis_results,
            "insights": insights,
            "recommendations": recommendations,
            "agents_used": agents_used,
            "relevant_memories": relevant_memories
        }
        
        return response
    
    def _create_execution_plan(self, query: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Create execution plan based on query"""
        
        query_lower = query.lower()
        tasks = []
        
        # Always start with summary
        tasks.append({
            "agent": "DataAnalyst",
            "action": "Generate data summary",
            "analysis_type": "summary"
        })
        
        # Detect query intent
        if any(word in query_lower for word in ["trend", "time", "over time", "growth"]):
            # Find date and value columns
            date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            if not date_cols:
                date_cols = [col for col in df.columns if 'date' in col.lower()]
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if date_cols and numeric_cols:
                tasks.append({
                    "agent": "DataAnalyst",
                    "action": "Analyze trends",
                    "analysis_type": "trend",
                    "params": {"date_col": date_cols[0], "value_col": numeric_cols[0]}
                })
                
                tasks.append({
                    "agent": "Visualizer",
                    "action": "Create trend visualization",
                    "viz_type": "line",
                    "params": {
                        "x_col": date_cols[0],
                        "y_col": numeric_cols[0],
                        "title": f"{numeric_cols[0]} Trend Over Time"
                    }
                })
        
        if any(word in query_lower for word in ["correlation", "relationship", "related"]):
            tasks.append({
                "agent": "DataAnalyst",
                "action": "Analyze correlations",
                "analysis_type": "correlation"
            })
            
            tasks.append({
                "agent": "Visualizer",
                "action": "Create correlation heatmap",
                "viz_type": "heatmap",
                "params": {"title": "Correlation Matrix"}
            })
        
        if any(word in query_lower for word in ["group", "by", "category", "segment"]):
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if categorical_cols and numeric_cols:
                tasks.append({
                    "agent": "DataAnalyst",
                    "action": "Analyze by groups",
                    "analysis_type": "group",
                    "params": {"group_col": categorical_cols[0], "value_col": numeric_cols[0]}
                })
                
                # Create aggregated data for visualization
                group_data = df.groupby(categorical_cols[0])[numeric_cols[0]].mean().reset_index()
                
                tasks.append({
                    "agent": "Visualizer",
                    "action": "Create group comparison",
                    "viz_type": "bar",
                    "params": {
                        "x_col": categorical_cols[0],
                        "y_col": numeric_cols[0],
                        "title": f"{numeric_cols[0]} by {categorical_cols[0]}"
                    }
                })
        
        if any(word in query_lower for word in ["anomaly", "outlier", "unusual"]):
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                tasks.append({
                    "agent": "DataAnalyst",
                    "action": "Detect anomalies",
                    "analysis_type": "anomaly",
                    "params": {"column": numeric_cols[0]}
                })
        
        # If no specific intent, do comprehensive analysis
        if len(tasks) == 1:  # Only summary task
            tasks.append({
                "agent": "DataAnalyst",
                "action": "Analyze correlations",
                "analysis_type": "correlation"
            })
        
        return {
            "description": f"Execute {len(tasks)} analysis tasks",
            "tasks": tasks
        }
