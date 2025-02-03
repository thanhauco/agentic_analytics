# Agentic Analytics System

## Overview
The Agentic Analytics system is an autonomous AI analytics agent that can analyze data, generate insights, create visualizations, and make data-driven recommendations.

## Architecture

### Core Components
- **Memory System**: Stores and retrieves past analyses for continuous learning
- **Tools**: Data processing, statistical analysis, and visualization capabilities
- **Agents**: Specialized agents working collaboratively
  - **DataAnalyst**: Performs statistical analysis and data processing
  - **Visualizer**: Creates charts and visual representations
  - **InsightGenerator**: Generates natural language insights
  - **Recommender**: Provides actionable recommendations
  - **Orchestrator**: Coordinates all agents and manages workflow

## Features

✅ Multi-agent collaboration  
✅ Autonomous decision-making  
✅ Self-improving through memory  
✅ Natural language interface  
✅ Automated visualization  
✅ Statistical analysis  
✅ Predictive insights

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the main application to see the system in action:

```bash
python main.py
```

The system will:
1. Load sample data
2. Process multiple analytical queries
3. Generate insights and recommendations
4. Store results in memory for future reference

## Example Queries

The system can handle various types of analytical queries:

- **Trend Analysis**: "Analyze sales trends over time"
- **Correlation Analysis**: "What are the correlations between different metrics?"
- **Group Comparison**: "Compare performance by region"
- **Anomaly Detection**: "Detect any anomalies in the sales data"

## Verification Results

The system was successfully verified with the following capabilities:

1. **Analyze sales trends over time**
   - Analyzed trends and created trend visualizations
   - Detected growth rates and patterns
   - Provided actionable recommendations

2. **Correlation analysis**
   - Calculated correlation matrix and created heatmaps
   - Identified strong correlations (e.g., between sales and revenue)
   - Suggested feature engineering opportunities

3. **Performance comparison**
   - Grouped data by categories and compared metrics
   - Identified best and worst performing groups

4. **Anomaly detection**
   - Detected anomalies using z-score method
   - Reported anomaly counts and percentages
   - Recommended investigation when needed

## Memory System

The memory system stores all past analyses and can retrieve relevant historical context for new queries, enabling the system to learn and improve over time.

## Project Structure

```
agentic_analytics/
├── agents/              # Specialized AI agents
├── tools/               # Data processing and analysis tools
├── memory/              # Memory system for learning
├── config.py            # Configuration settings
├── main.py              # Main application
└── requirements.txt     # Project dependencies
```

## License

This project demonstrates an autonomous agentic analytics system following Nov 2025 best practices.
