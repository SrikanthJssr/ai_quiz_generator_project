import streamlit as st
import requests

# -------------------- CONFIG --------------------
API_BASE_URL = "https://ai-quiz-generator-project-2.onrender.com"  # Updated backend URL

st.set_page_config(page_title="AI Wiki Quiz Generator", layout="wide")
st.title("🧠 AI Wiki Quiz Generator")

# Tabs
tab1, tab2 = st.tabs(["Generate Quiz", "History"])

# -------------------- TAB 1: Generate Quiz --------------------
with tab1:
    url = st.text_input(
        "Enter Wikipedia Article URL:", 
        placeholder="https://en.wikipedia.org/wiki/Machine_learning"
    )

    if st.button("Generate Quiz"):
        if not url.strip():
            st.warning("Please enter a valid Wikipedia URL.")
        else:
            with st.spinner("Generating quiz... ⏳"):
                try:
                    response = requests.post(f"{API_BASE_URL}/generate_quiz", json={"url": url})
                    response.raise_for_status()
                    quiz_data = response.json()
                except Exception as e:
                    st.error(f"❌ Something went wrong: {e}")
                    st.stop()

            st.success("✅ Quiz Generated Successfully!")

            # -------------------- Article Info --------------------
            st.header(f"🔎 {quiz_data.get('title', 'No Title')}")
            st.subheader("📄 Summary / Intro")
            st.write(quiz_data.get("summary", "No summary available."))

            # Key Entities
            st.subheader("🧠 Key Entities")
            ke = quiz_data.get("key_entities", {})
            col1, col2, col3 = st.columns(3)
            col1.write("👨 People:")
            col1.write(ke.get("people", []))
            col2.write("🏛 Organizations:")
            col2.write(ke.get("organizations", []))
            col3.write("📍 Locations:")
            col3.write(ke.get("locations", []))

            # Sections
            with st.expander("📂 Article Sections"):
                for sec in quiz_data.get("sections", []):
                    st.write(f"- {sec}")

            # -------------------- Quiz Questions --------------------
            st.write("---")
            st.header("🧩 Quiz Questions")
            for i, q in enumerate(quiz_data.get("quiz", [])):
                st.subheader(f"Q{i+1}: {q['question']}")
                
                # Show options as radio buttons
                for opt in q['options']:
                    st.radio("", [opt], key=f"{i}_{opt}")

                # Show answer button using expander
                with st.expander("Show Answer"):
                    st.markdown(f"**✅ Correct Answer:** {q['answer']}")
                    st.markdown(f"💡 Explanation: {q.get('explanation', 'No explanation provided.')}")
                    difficulty = q.get("difficulty", "").capitalize()
                    st.markdown(f"📊 Difficulty: {difficulty}")

                st.write("---")

# -------------------- TAB 2: History --------------------
with tab2:
    st.write("### Previously Generated Quizzes")
    try:
        response = requests.get(f"{API_BASE_URL}/history")
        response.raise_for_status()
        history = response.json()
    except Exception as e:
        st.error(f"❌ Failed to fetch history: {e}")
        history = []

    if not history:
        st.info("No quiz history found.")
    else:
        for item in history:
            st.write(f"**ID:** {item['id']}  |  **Title:** {item['title']}  |  **URL:** {item['url']}")
            with st.expander(f"View Quiz Details (ID: {item['id']})"):
                try:
                    detail_response = requests.get(f"{API_BASE_URL}/quiz/{item['id']}")
                    detail_response.raise_for_status()
                    quiz_detail = detail_response.json()

                    for idx, q in enumerate(quiz_detail.get("quiz", []), start=1):
                        st.markdown(f"**Q{idx}: {q.get('question','')}**")
                        options = q.get("options", [])
                        for i, opt in enumerate(options, start=1):
                            st.markdown(f"- {i}. {opt}")
                        st.markdown(f"**Answer:** {q.get('answer','')}") 
                        st.markdown(f"**Explanation:** {q.get('explanation','')}")
                        st.markdown(f"**Difficulty:** {q.get('difficulty','')}")
                        st.write("---")

                except Exception as e:
                    st.error(f"❌ Could not fetch quiz details: {e}")
