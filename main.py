import sys
import argparse
import logging
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from agent.graph import agent_app

logging.basicConfig(level=logging.ERROR)
console = Console()

def run_cli_research(query: str):
    console.print(Panel.fit(
        f"[bold cyan]Advanced AI Multi-Source Research Agent[/bold cyan]\n"
        f"[yellow]Topic:[/yellow] {query}\n"
        f"[dim]LangGraph Parallel Workflows • Google • Reddit • BrightData Scraper • GPT-4o[/dim]",
        title="🤖 AI Research Agent",
        border_style="cyan"
    ))

    initial_state = {
        "original_query": query,
        "expanded_queries": [],
        "google_results": [],
        "reddit_results": [],
        "scraped_snapshots": [],
        "aggregated_context": "",
        "final_report": None,
        "execution_logs": [],
        "error_count": 0
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Executing parallel LangGraph workflow...", total=None)
        
        # Execute compiled LangGraph application
        final_state = agent_app.invoke(initial_state)
        progress.update(task, completed=True)

    report = final_state.get("final_report", {})
    if not report:
        console.print("[bold red]Failed to generate research report.[/bold red]")
        return

    # Print Executive Summary
    console.print("\n", Panel(
        report.get("executive_summary", ""),
        title="📋 Executive Summary",
        border_style="green"
    ))

    # Print Key Findings Table
    findings_table = Table(title="🔍 Empirical Key Findings", border_style="yellow")
    findings_table.add_column("Title", style="bold yellow")
    findings_table.add_column("Finding", style="white")
    findings_table.add_column("Confidence", style="bold green", justify="center")
    findings_table.add_column("Citations", style="dim cyan")

    for finding in report.get("key_findings", []):
        findings_table.add_row(
            finding.get("title", ""),
            finding.get("description", ""),
            finding.get("confidence", "High"),
            ", ".join(finding.get("citation_ids", []))
        )
    console.print(findings_table)

    # Print Multi-Source Sentiment
    sentiment = report.get("sentiment_analysis", {})
    console.print(Panel(
        f"[bold]Overall Sentiment:[/bold] {sentiment.get('overall_sentiment')}\n"
        f"[bold]Community Consensus (Reddit):[/bold] {sentiment.get('community_consensus')}\n"
        f"[bold]Expert Perspective (Google/Docs):[/bold] {sentiment.get('expert_perspective')}",
        title="📊 Multi-Source Sentiment Analysis",
        border_style="magenta"
    ))

    # Print Detailed Analysis Markdown
    console.print(Panel(
        Markdown(report.get("detailed_analysis", "")),
        title="📄 Detailed Analysis Report",
        border_style="blue"
    ))

    # Print Source Citations
    citations_table = Table(title="📚 Verified Source Bibliography", border_style="cyan")
    citations_table.add_column("ID", style="bold cyan")
    citations_table.add_column("Platform", style="green")
    citations_table.add_column("Title", style="white")
    citations_table.add_column("URL", style="dim underline blue")

    for cite in report.get("citations", []):
        citations_table.add_row(
            cite.get("source_id", ""),
            cite.get("platform", ""),
            cite.get("title", ""),
            cite.get("url", "")
        )
    console.print(citations_table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced AI Web Agent for Multi-Source Research")
    parser.add_argument("--query", type=str, default="DeepSeek-R1 vs GPT-4o architecture comparison for agentic coding", help="Research topic prompt")
    args = parser.parse_args()
    
    run_cli_research(args.query)
