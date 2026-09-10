from typing import List, Optional
from pydantic import BaseModel, Field

class SourceCitation(BaseModel):
    """Citation metadata for verified multi-source research items."""
    source_id: str = Field(..., description="Unique reference ID (e.g. SRC-01)")
    title: str = Field(..., description="Article, thread, or document title")
    url: str = Field(..., description="Direct HTTP URL to source")
    platform: str = Field(..., description="Source origin platform (e.g. Google, Reddit, Web Scrape)")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score from 0.0 to 1.0")

class KeyFinding(BaseModel):
    """Extracted key empirical insight with source backing."""
    title: str = Field(..., description="Concise statement of finding")
    description: str = Field(..., description="Detailed explanation of finding")
    supporting_evidence: str = Field(..., description="Direct quote or metric from source data")
    confidence: str = Field(..., description="Confidence level: High, Medium, or Low")
    citation_ids: List[str] = Field(default_factory=list, description="IDs of backing citations")

class SentimentOverview(BaseModel):
    """Community consensus vs expert sentiment analysis."""
    overall_sentiment: str = Field(..., description="Positive, Negative, Mixed, or Neutral")
    community_consensus: str = Field(..., description="Summary of community opinions (e.g. Reddit discussions)")
    expert_perspective: str = Field(..., description="Summary of official / documentation / web findings")
    controversies_or_risks: List[str] = Field(default_factory=list, description="Identified trade-offs or debate points")

class ResearchReport(BaseModel):
    """Structured Pydantic model for complete AI multi-source research output."""
    topic: str = Field(..., description="Research topic or user prompt")
    executive_summary: str = Field(..., description="High-level 3-4 sentence overview synthesized by GPT-4o")
    key_findings: List[KeyFinding] = Field(..., description="Structured findings extracted across platforms")
    sentiment_analysis: SentimentOverview = Field(..., description="Multi-source sentiment breakdown")
    detailed_analysis: str = Field(..., description="Comprehensive synthesized markdown research report")
    citations: List[SourceCitation] = Field(..., description="Complete list of source citations")
    methodology: str = Field(..., description="Explanation of parallel data collection and LLM validation process")
