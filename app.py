import streamlit as st
from run_pipeline import run_full_pipeline
from briefing_agent import generate_briefing

st.set_page_config(page_title="AI Day-Briefing", page_icon="📋", layout="centered")

st.title("📋 AI Day-Briefing Agent")
st.caption("An AI agent that reads your Gmail + Calendar and generates a personalized daily briefing")

st.divider()

if st.button("🔄 Generate Today's Briefing", type="primary"):
    with st.spinner("Fetching emails and calendar events..."):
        emails, events = run_full_pipeline()

    with st.spinner("Generating your briefing with AI..."):
        briefing = generate_briefing(emails, events)

    st.success("Briefing generated!")
    st.subheader("Your Briefing")
    st.write(briefing)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Emails Analyzed", len(emails))
    with col2:
        high_priority = len([e for e in emails if e['urgency_score'] >= 4])
        st.metric("High Priority", high_priority)

    with st.expander("🔍 See Email Breakdown"):
        for e in emails[:10]:
            st.write(f"**{e['subject']}**")
            st.caption(f"From: {e['sender']} | Urgency: {e['urgency_score']}/10 | Category: {e['category']}")
            st.divider()
else:
    st.info("👆 Click the button above to generate your daily briefing")