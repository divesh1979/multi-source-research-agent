import pytest
from pathlib import Path
from schemas.output_models import ResearchReport, SourceCitation, KeyFinding, SentimentOverview
from tools.google_search import execute_google_search
from tools.reddit_search import execute_reddit_search
from tools.brightdata_scraper import SnapshotManager
from agent.graph import agent_app

def test_pydantic_output_schemas():
    """Test Pydantic data model instantiation and type validation."""
    citation = SourceCitation(
        source_id="SRC-01",
        title="Test Citation",
        url="https://example.com",
        platform="Google Search",
        relevance_score=0.95
    )
    assert citation.source_id == "SRC-01"
    assert citation.relevance_score == 0.95

    report = ResearchReport(
        topic="Test Topic",
        executive_summary="Test Summary",
        key_findings=[],
        sentiment_analysis=SentimentOverview(
            overall_sentiment="Positive",
            community_consensus="Consensus",
            expert_perspective="Expert",
            controversies_or_risks=[]
        ),
        detailed_analysis="## Detailed Analysis",
        citations=[citation],
        methodology="Test Methodology"
    )
    assert report.topic == "Test Topic"
    assert len(report.citations) == 1

def test_google_search_tool():
    """Test Google Search tool execution and output schema."""
    results = execute_google_search("LangGraph python benchmarks")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "url" in results[0]

def test_reddit_search_tool():
    """Test Reddit search tool execution."""
    results = execute_reddit_search("LangGraph state graph")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "subreddit" in results[0]

def test_snapshot_manager(tmp_path):
    """Test SnapshotManager HTML-to-Markdown cleaning and snapshot file saving."""
    manager = SnapshotManager(snapshot_dir=tmp_path)
    raw_html = "<html><head><title>Test Page</title></head><body><h1>Header</h1><p>Main content paragraph here.</p></body></html>"
    markdown = manager.html_to_clean_markdown(raw_html, "https://example.com/test")
    
    assert "# Test Page" in markdown
    assert "Main content paragraph here." in markdown
    
    snapshot = manager.save_snapshot("https://example.com/test", markdown)
    assert Path(snapshot["filepath"]).exists()

def test_langgraph_workflow_execution():
    """Test full end-to-end LangGraph StateGraph execution."""
    initial_state = {
        "original_query": "LangGraph multi-source research agent",
        "expanded_queries": [],
        "google_results": [],
        "reddit_results": [],
        "scraped_snapshots": [],
        "aggregated_context": "",
        "final_report": None,
        "execution_logs": [],
        "error_count": 0
    }
    
    final_state = agent_app.invoke(initial_state)
    assert "final_report" in final_state
    assert final_state["final_report"] is not None
    assert final_state["final_report"]["topic"] == "LangGraph multi-source research agent"
