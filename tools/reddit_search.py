import logging
from typing import List, Dict, Any
import httpx
from config import settings

logger = logging.getLogger(__name__)

def execute_reddit_search(query: str, max_posts: int = None) -> List[Dict[str, Any]]:
    """
    Retrieves relevant Reddit discussions, top comments, and community sentiments.
    Integrates via PRAW or public Reddit JSON endpoints, with deterministic mock fallback.
    """
    limit = max_posts or settings.max_reddit_posts
    results: List[Dict[str, Any]] = []

    # 1. PRAW API integration if credentials are present
    if settings.reddit_client_id and settings.reddit_client_secret:
        try:
            import praw
            reddit = praw.Reddit(
                client_id=settings.reddit_client_id,
                client_secret=settings.reddit_client_secret,
                user_agent=settings.reddit_user_agent
            )
            for submission in reddit.subreddit("all").search(query, limit=limit):
                submission.comments.replace_more(limit=0)
                top_comments = [c.body for c in submission.comments[:3]]
                results.append({
                    "platform": "Reddit",
                    "title": submission.title,
                    "author": str(submission.author),
                    "subreddit": submission.subreddit.display_name,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "body": submission.selftext[:500],
                    "top_comments": top_comments,
                    "url": f"https://reddit.com{submission.permalink}",
                    "source": "Reddit PRAW API"
                })
            if results:
                return results
        except Exception as e:
            logger.warning(f"PRAW API failed: {e}. Attempting public JSON endpoints.")

    # 2. Public Reddit JSON API Endpoint
    try:
        encoded_query = httpx.URL(query).raw_path.decode('utf-8')
        url = f"https://www.reddit.com/search.json?q={query}&limit={limit}&sort=relevance"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) MultiSourceAgent/1.0"}
        response = httpx.get(url, headers=headers, timeout=8.0)
        if response.status_code == 200:
            data = response.json()
            posts = data.get("data", {}).get("children", [])
            for post in posts:
                pdata = post.get("data", {})
                results.append({
                    "platform": "Reddit",
                    "title": pdata.get("title", ""),
                    "subreddit": pdata.get("subreddit", ""),
                    "score": pdata.get("score", 0),
                    "num_comments": pdata.get("num_comments", 0),
                    "body": pdata.get("selftext", "")[:400],
                    "url": f"https://reddit.com{pdata.get('permalink', '')}",
                    "source": "Reddit Public JSON API"
                })
            if results:
                return results
    except Exception as e:
        logger.warning(f"Reddit JSON endpoint failed: {e}")

    # 3. Deterministic Mock Fallback dataset
    return [
        {
            "platform": "Reddit",
            "title": f"r/LocalLLaMA - Community consensus & hands-on experience with {query}",
            "subreddit": "LocalLLaMA",
            "score": 482,
            "num_comments": 124,
            "body": f"We've been testing {query} in production for 3 weeks. Here are our findings: throughput is outstanding, but prompt structuring requires Pydantic models for clean json outputs. Anyone else experienced latency spikes under concurrency?",
            "top_comments": [
                "Agreed on the structured output point. Using instructor or LangChain output parsers completely fixed our validation errors.",
                "Great benchmark post! We saw a 35% reduction in hallucination rates when combining search scrapers with parallel graph nodes."
            ],
            "url": "https://reddit.com/r/LocalLLaMA/comments/tech_discussion_01",
            "source": "Mock Reddit Endpoint"
        },
        {
            "platform": "Reddit",
            "title": f"r/MachineLearning - Trade-offs and empirical comparisons for {query}",
            "subreddit": "MachineLearning",
            "score": 890,
            "num_comments": 210,
            "body": f"Comparing current SOTA approaches to {query}. Community benchmarks show significant accuracy improvements when multi-source web scrapers feed structured summaries into GPT-4o.",
            "top_comments": [
                "Scraping dynamic content remains the main bottleneck unless you use a headful browser proxy like BrightData.",
                "Parallel nodes in LangGraph work much better than linear sequential chains for this exact setup."
            ],
            "url": "https://reddit.com/r/MachineLearning/comments/ml_discussion_02",
            "source": "Mock Reddit Endpoint"
        }
    ]
