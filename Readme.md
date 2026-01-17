# 🛡️ AI Cyber Threat Detection System

This project simulates network traffic, detects cyber attacks using Machine Learning, and triggers automated incident responses via On‑Demand agents. The final results are visualized on a clean Streamlit dashboard for demonstration purposes.

---

## 📂 Dataset Requirement (Important)

This project does **not include the dataset** due to size limits.  
To run locally, you must download the dataset manually:

📎 **Dataset Link:**  
https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset

### After downloading:
1. Download the ZIP from Kaggle
2. Create a folder named `dataset` in the project root
3. Place the downloaded ZIP file inside `dataset/`

Expected structure:

project-root/
├── backend/
├── frontend/
├── dataset/
│ └── network-intrusion-dataset.zip
└── README.md


---

## 🎯 Key Features

- 🔍 Real‑time traffic & attack simulation
- 🤖 ML‑based threat classification
- 📊 Streamlit dashboard for SOC visibility
- 🧩 Multi‑step OnDemand agent automation
- 🚨 Automatic alert & escalation logic
- 📝 Explainable results and severity scoring

---

## 🧱 System Architecture
Simulation → Backend API → ML Model → OnDemand Agents → Dashboard


### OnDemand Agent Pipeline:
1. Traffic Monitoring  
2. Data Validation  
3. Feature Engineering  
4. Threat Detection (ML)  
5. Severity Classification  
6. Alert & Automation

---

## 🧠 Machine Learning

The ML backend classifies traffic and outputs:

- **Status:** normal / attack
- **Risk Score:** 0‑100
- **Severity:** Low | Medium | High

➡ **Example Input:**
```json
{ "failedlogins": 4, "requestrate": 30, "data_size": 900 }

-**Example Output:**
{ "status": "attack", "risk_score": 92, "severity": "High" }

⚙️ Tech Stack
Frontend / Dashboard

Python
Streamlit
Plotly / Matplotlib
Backend
Flask 
Scikit‑Learn
Automation (OnDemand Track)
Custom AI Agents

🖥️ Local Setup & Execution Guide
Make sure you have Python 3.10+ installed

git clone <your-repo-url>
cd <project-folder>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

🚀 Execution Steps (In Order)
Step 1: Merge Dataset
Step 2: Train the Model
Step 3: Start Backend API
Step 4: Run Traffic Simulation
Step 5: Start Streamlit Dashboard
