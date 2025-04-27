# ETL-Designer

🛠️ Low-Code ETL Designer
A Streamlit proof-of-concept that lets you visually build simple ETL pipelines—then export a runnable Python script. No notebooks, no Docker, no orchestration.

🔍 What it does
Upload any CSV.

Define ETL steps via drag-and-drop (or static list):

Drop columns

Filter rows

Aggregate (group + aggregate function)

Reorder steps interactively.

Generate a plain-Pandas Python script (etl_pipeline.py).

Download the script and run it locally to produce output.csv.

Demo only—no type-checks, schema enforcement, or scheduler.
For production ETL / DataOps solutions, contact me.

✨ Key Features
Drag-and-drop UI (via streamlit-sortable)

Three core operations: drop, filter, aggregate

One-file app (etl_designer_app.py)

Script download—the generated code is plain Pandas

Fallback UI when streamlit-sortable isn’t installed

🚀 Quick Start (Local)
bash
Copy
Edit
git clone https://github.com/THartyMBA/low-code-etl-designer.git
cd low-code-etl-designer
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run etl_designer_app.py
Upload your CSV.

Add/arrange ETL steps.

Copy or download the generated etl_pipeline.py.

☁️ Deploy on Streamlit Cloud (Free)
Push this repo (public or private) to GitHub under THartyMBA.

Go to streamlit.io/cloud ➜ New app → select your repo & branch.

Click Deploy—no secrets needed.

🛠️ Requirements
text
Copy
Edit
streamlit>=1.32
pandas
streamlit-sortable   # optional; falls back to static UI if omitted
🗂️ Repo Structure
kotlin
Copy
Edit
low-code-etl-designer/
├─ etl_designer_app.py   ← single-file Streamlit app
├─ requirements.txt
└─ README.md             ← this file
📜 License
CC0 1.0 – public-domain dedication. Attribution appreciated but not required.

🙏 Acknowledgements
Streamlit – rapid Python UIs

Pandas – data manipulation

streamlit-sortable – drag-and-drop ordering

Design your ETL visually, export code, and build data pipelines in seconds!
