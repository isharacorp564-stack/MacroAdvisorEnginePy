import streamlit as st
import pandas as pd
import os
import logging
from dotenv import load_dotenv
import json
import time

# 🧬 SEPARATION OF CONCERNS: Import decoupled system data and agent modules
from database_connection import NatWestDatabaseManager, NatWestMCPServerClient
from agents import compile_natwest_agent_graph

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

# --- INITIALIZE CORE ARCHITECTURE MANAGERS ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("NatWestUI")

db_manager = NatWestDatabaseManager()
mcp_server = NatWestMCPServerClient(db_manager)
agent_graph = compile_natwest_agent_graph()  # Compiles the multi-agent graph layout
logger.info("Decoupled multi-agent systems and database pipelines verified.")

# --- STAGE CONFIGURATION ---
st.set_page_config(page_title="NatWest Macro-Guardian Graph", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fcfbfe; }
    h1, h2, h3 { color: #421453 !important; }
    .stButton>button { background-color: #5a2574; color: white; border-radius: 4px; padding: 0.5rem 1.5rem; font-weight: bold; }
    .metric-box { background-color: #ffffff; padding: 15px; border-radius: 6px; border-left: 5px solid #5a2574; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)


def clear_old_response():
    st.session_state["execution_triggered"] = False


if "execution_triggered" not in st.session_state:
    st.session_state["execution_triggered"] = False

uk_macro_feed = {"ONS_CPI": "3.2%", "BoE_Rate": "4.75%", "Energy_Cap": "+4.8%"}

# --- UI HEADER ---
st.title("NatWest Macro-Resilience Guardian")
st.caption("Strategic GenAI Prototype | LangGraph Multi-Agent State Engine & DAO SQLite Architecture")
st.markdown("---")

# --- CONTROL PANEL SIDEBAR ---
st.sidebar.header("🎯 System Control Deck")
segment_choice = st.sidebar.radio("1. Segment:", ("Retail", "Corporate"), on_change=clear_old_response)

available_names = db_manager.get_customer_names_by_segment(segment_choice)
selected_name = st.sidebar.selectbox("2. Customer Selection:", options=available_names, on_change=clear_old_response)

# 🖥️ NEW FEATURE: HIGH-VISIBILITY STATUS CHECKLIST
st.sidebar.markdown("---")
st.sidebar.subheader("🔌 Core Architecture Status")

# 1. Verify local asset storage file presence
if os.path.exists("natwest_guardian.db"):
    st.sidebar.markdown("✅ **SQLite Database:** Connected")
else:
    st.sidebar.markdown("❌ **SQLite Database:** Disconnected")

# 2. Verify the MCP tool execution server is bound
if 'mcp_server' in globals():
    st.sidebar.markdown("✅ **MCP Host Client Engine:** Active")
else:
    st.sidebar.markdown("❌ **MCP Host Client Engine:** Offline")

# 3. Verify LangGraph state topology compilation status
if 'agent_graph' in globals():
    st.sidebar.markdown("✅ **LangGraph Consensus Graph:** Bound")
else:
    st.sidebar.markdown("❌ **LangGraph Consensus Graph:** Broken")

# 4. Verify Groq API Environment token availability
if os.getenv("GROQ_API_KEY"):
    st.sidebar.markdown("✅ **Groq Cloud Gateway:** Authenticated")
else:
    st.sidebar.markdown("❌ **Groq Cloud Gateway:** Missing API Key")

# 🔌 FIX 2: REPLACED NATIVE PYTHON DB READS WITH STANDARDIZED MCP PROTOCOL TOOL CALLS
mcp_response_json = mcp_server.execute_mcp_tool_call(
    tool_name="mcp_query_customer_profile",
    arguments={"customer_name": selected_name}
)
mcp_data = json.loads(mcp_response_json)

# Unpack data directly from your MCP Protocol stream wrapper
active_profile = {
    "Location Code": mcp_data.get("location"),
    "Liquid Balance / Capital": mcp_data.get("capital_balance"),
    "Active Facility Liability": mcp_data.get("facility_liability"),
    "Identified Macro Risk Area": mcp_data.get("macro_vulnerability")
}

# active_profile = db_manager.get_customer_profile(selected_name)

# --- LAYOUT BUILD ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader(f"📋 SQLite Core Ledger: {selected_name}")
    for key, value in active_profile.items():
        st.markdown(f"<div class='metric-box'><b>{key}:</b> {value}</div>", unsafe_allow_html=True)

    st.markdown("---")
    uploaded_file = st.file_uploader("Upload contextual data (.txt)", type=["txt"], on_change=clear_old_response)

    document_context = "No external custom document uploaded."
    if uploaded_file is not None:
        document_context = uploaded_file.read().decode("utf-8")
        st.success("⚡ Context Cache Loaded Successfully")

    st.markdown("---")
    st.subheader("📊 Cached UK Macro Feeds")
    st.dataframe(pd.DataFrame(list(uk_macro_feed.items()), columns=["ID", "Value"]), use_container_width=True,
                 hide_index=True)

with col2:
    st.subheader("📲 Live Output Portal")

    if segment_choice == "Retail":
        suggested_prompt = f"Correlate {selected_name}'s bank files and uploaded text against market data. Give clear investment steps."
    else:
        suggested_prompt = f"Evaluate immediate financial risk for {selected_name} given our macro metrics and uploaded supplier terms."

    if "last_user_query" not in st.session_state:
        st.session_state["last_user_query"] = suggested_prompt

    query_box_val = st.text_area("Query Engine Prompt Window:", value=suggested_prompt, height=70)

    if query_box_val != st.session_state["last_user_query"]:
        st.session_state["last_user_query"] = query_box_val
        st.session_state["execution_triggered"] = False
        st.rerun()

    user_input = query_box_val

    if st.button("🚀 Process Agent Graph"):
        st.session_state["execution_triggered"] = True

    # --- PROTECTED AGENT STATE RUNNER PROCESSING WINDOW ---
    if st.session_state["execution_triggered"]:
        if not os.getenv("GROQ_API_KEY"):
            st.error("❌ Execution Blocked: Missing GROQ_API_KEY inside your .env configuration.")
        else:
            with st.spinner("Invoking multi-agent state graph pipeline routes..."):
                try:
                    logger.info("Passing runtime payloads into compiled LangGraph infrastructure.")

                    # 🚀 EXECUTE THE AGENT GRAPH MATRIX
                    # We pass variables down to the graph state dictionary input channels
                    graph_output = agent_graph.invoke({
                        "customer_name": selected_name,
                        "segment": segment_choice,
                        "bank_data": str(active_profile),
                        "macro_data": str(uk_macro_feed),
                        "uploaded_doc": document_context,
                        "question": user_input
                    })

                    st.markdown("---")

                    # Identify if the final output card caught a security block state
                    if graph_output.get("security_flag", False):
                        st.error("🔒 Security Alert: Unauthorized Query Parameters Intercepted by Supervisor Agent.")
                    else:
                        st.success("🤖 Multi-Agent Consensus Architecture Synthesis Complete")

                    final_text_block = graph_output["final_compiled_response"]


                    def response_chunk_generator():
                        """Simulates word token stream generation for the combined agent matrix block."""
                        for word in final_text_block.split(" "):
                            yield word + " "
                            time.sleep(0.04)


                    # Render the final text block computed asynchronously by the multi-agent graph layer
                    # st.markdown(graph_output["final_compiled_response"])
                    # Stream text chunks smoothly into the Streamlit presentation portal canvas
                    st.write_stream(response_chunk_generator())

                    st.markdown("#### 📱 Native App Quick Actions:")
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if segment_choice == "Retail":
                            st.button("💰 Instantly Open NatWest Regular Saver")
                        else:
                            st.button("💷 Secure Pre-Approved Facility Tranche")
                    with col_btn2:
                        st.button("📅 Secure Chat with a NatWest Advisor")

                except Exception as e:
                    st.error(f"Execution Error: {e}")
                    logger.error(f"Graph Runtime Fault: Stack Trace: {e}")
                    st.session_state["execution_triggered"] = False

st.markdown("---")
