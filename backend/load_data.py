import sqlite3
import pandas as pd
import os
import json

BASE_PATH = "data/sap-o2c-data"
conn = sqlite3.connect("data/data.db")


def rename_columns(df):
    column_map = {
        "sales_document": "order_id",
        "sold_to_party": "customer_id",
        "delivery_document": "delivery_id",
        "billing_document": "invoice_id",
        "material": "product_id",
        "reference_document": "reference_document"
    }
    df.rename(columns=column_map, inplace=True)
    return df


def clean_dataframe(df):
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x
        )
    return df


def load_folder(folder_name, table_name):
    folder_path = os.path.join(BASE_PATH, folder_name)

    print(f"\nChecking {folder_name}")

    if not os.path.exists(folder_path):
        print("❌ Missing folder")
        return

    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for file in filenames:
            if file.lower().endswith(".jsonl"):
                files.append(os.path.join(root, file))

    if not files:
        print("❌ No JSONL files found")
        return

    df_list = []

    for path in files:
        print(f"📄 Loading: {path}")

        data = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line))

        df = pd.DataFrame(data)
        df.columns = df.columns.str.lower()

        df = rename_columns(df)
        df_list.append(df)

    final_df = pd.concat(df_list, ignore_index=True)

    # 🔥 CLEAN NESTED DATA
    final_df = clean_dataframe(final_df)

    print(f"✅ Loaded {table_name} ({len(final_df)} rows)")

    final_df.to_sql(table_name, conn, if_exists="replace", index=False)


TABLE_MAP = {
    "sales_order_headers": "orders",
    "sales_order_items": "order_items",
    "outbound_delivery_headers": "deliveries",
    "billing_document_headers": "invoices",
    "payments_accounts_receivable": "payments",
    "products": "products",
    "business_partners": "customers"
}


for folder, table in TABLE_MAP.items():
    load_folder(folder, table)

conn.close()

print("\n🎉 Data Loaded Successfully")