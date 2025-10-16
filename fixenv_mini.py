import streamlit as st
from openai import OpenAI
import difflib

st.set_page_config(page_title="FixEnv Mini — Zarvah P1", page_icon="🧠", layout="centered")
st.title("🧩 FixEnv Mini")
st.caption("AI-powered environment conflict detector")

st.markdown("---")

st.subheader("Step 1️⃣  Enter your Python dependencies")
content = st.text_area(
    "Paste or type your package list (e.g., numpy==1.25, pandas==2.0.3):",
    "numpy==1.20\nnumpy==1.25\npandas==1.3\nmatplotlib==3.7.1",
    height=180,
    placeholder="Enter one package per line, like numpy==1.25"
)

conflicts = []
ai_explanation = ""

st.markdown("---")
st.subheader("Step 2️⃣  Detect conflicts")

if st.button("🔍 Detect Conflicts"):
    lines = [l.strip() for l in content.splitlines() if "==" in l]
    pkgs = {}

    for line in lines:
        try:
            name, ver = line.split("==")
            if name in pkgs and pkgs[name] != ver:
                conflicts.append(f"{name}: {pkgs[name]} vs {ver}")
            pkgs[name] = ver
        except:
            pass

    if conflicts:
        st.error("⚠️ Conflicts detected:")
        for c in conflicts:
            st.markdown(f"- `{c}`")
        st.session_state["conflicts"] = conflicts
    else:
        st.success("✅ No version conflicts detected!")
        st.session_state["conflicts"] = []

if "conflicts" in st.session_state and st.session_state["conflicts"]:
    st.markdown("---")
    st.subheader("Step 3️⃣  AI Explanation")

    if st.button("💡 Explain with AI"):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = (
            "Explain these Python dependency conflicts and how to fix them clearly:\n"
            + "\n".join(st.session_state["conflicts"])
        )
        with st.spinner("Contacting AI assistant..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
        ai_explanation = response.choices[0].message.content
        st.success("🧠 AI Explanation:")
        st.write(ai_explanation)
        st.session_state["ai_explanation"] = ai_explanation

if "conflicts" in st.session_state and st.session_state["conflicts"]:
    st.markdown("---")
    st.subheader("Step 4️⃣  Suggested Fix Preview")

    lines = [l.strip() for l in content.splitlines() if "==" in l]
    new_lines = [l.replace("==", "==latest") for l in lines]
    diff = difflib.unified_diff(
        lines, new_lines, fromfile="original", tofile="suggested", lineterm=""
    )
    st.code("\n".join(diff))

if "ai_explanation" in st.session_state and st.session_state["ai_explanation"]:
    import io, zipfile
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("requirements.txt", content)
        z.writestr("ai_explanation.txt", st.session_state["ai_explanation"])
    st.download_button(
        label="📦 Download Snapshot (ZIP)",
        data=buffer.getvalue(),
        file_name="FixEnvMini_Snapshot.zip",
        mime="application/zip",
    )

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; opacity: 0.7;'>
    🚀 <b>FixEnv Mini</b> is a prototype of <b>Zarvah</b> — a self-healing developer platform built to automate and simplify coding environments.
    </div>
    """,
    unsafe_allow_html=True,
)
