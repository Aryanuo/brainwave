# 🛡️ AI Cyber Threat Detection System

This project simulates network traffic, detects cyber attacks using ML, and triggers automated incident responses via OnDemand agents. The final results are visualized on a clean Streamlit dashboard for demo & presentation purposes.

## 🎯 Key Features
- 🔍 Real‑time traffic simulation
- 🤖 ML‑based threat classification
- 📊 Interactive Streamlit dashboard
- 🧩 Multi‑step OnDemand agent pipeline
- 🚨 Automated alert & escalation
- 📝 Explainable results for SOC visibility

## 🧱 System Architecture
Simulation → Backend API → ML Model → OnDemand Agents → Streamlit Dashboard

### OnDemand Agent Pipeline:
1. Traffic Monitoring  
2. Data Validation  
3. Feature Engineering  
4. Threat Detection (ML)  
5. Severity Classification  
6. Alert & Automation  

## 🧠 Machine Learning
The backend uses an ML model to classify:
- normal vs attack
- risk score (0‑100)
- severity (Low | Medium | High)

**Model Example Input:**
{ "failedlogins": 4, "requestrate": 30, "data_size": 900 }

**Example Output:**
{ "status": "attack", "risk_score": 92, "severity": "High" }

## ⚙️ Tech Stack
**Frontend/Dashboard**
- Python, Streamlit, Plotly/Matplotlib

**Backend**
- Flask, Scikit‑Learn

**Automation (OnDemand Track)**
- Custom AI Agents
