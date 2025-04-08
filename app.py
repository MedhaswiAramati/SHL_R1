import streamlit as st
from models.recommender import AssessmentRecommender

# ✅ Load Google API key from .streamlit/secrets.toml
GOOGLE_API_KEY = st.secrets["google"].get("api_key")

if not GOOGLE_API_KEY:
    st.error("Missing Google API Key. Please add it in Streamlit secrets.")
    st.stop()

# Initialize your recommender
recommender = AssessmentRecommender(api_key=GOOGLE_API_KEY)

# Streamlit UI
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommendation Tool")

query = st.text_area("Enter a job description or role description:", height=200)

if st.button("Get Recommendations"):
    if query.strip():
        with st.spinner("Analyzing and recommending..."):
            try:
                results = recommender.get_recommendations(query)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.stop()

        if results:
            st.subheader("Top Recommended Assessments:")
            for item in results:
                # Use .get() to safely handle missing keys
                name = item.get("name", "Unnamed Assessment")
                url = item.get("url", "#")
                type_ = item.get("type", "Exam")
                duration = item.get("duration", "one hour")
                remote = item.get("remote", "yes/no")
                adaptive = item.get("adaptive", "yes/no")

                st.markdown(
                    f"- **{name}** ([Link]({url}))  \n"
                    f"🧪 Type: {type_} | ⏱️ Duration: {duration}  \n"
                    f"🌐 Remote: {remote} | 📊 Adaptive/IRT: {adaptive}"
                )
        else:
            st.warning("No relevant assessments found.")
    else:
        st.warning("Please enter a valid query.")
