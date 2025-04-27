# etl_designer_app.py
"""
Low-Code ETL Designer  🛠️📊
────────────────────────────────────────────────────────────────────────────
Proof-of-concept Streamlit app that lets you:

1. **Upload** one CSV (for demo simplicity).  
2. **Drag-and-drop** ETL steps (drop columns, filter rows, aggregate).  
3. **Generate & download** a runnable Python script that recreates the pipeline.

This POC skips schemas, data-type checks, and orchestrators.  
For enterprise-grade ELT / DataOps, contact me → drtomharty.com/bio
"""
# ───────────────────────────────────── imports ────────────────────────────
import io, textwrap, json
import pandas as pd
import streamlit as st

# drag-and-drop component
try:
    from streamlit_sortables import st_sortable
    HAS_SORTABLE = True
except ImportError:
    HAS_SORTABLE = False  # fallback to static list

# ───────────────────────── session helpers ───────────────────────────────
def init_session():
    st.session_state.setdefault("steps", [])    # list of dicts
    st.session_state.setdefault("df", None)
    st.session_state.setdefault("csv_name", "input.csv")

# ───────────────────────── step renderer ────────────────────────────────
def render_step(step):
    op = step["op"]
    if op == "drop":
        return f"Drop columns: {', '.join(step['cols'])}"
    if op == "filter":
        return f"Filter: {step['col']} {step['operator']} {step['value']}"
    if op == "agg":
        return f"Aggregate by {', '.join(step['group_cols'])} ({step['agg_func']})"
    return "Unknown step"

# ───────────────────────── code generator ───────────────────────────────
PY_HEADER = '''\
import pandas as pd

df = pd.read_csv("{csv_name}")
'''

def step_to_code(step):
    if step["op"] == "drop":
        return f'df = df.drop(columns={step["cols"]})'
    if step["op"] == "filter":
        op_map = {"==":"==", "contains":".str.contains", ">":">", "<":"<"}
        if step["operator"] == "contains":
            return f'df = df[df["{step["col"]}"].str.contains("{step["value"]}", na=False)]'
        return f'df = df[df["{step["col"]}"] {step["operator"]} {step["value"]}]'
    if step["op"] == "agg":
        groups = step["group_cols"]
        func   = step["agg_func"]
        return (
            f'df = (df.groupby({groups})'
            f'.agg({{"{step["value_col"]}":"{func}"}})'
            f'.reset_index())'
        )
    return "# unknown op"

def build_script():
    lines = [PY_HEADER.format(csv_name=st.session_state.csv_name)]
    for step in st.session_state.steps:
        lines.append(step_to_code(step))
    lines.append('df.to_csv("output.csv", index=False)')
    return "\n\n".join(lines)

# ──────────────────────────── UI ─────────────────────────────────────────
st.set_page_config(page_title="Low-Code ETL Designer", layout="wide")
init_session()

st.title("🛠️ Low-Code ETL Designer")

st.info(
    "🔔 **Demo Notice**\n"
    "Drag-and-drop a few steps, generate a script. No scheduling, versioning, "
    "or schema validation included. For production ELT pipelines, "
    "[contact me](https://drtomharty.com/bio).",
    icon="💡",
)

# Upload CSV
csv_file = st.file_uploader("📂 Upload a CSV (≤15 MB)", type="csv")
if csv_file:
    st.session_state.df = pd.read_csv(csv_file)
    st.session_state.csv_name = csv_file.name
    st.subheader("Data Preview")
    st.dataframe(st.session_state.df.head())
else:
    st.stop()

st.sidebar.header("➕ Add ETL Step")
op_choice = st.sidebar.selectbox("Operation", ["Drop columns","Filter rows","Aggregate"])
if op_choice == "Drop columns":
    cols = st.sidebar.multiselect("Columns to drop", st.session_state.df.columns)
    if st.sidebar.button("Add step") and cols:
        st.session_state.steps.append({"op":"drop","cols":cols})
elif op_choice == "Filter rows":
    col = st.sidebar.selectbox("Column", st.session_state.df.columns)
    operator = st.sidebar.selectbox("Operator", ["==","contains",">","<"])
    value = st.sidebar.text_input("Value (quote strings)")
    if st.sidebar.button("Add step") and value != "":
        st.session_state.steps.append({"op":"filter","col":col,"operator":operator,"value":value})
else:  # Aggregate
    group_cols = st.sidebar.multiselect("Group-by columns", st.session_state.df.columns)
    value_col  = st.sidebar.selectbox("Value column", st.session_state.df.select_dtypes(include="number").columns)
    agg_func   = st.sidebar.selectbox("Agg. function", ["sum","mean","median","max","min"])
    if st.sidebar.button("Add step") and group_cols:
        st.session_state.steps.append(
            {"op":"agg","group_cols":group_cols,"value_col":value_col,"agg_func":agg_func}
        )

# ─────────────── render & reorder steps ───────────────────────────
st.subheader("🗂️ Pipeline")
if not st.session_state.steps:
    st.caption("No steps yet. Add one from the sidebar.")
else:
    step_labels = [render_step(s) for s in st.session_state.steps]
    if HAS_SORTABLE:
        new_order = st_sortable(step_labels, key="sortable")
        # re-order session steps to match drag-order
        st.session_state.steps = [st.session_state.steps[step_labels.index(lbl)] for lbl in new_order]
    else:
        st.write("`streamlit-sortable` not installed → steps shown in fixed order.")
        for lbl in step_labels:
            st.markdown(f"* {lbl}")

# ─────────────── build & download script ──────────────────────────
if st.session_state.steps:
    st.subheader("Generated Python script")
    code = build_script()
    st.code(code, language="python")
    st.download_button("💾 Download script", code.encode(), "etl_pipeline.py", "text/x-python")
