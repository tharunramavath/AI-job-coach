import streamlit as st
from ui.styles import apply_base_style, stage_header, response_box
from ai.memory import init_memory, add_message, get_history, clear_memory
from dotenv import load_dotenv

load_dotenv()


DEFAULT_RESUME = """Name: Priya Sharma
Degree: B.Tech Computer Science, 2024, VIT Vellore
Skills: Python, Machine Learning, TensorFlow, SQL, REST APIs
Projects: Sentiment analysis on Twitter data (90% accuracy), E-commerce recommendation system
Internship: 2 months at a Hyderabad startup — built a data pipeline in Python
Looking for: Entry-level ML Engineer or Data Scientist roles in India
Preferences: Avoids micromanagement, prefers remote-friendly companies"""


def render_stage_runner(stage_num: int):
    apply_base_style()

    if stage_num == 1:
        from stages.stage_1_oracle import run_stage_1
        
        stage_header(
            stage_num=1,
            title="The Dumb Oracle",
            duration="10 min",
            concept="Just call an LLM with no context. Watch how useless it is.",
        )
        
        st.markdown("**Ask it anything about your job search:**")
        user_input = st.text_input(
            label="Your question",
            placeholder="What jobs should I apply for?",
            label_visibility="collapsed",
        )
        
        if st.button("Ask", disabled=not user_input):
            with st.spinner("Calling LLM..."):
                response = run_stage_1(user_input)
            response_box(response)
            st.caption("⬆ Generic. Useless. No context about you whatsoever.")

    elif stage_num == 2:
        from stages.stage_2_memory import run_stage_2
        
        stage_header(
            stage_num=2,
            title="Give It a Brain: Memory",
            duration="15 min",
            concept="Paste your resume. The system prompt becomes the agent's short-term memory.",
        )
        
        resume = st.text_area(
            label="Your resume / background",
            value=DEFAULT_RESUME,
            height=200,
            label_visibility="visible",
        )
        
        user_input = st.text_input(
            label="Your question",
            placeholder="What jobs should I apply for?",
            label_visibility="visible",
        )
        
        if st.button("Ask with context", disabled=not user_input or not resume):
            with st.spinner("Calling LLM with context..."):
                res = run_stage_2(user_input, resume)
                
            st.markdown("**Without context (Stage 1 answer):**")
            response_box(res["without_context"])
            
            st.markdown("**With your resume context (Stage 2 answer):**")
            response_box(res["with_context"])
            
            st.caption("⬆ Same LLM. Same question. Completely different answer — because of context.")

    elif stage_num == 3:
        from stages.stage_3_tools import run_stage_3
        
        stage_header(
            stage_num=3,
            title="Give It Eyes: Tools",
            duration="20 min",
            concept="Add a real-time job search tool. It stops being a chatbot and starts being an agent.",
        )
        
        role_query = st.text_input(
            label="What role are you looking for?",
            placeholder="ML Engineer fresher India remote",
            label_visibility="visible",
        )
        
        resume_snippet = st.text_area(
            label="Your background (brief)",
            placeholder="B.Tech CS 2024, Python, ML, TensorFlow, looking for ML Engineer role",
            height=80,
            label_visibility="visible",
        )
        
        if st.button("Search + Advise", disabled=not role_query):
            with st.spinner("Running job search and synthesizing advice..."):
                try:
                    res = run_stage_3(role_query, resume_snippet)
                    
                    st.markdown("**Tool Output — Real job listings found:**")
                    st.code(res["jobs_text"], language="text")
                    
                    st.markdown("**Agent Response:**")
                    response_box(res["response"])
                    
                    st.caption("⬆ Real listings from the web + LLM reasoning = an agent with eyes.")
                except Exception as e:
                    st.error(f"Execution failed: {e}")

    elif stage_num == 4:
        from stages.stage_4_react import run_stage_4
        
        stage_header(
            stage_num=4,
            title="Give It Judgment: ReAct Loop",
            duration="15 min",
            concept="Thought → Action → Observation. Watch the agent decide when to search vs when to reason.",
        )
        
        st.markdown("Try both types of questions:")
        st.markdown("- **Search-Required**: *'Find me ML Engineer jobs in Bangalore'* — will trigger the Jina search tool.")
        st.markdown("- **Reasoning-Only**: *'Can you explain what a Machine Learning Engineer does?'* — will answer directly from LLM reasoning.")

        
        resume_context = st.text_area(
            label="User background (optional)",
            placeholder="B.Tech CS 2024, Python, ML, TensorFlow...",
            height=70,
            label_visibility="visible",
        )
        
        user_input = st.text_input(
            label="Ask the agent",
            placeholder="Find me ML Engineer jobs in Bangalore",
            label_visibility="visible",
        )
        
        if st.button("Run ReAct Loop", disabled=not user_input):
            with st.spinner("Agent is thinking..."):
                steps = run_stage_4(user_input, resume_context)
                
            st.markdown("**Agent Trace:**")
            for step in steps:
                if step["type"] == "thought":
                    st.markdown(
                        f'<div class="thought-box">💭 <strong>Thought:</strong><br>{step["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                elif step["type"] == "action":
                    st.markdown(
                        f'<div class="action-box">⚡ <strong>Action:</strong><br>{step["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                elif step["type"] == "observation":
                    content = step["content"]
                    if len(content) > 600:
                        content = content[:600] + "\n... [truncated]"
                    st.markdown(
                        f'<div class="obs-box">👁 <strong>Observation:</strong><br>{content}</div>',
                        unsafe_allow_html=True,
                    )
                elif step["type"] == "final":
                    st.markdown(
                        f'<div class="final-box">✅ <strong>Final Answer:</strong><br>{step["content"]}</div>',
                        unsafe_allow_html=True,
                    )

    elif stage_num == 5:
        from stages.stage_5_persistent_memory import run_stage_5
        
        stage_header(
            stage_num=5,
            title="Give It Continuity: Persistent Memory",
            duration="10 min",
            concept="It remembers what you said 3 messages ago and factors it in automatically.",
        )
        
        init_memory(st.session_state, key="stage5_history")
        st.caption("Try saying: *'I hate micromanagement'* then later ask *'What companies should I avoid?'*")
        st.caption("The agent will connect the dots.")
        
        history = get_history(st.session_state, key="stage5_history")
        if history:
            st.markdown("**Conversation so far:**")
            for msg in history:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**Agent:** {msg['content']}")
            st.divider()
            
        user_input = st.text_input(
            label="Say something",
            placeholder="I hate micromanagement and open offices...",
            label_visibility="visible",
            key="stage5_input",
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            send = st.button("Send", disabled=not user_input)
        with col2:
            if st.button("Clear memory"):
                clear_memory(st.session_state, key="stage5_history")
                st.rerun()
                
        if send and user_input:
            add_message(st.session_state, "user", user_input, key="stage5_history")
            current_history = get_history(st.session_state, key="stage5_history")
            
            with st.spinner("Thinking..."):
                response = run_stage_5(current_history)
                
            add_message(st.session_state, "assistant", response, key="stage5_history")
            st.rerun()

    elif stage_num == 6:
        from stages.stage_6_full_agent import run_stage_6_stream
        
        stage_header(
            stage_num=6,
            title="The Full Agent",
            duration="15 min",
            concept="Resume context + real job search + conversation memory. All wired together.",
        )
        
        if "stage6_resume" not in st.session_state:
            st.session_state["stage6_resume"] = ""
            
        init_memory(st.session_state, key="stage6_history")
        
        with st.expander("📄 Paste your resume here (do this once)", expanded=not st.session_state["stage6_resume"]):
            resume_input = st.text_area(
                label="Resume / background",
                value=st.session_state["stage6_resume"],
                height=180,
                placeholder="Name: Priya Sharma\nSkills: Python, ML...",
                label_visibility="collapsed",
            )
            if st.button("Set resume"):
                st.session_state["stage6_resume"] = resume_input
                st.success("Resume saved. Start chatting below.")
                st.rerun()
                
        resume = st.session_state.get("stage6_resume", "")
        history = get_history(st.session_state, key="stage6_history")
        
        if history:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-bubble-user">👤 <strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    st.markdown(f'<div class="chat-bubble-agent">🤖 <strong>Agent:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "tool":
                    st.markdown('</div>', unsafe_allow_html=True)
                    with st.expander("🔍 Job search result"):
                        st.code(msg["content"], language="text")
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.divider()
            
        user_input = st.text_input(
            label="Ask your job coach",
            placeholder="Find me ML Engineer jobs in Hyderabad, or ask for career advice...",
            label_visibility="visible",
            key="stage6_input",
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            send = st.button("Send", disabled=not user_input)
        with col2:
            if st.button("Clear chat"):
                clear_memory(st.session_state, key="stage6_history")
                st.rerun()
                
        if send and user_input:
            # Add user message to history
            add_message(st.session_state, "user", user_input, key="stage6_history")
            
            # Show the user message immediately on screen using styled bubble
            st.markdown(
                f'<div class="chat-container"><div class="chat-bubble-user">👤 <strong>You:</strong><br>{user_input}</div></div>', 
                unsafe_allow_html=True
            )
            
            current_history = get_history(st.session_state, key="stage6_history")
            
            with st.spinner("Searching real job listings..."):
                from stages.stage_6_full_agent import run_stage_6_stream
                tool_context, stream = run_stage_6_stream(user_input, resume, current_history)
                
            if tool_context:
                add_message(st.session_state, "tool", tool_context, key="stage6_history")
                with st.expander("🔍 Job search result", expanded=True):
                    st.code(tool_context, language="text")
                    
            # Custom token-by-token streaming loop inside HTML bubble
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            placeholder = st.empty()
            response_text = ""
            for chunk in stream:
                response_text += chunk
                placeholder.markdown(
                    f'<div class="chat-bubble-agent">🤖 <strong>Agent:</strong><br>{response_text}▌</div>',
                    unsafe_allow_html=True
                )
            placeholder.markdown(
                f'<div class="chat-bubble-agent">🤖 <strong>Agent:</strong><br>{response_text}</div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Save the final text to session history and rerun to clean layout
            add_message(st.session_state, "assistant", response_text, key="stage6_history")
            st.rerun()





