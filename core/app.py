import streamlit as st
import re
import sys
import os

# Adding parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.api_client import call_local_ai
from agents import (
    bug_agent, 
    style_agent, 
    mentor, 
    context_agent, 
    best_practice,
    refining_agent, 
    scoring_agent
)

# Page Config
st.set_page_config(page_title="AI Code Reviewer", layout="wide", page_icon="🚀")

# SESSION STATE INITIALIZATION : role : keeping data alive between button clicks 
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'combined_reports' not in st.session_state:
    st.session_state.combined_reports = ""
if 'final_score' not in st.session_state:
    st.session_state.final_score = 0
if 'verdict' not in st.session_state:
    st.session_state.verdict = ""

# Title and Description
st.title("🛡️ Multi-Agent Code Reviewer")
st.toast('All 6 Agents Online & Ready!', icon='🤖')

# --- SIDEBAR ---
with st.sidebar:
    st.header("Project Info")
    st.info("Powered by Qwen 2.5 Coder (Local)")
    languages = [
    "python", "javascript", "java", "c", "cpp", "csharp", 
    "ruby", "r", "go", "rust", "php", "swift", 
    "kotlin", "typescript", "html", "css", "sql"]
    selected_lang = st.selectbox("🌐 Select Code Language:", languages, index=0)
    if st.button("Clear Cache & Reset"):
        st.session_state.analysis_results = None
        st.rerun()
st.markdown(f"Enter your **{selected_lang.upper()}** code below for a deep analysis.")

# MAIN UI
user_code = st.text_area("📄 Write your Code here:", height=250, placeholder="def my_func()...")

# STEP 1: ANALYSIS BUTTON
if st.button("🔍 Run Full Analysis"):
    if not user_code.strip():
        st.warning("Please paste some code first!")
    else:
        with st.status("🤖 Agents are working...", expanded=True) as status:
            st.write("Gathering agent instructions")
            agents_to_run = {
                "Context": context_agent.get_context_agent_prompt(selected_lang),
                "Bugs": bug_agent.get_bug_agent_prompt(selected_lang),
                "Style": style_agent.get_style_agent_prompt(selected_lang),
                "Best Practices": best_practice.get_best_practices_prompt(selected_lang),
                "Mentor": mentor.get_mentor_prompt(selected_lang)
            }

            results = {}
            for name, prompt in agents_to_run.items():
                st.write(f"Calling {name} Agent...")
                results[name] = call_local_ai(prompt, user_code)

            st.write("Calculating final score...")
            score_prompt = scoring_agent.get_scoring_agent_prompt(selected_lang)
            combined = "\n".join([f"{k}: {v}" for k, v in results.items()])
            score_raw = call_local_ai(score_prompt, combined)
            
            # Save to Session State
            st.session_state.analysis_results = results
            st.session_state.combined_reports = combined
            
            # Parse Score
            score_match = re.search(r"^Score:\s*(\d+)", score_raw, re.IGNORECASE | re.MULTILINE)
            st.session_state.final_score = int(score_match.group(1)) if score_match else 0
            reason_match = re.search(r"^Reason:\s*(.*)", score_raw, re.IGNORECASE | re.MULTILINE)
            
            # handling Fallback issue 
            if reason_match:
                st.session_state.verdict = reason_match.group(1)
            elif score_raw.strip():
                st.session_state.verdict = score_raw.split('\n')[0][:150]
            else:
                st.session_state.verdict = "No reason provided by the scoring agent."
            
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

# DISPLAY ANALYSIS RESULTS
if st.session_state.analysis_results:
    m1, m2, m3 = st.columns(3)
    m1.metric("Code Quality Score", f"{st.session_state.final_score}/100")
    m2.metric("Language", selected_lang.upper())
    m3.write(f"**Final Verdict:** {st.session_state.verdict}")

    st.divider()

    tabs = st.tabs(list(st.session_state.analysis_results.keys()))
    for i, (name, report) in enumerate(st.session_state.analysis_results.items()):
        with tabs[i]:
            st.markdown(f"### {name} Analysis")
            st.write(report)

    # REFINING SECTION
    st.divider()
    st.subheader("🛠️ Master Architect Optimization")
    st.write("Ready to fix the issues found above?")
    
    if st.button("✨ Generate Improved Code"):
        with st.spinner("Master Architect is rewriting your code..."):
            refine_prompt = refining_agent.get_refining_agent_prompt(selected_lang)
            # sending the Architect the Language ,original code and the results of the other agents
            full_context = f"LANGUAGE: {selected_lang}\nORIGINAL CODE:\n{user_code}\n\nFEEDBACK FROM AGENTS:\n{st.session_state.combined_reports}"
            
            improved_code = call_local_ai(refine_prompt, full_context)
            
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**Original Code in {selected_lang.upper()}**")
                st.code(user_code, language=selected_lang)
            with c2:
                st.success(f"**Improved Code in {selected_lang.upper()}**")
                st.code(improved_code, language=selected_lang)

            #For downloading 
            ext_map = {
                "python": "py", "javascript": "js", "java": "java", 
                "c": "c", "cpp": "cpp", "csharp": "cs", "ruby": "rb", 
                "r": "r", "go": "go", "rust": "rs", "php": "php", 
                "swift": "swift", "kotlin": "kt", "typescript": "ts", 
                "html": "html", "css": "css", "sql": "sql"
            }
            file_extension = ext_map.get(selected_lang, "txt")

            st.download_button(
                label="📥 Download Fixed Code",
                data=improved_code,
                file_name=f"fixed_code.{file_extension}",
                mime="text/plain"
            )