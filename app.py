import json
import streamlit as st
from agent.graph import agent_app
from config import settings

st.set_page_config(
    page_title="Multi-Source AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Advanced AI Web Agent for Multi-Source Research")
st.caption("Powered by LangGraph parallel workflows • GPT-4o Pydantic synthesis • Google & Reddit APIs • BrightData Web Unlocker & Snapshot Manager")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Agent Settings")
    max_search = st.slider("Google Search Depth", 1, 10, settings.max_search_results)
    max_reddit = st.slider("Reddit Discussion Limit", 1, 10, settings.max_reddit_posts)
    use_fallbacks = st.checkbox("Enable Mock Fallback Engines", value=settings.use_mock_fallbacks)
    
    st.markdown("---")
    st.markdown("### 🛠️ Architecture Pipeline")
    st.code("""
[User Query]
     │
     ▼
[Planner Node]
 ├──► Google Node
 ├──► Reddit Node
 └──► BrightData Node
     │
     ▼
[Aggregator Node]
     │
     ▼
[Synthesis Node (GPT-4o)]
     │
     ▼
[Pydantic Report]
    """, language="text")

# Main Query Input Form
with st.form("research_form"):
    query = st.text_input(
        "Enter Research Topic or Engineering Question:",
        value="Compare DeepSeek-R1 and GPT-4o for complex multi-step tool use and agentic coding"
    )
    submit_button = st.form_submit_button("🚀 Run Multi-Source Research Agent", type="primary")

if submit_button and query:
    st.info(f"Initiating LangGraph parallel execution workflow for: **'{query}'**")
    
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
    
    with st.spinner("Executing parallel graph nodes (Google, Reddit, BrightData)..."):
        final_state = agent_app.invoke(initial_state)
        
    report = final_state.get("final_report", {})
    
    if report:
        st.success("✅ Research synthesis completed successfully!")
        
        # Tabs layout
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Executive Summary", 
            "🔍 Key Findings", 
            "📊 Multi-Source Sentiment", 
            "📄 Detailed Report", 
            "📚 Source Bibliography"
        ])
        
        with tab1:
            st.subheader("Executive Summary")
            st.write(report.get("executive_summary", ""))
            
            st.subheader("Methodology")
            st.write(report.get("methodology", ""))
            
        with tab2:
            st.subheader("Extracted Key Findings")
            for finding in report.get("key_findings", []):
                with st.expander(f"🔹 {finding.get('title')} ({finding.get('confidence')} Confidence)"):
                    st.write(finding.get("description"))
                    st.markdown(f"**Supporting Evidence:** _{finding.get('supporting_evidence')}_")
                    st.caption(f"Citations: {', '.join(finding.get('citation_ids', []))}")
                    
        with tab3:
            sentiment = report.get("sentiment_analysis", {})
            st.subheader("Sentiment & Consensus Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Overall Sentiment", sentiment.get("overall_sentiment"))
                st.markdown("**Community Consensus (Reddit):**")
                st.write(sentiment.get("community_consensus"))
            with col2:
                st.markdown("**Expert Perspective (Google/Docs):**")
                st.write(sentiment.get("expert_perspective"))
                
            if sentiment.get("controversies_or_risks"):
                st.markdown("**Identified Risks / Controversies:**")
                for risk in sentiment.get("controversies_or_risks", []):
                    st.warning(f"⚠️ {risk}")
                    
        with tab4:
            st.markdown(report.get("detailed_analysis", ""))
            
        with tab5:
            st.subheader("Verified Source Bibliography")
            for cite in report.get("citations", []):
                st.markdown(f"- **[{cite.get('source_id')}] [{cite.get('title')}]({cite.get('url')})** ({cite.get('platform')}) - Relevance: `{cite.get('relevance_score')}`")
                
        # Export Options
        st.markdown("---")
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                "📥 Export Report as JSON",
                data=json.dumps(report, indent=2),
                file_name="research_report.json",
                mime="application/json"
            )
        with col_exp2:
            st.download_button(
                "📥 Export Report as Markdown",
                data=report.get("detailed_analysis", ""),
                file_name="research_report.md",
                mime="text/markdown"
            )
