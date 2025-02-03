import pandas as pd
from agents.orchestrator import OrchestratorAgent
from tools.data_tools import DataTools
from config import Config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def print_results(response):
    """Pretty print analysis results"""
    
    print("\n" + "="*80)
    print("📊 AGENTIC ANALYTICS REPORT")
    print("="*80)
    
    print(f"\n🔍 Query: {response['query']}")
    
    print(f"\n🤖 Agents Used: {', '.join(response['agents_used'])}")
    
    print("\n💡 KEY INSIGHTS:")
    print("-" * 80)
    for i, insight in enumerate(response['insights'], 1):
        print(f"{i}. {insight}")
    
    print("\n🎯 RECOMMENDATIONS:")
    print("-" * 80)
    for i, rec in enumerate(response['recommendations'], 1):
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "⚪")
        print(f"{i}. {priority_emoji} [{rec['priority'].upper()}] {rec['action']}")
        print(f"   → {rec['recommendation']}\n")
    
    if response.get('relevant_memories'):
        print("\n🧠 RELEVANT PAST ANALYSES:")
        print("-" * 80)
        for memory in response['relevant_memories']:
            print(f"  • {memory['query']}")
    
    print("\n" + "="*80)

def main():
    """Main execution function"""
    
    print("🚀 Initializing Agentic Analytics System...")
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent()
    
    # Generate or load sample data
    print("\n📁 Loading sample data...")
    data_tools = DataTools()
    df = data_tools.generate_sample_data(rows=1000)
    
    print(f"✅ Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
    
    # Example queries
    queries = [
        "Analyze sales trends over time",
        "What are the correlations between different metrics?",
        "Compare performance by region",
        "Detect any anomalies in the sales data"
    ]
    
    print("\n" + "="*80)
    print("🎯 RUNNING AGENTIC ANALYTICS")
    print("="*80)
    
    # Process each query
    for i, query in enumerate(queries, 1):
        print(f"\n\n{'='*80}")
        print(f"QUERY {i}/{len(queries)}")
        print(f"{'='*80}")
        
        response = orchestrator.process_query(query, df)
        print_results(response)
        
        # Show visualization if created
        if 'visualization' in response['analysis_results']:
            viz_result = response['analysis_results']['visualization']
            if viz_result.get('status') == 'success':
                # In a real app we might save or display differently, here we just note it
                print("Visualization created successfully.")
                # plt.show() # Commented out to avoid blocking execution in non-interactive env
    
    # Display memory statistics
    print("\n\n" + "="*80)
    print("🧠 MEMORY SYSTEM STATISTICS")
    print("="*80)
    
    stats = orchestrator.memory.get_statistics()
    print(f"\nTotal Queries Processed: {stats['total_queries']}")
    print(f"\nAgent Usage:")
    for agent, count in stats['agents_usage'].items():
        print(f"  • {agent}: {count} times")
    
    print("\n✅ Agentic Analytics Complete!")

if __name__ == "__main__":
    main()
