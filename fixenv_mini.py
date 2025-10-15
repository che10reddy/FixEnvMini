import streamlit as st
from openai import OpenAI
import difflib

st.title("FixEnv Mini — Zarvah P1 Prototype")
st.caption("AI-powered environment conflict detector")

uploaded_file = st.file_uploader("Upload requirements.txt", type="txt")

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    st.text_area("File content", content, height=200)

    # Basic conflict detection
    lines = [l.strip() for l in content.splitlines() if "==" in l]
    pkgs = {}
    conflicts = []
    for line in lines:
        try:
            name, ver = line.split("==")
            if name in pkgs and pkgs[name] != ver:
                conflicts.append(f"{name}: {pkgs[name]} vs {ver}")
            pkgs[name] = ver
        except:
            pass

    if conflicts:
        st.error("Conflicts found:\n" + "\n".join(conflicts))

        # Explain with AI
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        if st.button("Explain with AI"):
            prompt = "Explain these Python dependency conflicts and suggest fixes:\n" + "\n".join(conflicts)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(response.choices[0].message.content)

            # Diff preview
            new_lines = [l.replace("==", "==latest") for l in lines]
            diff = difflib.unified_diff(lines, new_lines, fromfile="original", tofile="suggested", lineterm="")
            st.code("\n".join(diff))
    else:
        st.success("No version conflicts detected!")