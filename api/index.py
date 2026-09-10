import traceback
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from agent.graph import agent_app

app = FastAPI(
    title="Multi-Source AI Research Agent API",
    description="Vercel Serverless API endpoint for LangGraph research workflow",
    version="1.0"
)

class ResearchRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Multi-Source AI Research Agent API is running on Vercel!"}

@app.get("/api/research")
def run_research_get(query: str = Query("DeepSeek-R1 vs GPT-4o architecture comparison")):
    return execute_research(query)

@app.post("/api/research")
def run_research_post(request: ResearchRequest):
    return execute_research(request.query)

def execute_research(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")
        
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
    
    try:
        final_state = agent_app.invoke(initial_state)
        report = final_state.get("final_report")
        if not report:
            raise HTTPException(status_code=500, detail="Failed to synthesize research report.")
        return report
    except Exception as e:
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)} | Stacktrace: {error_details[:500]}")
