import subprocess
import sys
from pathlib import Path

import streamlit as st

from tools import load_history


UPLOAD_FOLDER = Path("uploads")
HISTORY_FILE = "bug_history.json"

st.set_page_config(
    page_title="Python Bug Fixer",
    page_icon="🐞",
    layout="wide"
)

st.title("Python Bug Fixer Agent")
st.write("Upload a tested Python file and let the agent fix it.")

uploaded_file = st.file_uploader(
    "Choose a Python file",
    type=["py"]
)

if uploaded_file is not None:
    code = uploaded_file.getvalue().decode("utf-8")

    st.subheader("Uploaded Code")
    st.code(code, language="python")

    if st.button("Fix Bug", type="primary"):
        if "# === TESTS ===" not in code:
            st.error("The uploaded file must contain # === TESTS ===")
        else:
            UPLOAD_FOLDER.mkdir(exist_ok=True)

            safe_filename = Path(uploaded_file.name).name
            uploaded_path = UPLOAD_FOLDER / safe_filename
            uploaded_path.write_text(code, encoding="utf-8")

            with st.spinner("The agent is inspecting and fixing the bug..."):
                try:
                    result = subprocess.run(
                        [
                            sys.executable,
                            "main.py",
                            str(uploaded_path)
                        ],
                        capture_output=True,
                        text=True,
                        timeout=180
                    )

                    history = load_history(HISTORY_FILE)

                    if not history:
                        st.error("No agent result was saved.")
                    else:
                        record = history[-1]
                        attempts = record.get("attempts", [])

                        if record["success"]:
                            st.success("The bug was fixed successfully!")

                            if attempts:
                                final_attempt = attempts[-1]

                                first_column, second_column = st.columns(2)

                                with first_column:
                                    st.metric(
                                        "Bug Type",
                                        final_attempt.get(
                                            "bug_type",
                                            "Unknown"
                                        )
                                    )

                                with second_column:
                                    st.metric(
                                        "Confidence",
                                        final_attempt.get(
                                            "confidence",
                                            "Unknown"
                                        )
                                    )

                                st.subheader("Explanation")
                                st.write(
                                    final_attempt.get(
                                        "explanation",
                                        "No explanation provided."
                                    )
                                )

                                st.subheader("Original Error")
                                st.code(
                                    final_attempt.get("error", ""),
                                    language="text"
                                )

                                st.subheader("Fixed Code")
                                fixed_code = final_attempt.get("code", "")
                                st.code(fixed_code, language="python")

                                st.download_button(
                                    "Download Fixed Code",
                                    data=fixed_code,
                                    file_name=f"fixed_{safe_filename}",
                                    mime="text/x-python"
                                )

                            with st.expander("Attempt History"):
                                for attempt in attempts:
                                    st.write(
                                        f"Attempt {attempt['attempt']}"
                                    )
                                    st.write(
                                        attempt.get(
                                            "explanation",
                                            "No explanation"
                                        )
                                    )
                                    st.code(
                                        attempt.get("code", ""),
                                        language="python"
                                    )

                        else:
                            st.error("The agent could not fix the bug.")
                            st.write(
                                record.get(
                                    "reason",
                                    "Unknown failure"
                                )
                            )

                    with st.expander("Raw Agent Output"):
                        st.code(result.stdout, language="text")

                        if result.stderr:
                            st.code(result.stderr, language="text")

                except subprocess.TimeoutExpired:
                    st.error("The agent took too long and was stopped.")