import logging
from langgraph.graph import StateGraph, END
from schemas.research_state import AgentState
from agent.nodes import (
    planner_node,
    google_node,
    reddit_node,
    scraping_node,
    aggregate_node,
    synthesis_node
)

logger = logging.getLogger(__name__)

def build_research_graph():
    """
    Constructs and compiles the parallel multi-source LangGraph StateGraph.
    
    Graph Topology:
        [START] -> planner_node
                     |
                     +---> google_node -------+
                     |                        |
                     +---> reddit_node -------+---> aggregate_node -> synthesis_node -> [END]
                     |                        |
                     +---> scraping_node -----+
    """
    workflow = StateGraph(AgentState)
    
    # Register Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("google", google_node)
    workflow.add_node("reddit", reddit_node)
    workflow.add_node("scraping", scraping_node)
    workflow.add_node("aggregate", aggregate_node)
    workflow.add_node("synthesis", synthesis_node)
    
    # Set Entry Point
    workflow.set_entry_point("planner")
    
    # Parallel Fan-Out Edges from Planner Node
    workflow.add_edge("planner", "google")
    workflow.add_edge("planner", "reddit")
    workflow.add_edge("planner", "scraping")
    
    # Fan-In Edges from Parallel Sources to Aggregator Node
    workflow.add_edge("google", "aggregate")
    workflow.add_edge("reddit", "aggregate")
    workflow.add_edge("scraping", "aggregate")
    
    # Sequential Final Synthesis Pipeline
    workflow.add_edge("aggregate", "synthesis")
    workflow.add_edge("synthesis", END)
    
    # Compile StateGraph
    research_agent_app = workflow.compile()
    logger.info("LangGraph multi-source research agent graph successfully compiled.")
    return research_agent_app

# Expose compiled application instance
agent_app = build_research_graph()
