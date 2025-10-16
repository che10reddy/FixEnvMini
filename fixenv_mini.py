import streamlit as st
from openai import OpenAI
import difflib

# -----------------------------
# Title & Branding
# -----------------------------
st.set_page_config(page_title="FixEnv Mini — Zarvah P1", page_icon="🧠", layout="centered")
st.title("🧩 FixEnv Mini")
st.caption("AI-powered environment conflict detector")

st.markdown("---")

# -----------------------------
# Step 1: Input
# -----------------------------
st.subheader("Step 1️⃣  Paste your requirements.txt content")
content = st.text_area(
    "Paste below or type a few example dependencies:",
    "numpy==1.20\nnumpy==1.25\npandas==1.3\npandas==1.4",
    height=180,
    placeholder="e.g., numpy==1.25\npandas==2.0.3\nmatplotlib==3.7.1"
)

# keep content available across steps
st.session_state["content"] = content

st.markdown("---")

# -----------------------------
# Step 2: Detect Conflicts  ✅ now visible
# -----------------------------
st.subheader("Step 2️⃣  Detect conflicts")
detect_clicked = st.button("🔍 Detect Conflicts")

if detect_clicked:
    lines = [l.strip() for l in content.splitlines() if "==" in l]
    pkgs = {}
    conflicts = []

    for line in lines:
        try:
            name, ver = line.split("==", maxsplit=1)
            if name in pkgs and pkgs[name] != ver:
                conflicts.append(f"{name}: {pkgs[name]} vs {ver}")
            pkgs[name] = ver
        except Exception:
            # ignore malformed lines for demo
            pass

    st.session_state["lines"] = lines
    st.session_state["conflicts"] = conflicts

# Show detection results (after first click)
if "conflicts" in st.session_state:
    if st.session_state["conflicts"]:
        st.error("⚠️ Conflicts detected:")
        for c in st.session_state["conflicts"]:
            st.markdown(f"- `{c}`")
    else:
        st.success("✅ No version conflicts detected!")

# -----------------------------
# Step 3: AI Explanation
# -----------------------------
if st.session_state.get("conflicts"):
    st.markdown("---")
    st.subheader("Step 3️⃣  AI Explanation & Suggested Fix Preview")

    if st.button("💡 Explain with AI"):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = (
            "Explain these Python dependency conflicts and how to fix them clearly:\n"
            + "\n".join(st.session_state["conflicts"])
        )
        with st.spinner("Contacting AI assistant..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
        ai_explanation = response.choices[0].message.content
        st.session_state["ai_explanation"] = ai_explanation

        # ✅ Show AI explanation first
        st.success("🧠 AI Explanation")
        st.write(ai_explanation)

        # ✅ Then show diff preview *after* explanation
        st.markdown("---")
        st.subheader("Step 4️⃣  Suggested Fix Preview")

        lines = st.session_state.get("lines", [])
        new_lines = [l.replace("==", "==latest") for l in lines]
        diff = difflib.unified_diff(
            lines, new_lines, fromfile="original", tofile="suggested", lineterm=""
        )
        st.code("\n".join(diff) or "# No changes suggested")
# -----------------------------
# Step 4: Suggested Fix Preview
# -----------------------------
if st.session_state.get("conflicts"):
    st.markdown("---")
    st.subheader("Step 4️⃣  Suggested fix preview")
    lines = st.session_state.get("lines", [])
    # simple demo suggestion: mark as "latest"
    new_lines = [l.replace("==", "==latest") for l in lines]
    diff = difflib.unified_diff(
        lines, new_lines, fromfile="original", tofile="suggested", lineterm=""
    )
    st.code("\n".join(diff) or "# No changes suggested")

# -----------------------------
# Step 5: Snapshot Download
# -----------------------------
if st.session_state.get("ai_explanation"):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("requirements.txt", st.session_state.get("content", ""))
        z.writestr("ai_explanation.txt", st.session_state["ai_explanation"])
    st.download_button(
        label="📦 Download snapshot (ZIP)",
        data=buffer.getvalue(),
        file_name="FixEnvMini_Snapshot.zip",
        mime="application/zip",
    )

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; opacity: 0.7;'>
    🚀 <b>FixEnv Mini</b> is a prototype of <b>Zarvah</b> — a self-healing developer platform to automate and simplify coding environments.
    </div>
    """,
    unsafe_allow_html=True,
)
