import streamlit as st
import requests
import json

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI GitHub Issue Assistant",
    layout="centered"
)

st.title("🤖 AI-Powered GitHub Issue Assistant")
st.caption("Analyze and prioritize GitHub issues using AI")

API_URL = "http://127.0.0.1:8000/analyze"

# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------
with st.form("issue_form", clear_on_submit=False):
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/facebook/react",
        help="Public GitHub repository URL"
    )

    issue_number = st.number_input(
        "Issue Number",
        min_value=1,
        step=1,
        help="Numeric GitHub Issue ID"
    )

    submit = st.form_submit_button("🔍 Analyze Issue")

# --------------------------------------------------
# API CALL
# --------------------------------------------------
if submit:
    if not repo_url.strip():
        st.error("Repository URL is required.")
        st.stop()

    with st.spinner("Fetching issue and analyzing with AI..."):
        try:
            response = requests.post(
                API_URL,
                json={
                    "repo_url": repo_url.strip(),
                    "issue_number": int(issue_number)
                },
                timeout=60
            )

            if response.status_code != 200:
                # Extract meaningful backend error
                try:
                    error_msg = response.json().get("detail", response.text)
                except Exception:
                    error_msg = response.text

                st.error(f"Backend error: {error_msg}")
                st.stop()

            result = response.json()

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to backend API: {e}")
            st.stop()

    # --------------------------------------------------
    # OUTPUT DISPLAY
    # --------------------------------------------------
    st.success("Analysis complete")

    st.subheader("📄 Summary")
    st.write(result.get("summary", "—"))

    st.subheader("🏷️ Type")
    st.write(result.get("type", "—"))

    st.subheader("🔥 Priority")
    st.write(result.get("priority_score", "—"))

    st.subheader("🧩 Suggested Labels")
    labels = result.get("suggested_labels", [])
    st.write(", ".join(labels) if labels else "—")

    st.subheader("⚠️ Potential Impact")
    st.write(result.get("potential_impact", "—"))

    st.divider()

    # --------------------------------------------------
    # RAW JSON + EXTRA MILE
    # --------------------------------------------------
    st.subheader("📦 Raw JSON Output")
    st.json(result)

    st.download_button(
        label="📋 Download JSON",
        data=json.dumps(result, indent=2),
        file_name="issue_analysis.json",
        mime="application/json"
    )
