import os
import tempfile
import logging
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

# Determine safe snapshot directory based on environment (Vercel serverless vs local)
default_snapshot_dir = "./snapshots"
if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    default_snapshot_dir = os.path.join(tempfile.gettempdir(), "snapshots")

class Settings(BaseSettings):
    # LLM Settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o")
    
    # BrightData Settings
    brightdata_api_key: str = os.getenv("BRIGHTDATA_API_KEY", "")
    brightdata_zone: str = os.getenv("BRIGHTDATA_ZONE", "web_unlocker")
    
    # Search API Settings
    serpapi_api_key: str = os.getenv("SERPAPI_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    
    # Reddit Settings
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_client_secret: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    reddit_user_agent: str = os.getenv("REDDIT_USER_AGENT", "MultiSourceResearchAgent/1.0")
    
    # Storage & Application Defaults
    snapshot_dir: Path = Path(os.getenv("SNAPSHOT_DIR", default_snapshot_dir))
    max_search_results: int = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    max_reddit_posts: int = int(os.getenv("MAX_REDDIT_POSTS", "5"))
    use_mock_fallbacks: bool = os.getenv("USE_MOCK_FALLBACKS", "true").lower() == "true"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

# Safely create snapshot directory if writable
try:
    settings.snapshot_dir.mkdir(parents=True, exist_ok=True)
except Exception as e:
    logger.warning(f"Could not create snapshot directory {settings.snapshot_dir}: {e}")
