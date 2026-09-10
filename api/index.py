from fastapi import FastAPI, HTTPException
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

@app.post("/api/research")
def run_research(request: ResearchRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")
        
    initial_state = {
        "original_query": request.query,
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
        raise HTTPException(status_code=500, detail=str(e))
