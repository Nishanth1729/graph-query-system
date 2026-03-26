import json
import sqlite3
import glob
import os

DB = "supply_chain.db"
DATA_DIR = r"C:\Users\pnred\Dodge AI\graph-query-system\data\sap-o2c-data"

TABLE_MAP = {
    "sales_order_headers":          "sales_order_headers",
    "sales_order_items":            "sales_order_items",
    "outbound_delivery_headers":    "outbound_delivery_headers",
    "outbound_delivery_items":      "outbound_delivery_items",
    "billing_document_headers":     "billing_document_headers",
    "billing_document_items":       "billing_document_items",
    "payments_accounts_receivable": "payments_accounts_receivable",
}

conn = sqlite3.connect(DB)

for folder, table in TABLE_MAP.items():
    folder_path = os.path.join(DATA_DIR, folder)
    files = glob.glob(f"{folder_path}/*.jsonl")

    if not files:
        print(f"⚠️  No files found for {table} at {folder_path}")
        continue

    rows = []
    for f in files:
        with open(f) as fp:
            for line in fp:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))

    if not rows:
        print(f"⚠️  No data for {table}")
        continue

    # Flatten nested dicts (e.g. creationTime)
    flat_rows = []
    for r in rows:
        flat = {k: str(v) if isinstance(v, dict) else v for k, v in r.items()}
        flat_rows.append(flat)

    keys = list(flat_rows[0].keys())
    cols = ", ".join(keys)
    placeholders = ", ".join(["?" for _ in keys])

    conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.execute(f"CREATE TABLE {table} ({', '.join(keys)})")
    conn.executemany(
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
        [tuple(r.get(k) for k in keys) for r in flat_rows]
    )
    conn.commit()
    print(f"✅ Loaded {len(flat_rows)} rows → {table}")

conn.close()
print("\n✅ Done. Database ready.")