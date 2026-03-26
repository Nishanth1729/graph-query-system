from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.db import run_query
from backend.guardrails import is_domain_query, is_safe_sql
from backend.graph import build_graph, extract_ids
from backend.llm import generate_sql

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "Graph Query System Running"}


@app.get("/graph")
def graph():
    return build_graph()


# 🔥 CLEAN FUNCTION (INSIDE FILE, BEFORE USE)
def clean_value(v):
    try:
        if isinstance(v, str) and v.startswith("{"):
            import json
            obj = json.loads(v)

            if all(k in obj for k in ["hours", "minutes", "seconds"]):
                return f"{obj['hours']:02}:{obj['minutes']:02}:{obj['seconds']:02}"

            return str(obj)

        if isinstance(v, str) and "T" in v:
            return v.split("T")[0]

        return v

    except:
        return v


@app.post("/query")
def query(q: Query):
    user_query = q.query

    print("\n👉 USER QUERY:", user_query)

    # Guardrail
    if not is_domain_query(user_query):
        return {"response": "Only dataset-related queries allowed"}

    # 🔥 Generate SQL (rule-based)
    sql = generate_sql(user_query)

    if not sql:
        print("⚠️ Using fallback SQL")
        sql = "SELECT * FROM deliveries LIMIT 10;"

    if not is_safe_sql(sql):
        return {"response": "Unsafe SQL detected"}

    # Run query
    cols, res = run_query(sql)

    if cols is None:
        return {"response": res}

    # 🔥 CLEAN DATA HERE (IMPORTANT)
    cleaned_rows = [
        [clean_value(v) for v in row]
        for row in res
    ]

    highlights = extract_ids(res)

    return {
        "query": user_query,
        "sql": sql,
        "columns": cols,
        "result": cleaned_rows,
        "highlight_nodes": highlights
    }