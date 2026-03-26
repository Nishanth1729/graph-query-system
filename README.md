# 🚀 Graph-Based Query System with Natural Language Interface

## 📌 Overview

This project builds a **graph-based data exploration system** on top of SAP Order-to-Cash (O2C) data.

It solves the problem of fragmented enterprise data by:

* Structuring entities into a connected graph
* Enabling **natural language querying**
* Returning **data-backed, explainable results**

---

## 🎯 Key Features

* 🌐 Interactive **graph visualization (D3.js)**
* 💬 Natural language → SQL query generation (LLM-powered)
* 🧠 Schema-grounded query generation for accuracy
* 🛡️ Guardrails for safe and domain-restricted queries
* ⚡ Fallback logic for reliability
* 📊 Structured results with SQL transparency

---

## 🧠 Architecture

### 🔹 Backend

* FastAPI (API layer)
* SQLite (data storage)
* Groq LLM API (SQL generation)
* Rule-based fallback (robustness)

### 🔹 Frontend

* HTML + D3.js graph visualization
* Query input interface
* SQL + results display panel

---

## 🧱 Data Model

### Entities

* Orders
* Deliveries
* Invoices
* Payments
* Customers
* Products

### Relationships

Customer → Order → Delivery → Invoice → Payment
Order → Product

---

## ⚙️ How It Works

1. User enters a natural language query
2. Query is processed by **LLM (Groq)**
3. SQL is generated using schema-aware prompting
4. SQL is executed on SQLite database
5. Results are returned and displayed
6. Relevant nodes are highlighted in the graph

---

## 🤖 LLM Integration

* Uses **Groq API (LLaMA 3.1 model)** for SQL generation
* Prompt includes:

  * Full schema
  * Relationships
  * Constraints
* Handles:

  * Missing data queries (LEFT JOIN)
  * Multi-table joins
  * Schema correctness

### 🔁 Fallback Mechanism

If LLM fails:

* System switches to rule-based SQL
* Ensures **zero system failure during demo**

---

## 🛡️ Guardrails

* Restricts queries to domain-specific context
* Blocks unsafe SQL (DROP, DELETE, UPDATE)
* Ensures valid SQL execution only

---

## 🎯 Example Queries

* Find deliveries without invoices
* Find invoices without payments
* Show cancelled billing documents
* Which products are most ordered?

---

## 💡 Design Decisions

* Used SQLite for simplicity and portability
* Used schema-grounded prompting to reduce LLM hallucination
* Designed hybrid system (LLM + fallback)
* Focused on **accuracy over raw generation**

---

## 🧪 Running Locally

```bash
pip install -r requirements.txt
python backend/load_data.py
uvicorn backend.main:app --port 8001
```

Open:
http://127.0.0.1:8001/docs

Frontend:
Open `index.html` using Live Server

---

## 🌐 Live Demo

👉 https://graph-query-system-fcpmcw02k-nishanth1729s-projects.vercel.app/

---

## 🔮 Future Improvements

* Graph database integration (Neo4j)
* Semantic search layer
* Conversation memory
* Advanced graph analytics

---

## 🏁 Conclusion

This system demonstrates:

* Graph-based data modeling
* LLM-powered query translation
* Robust backend engineering
* End-to-end product thinking

---

## 👨‍💻 Author

Built as part of Forward Deployed Engineer assignment.
