import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd
import numpy as np

class MemorySystem:
    """Stores and retrieves agent interactions and learnings"""
    
    def __init__(self, memory_file: str = "agent_memory.json", max_size: int = 100):
        self.memory_file = Path(memory_file)
        self.max_size = max_size
        self.memories: List[Dict[str, Any]] = []
        self.load_memory()
    
    def load_memory(self):
        """Load memories from file"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                self.memories = json.load(f)
    
    def save_memory(self):
        """Save memories to file"""
        
        class NumpyEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (np.int64, np.int32, np.int16, np.int8,
                                  np.uint64, np.uint32, np.uint16, np.uint8)):
                    return int(obj)
                elif isinstance(obj, (np.float64, np.float32, np.float16)):
                    return float(obj)
                elif isinstance(obj, (np.ndarray,)):
                    return obj.tolist()
                elif isinstance(obj, (np.bool_)):
                    return bool(obj)
                elif isinstance(obj, (np.datetime64, pd.Timestamp)):
                    return str(obj)
                elif hasattr(obj, 'dtype') and 'datetime64' in str(obj.dtype):
                    return str(obj)
                elif isinstance(obj, np.dtype):
                    return str(obj)
                elif hasattr(obj, 'savefig'):  # Simple check for matplotlib Figure
                    return "Matplotlib Figure"
                return json.JSONEncoder.default(self, obj)

        with open(self.memory_file, 'w') as f:
            json.dump(self.memories[-self.max_size:], f, indent=2, cls=NumpyEncoder)
    
    def add_memory(self, query: str, agents_used: List[str], 
                   results: Dict[str, Any], insights: str):
        """Add a new memory entry"""
        memory = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "agents_used": agents_used,
            "results": results,
            "insights": insights
        }
        self.memories.append(memory)
        self.save_memory()
    
    def get_relevant_memories(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant past memories (simple keyword matching)"""
        query_words = set(query.lower().split())
        scored_memories = []
        
        for memory in self.memories:
            memory_words = set(memory['query'].lower().split())
            score = len(query_words & memory_words)
            if score > 0:
                scored_memories.append((score, memory))
        
        scored_memories.sort(reverse=True, key=lambda x: x[0])
        return [m[1] for m in scored_memories[:top_k]]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_queries": len(self.memories),
            "agents_usage": self._count_agent_usage(),
            "recent_queries": [m['query'] for m in self.memories[-5:]]
        }
    
    def _count_agent_usage(self) -> Dict[str, int]:
        """Count how many times each agent was used"""
        usage = {}
        for memory in self.memories:
            for agent in memory['agents_used']:
                usage[agent] = usage.get(agent, 0) + 1
        return usage
