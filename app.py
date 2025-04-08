import os
import streamlit as st
from models.recommender import AssessmentRecommender

# ✅ Correct way to load the API key from environment
GOOGLE_API_KEY = os.getenv("AIzaSyBIXhp0hS8EqqFTD301_17VADbMcFHB7DA")

if not GOOGLE_API_KEY:
    st.error("Missing Google API Key. Please add it in Streamlit Cloud Secrets.")
    st.stop()

# Initialize recommender
recommender = AssessmentRecommender(api_key=GOOGLE_API_KEY)

# UI
st.title("SHL Assessment Recommendation")
query = st.text_area("Enter a job description or query:")

if st.button("Get Recommendations"):
    if query.strip():
        results = recommender.get_recommendations(query)
        if results:
            st.subheader("Top Recommendations:")
            for item in results:
                st.markdown(f"- **{item}**")
        else:
            st.warning("No recommendations found.")
    else:
        st.warning("Please enter a valid query.")
