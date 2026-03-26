# Graph-Based Query System with Natural Language Interface

## 🚀 Overview
This project builds a **graph-based data exploration system** on top of SAP Order-to-Cash (O2C) data.

It enables users to:
- Visualize relationships between business entities
- Query the system using natural language
- Get structured, data-backed responses

---

## 🧠 Architecture

### 🔹 Backend
- FastAPI (API layer)
- SQLite (data storage)
- Rule-based SQL generation (LLM fallback-ready)

### 🔹 Frontend
- HTML + D3.js graph visualization
- Interactive query interface
- Results + SQL display

---

## 🧱 Data Model

Entities:
- Orders
- Deliveries
- Invoices
- Payments
- Customers
- Products

Relationships:
Customer → Order → Delivery → Invoice → Payment  
Order → Product  

---

## ⚙️ How It Works

1. User enters natural language query
2. Query is converted into SQL (rule-based)
3. SQL is executed on SQLite DB
4. Results returned + nodes highlighted in graph

---

## 🛡️ Guardrails

- Only domain queries allowed
- SQL safety checks (no DELETE, DROP, etc.)
- Fallback SQL ensures system stability

---

## 🎯 Example Queries

- Find deliveries without invoices
- Find invoices without payments
- Which products are most ordered?

---

## 💡 Design Decisions

- Used SQLite for simplicity and portability
- Used rule-based SQL due to free-tier constraints
- Designed modular LLM integration (plug-and-play)
- Added fallback logic to prevent system failure

---

## 🧪 Running Locally

```bash
pip install -r requirements.txt
python backend/load_data.py
uvicorn backend.main:app --port 8001