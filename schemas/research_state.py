from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    """
    LangGraph AgentState schema representing state propagation through parallel research nodes.
    Uses Annotated reducers to safely aggregate results from concurrent execution nodes.
    """
    original_query: str
    expanded_queries: List[str]
    
    # Reducers for parallel fan-in nodes
    google_results: Annotated[List[Dict[str, Any]], operator.add]
    reddit_results: Annotated[List[Dict[str, Any]], operator.add]
    scraped_snapshots: Annotated[List[Dict[str, Any]], operator.add]
    
    # Aggregated & Final Outputs
    aggregated_context: Optional[str]
    final_report: Optional[Dict[str, Any]]
    execution_logs: Annotated[List[str], operator.add]
    error_count: int
