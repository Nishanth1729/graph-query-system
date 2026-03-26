import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")


PROMPT = """
You are an expert SQL generator for SAP Order-to-Cash data.

Tables and their EXACT column names:

1. sales_order_headers(salesOrder, salesOrderType, soldToParty, totalNetAmount, overallDeliveryStatus, overallOrdReltdBillgStatus, transactionCurrency, creationDate, requestedDeliveryDate, customerPaymentTerms)

2. sales_order_items(salesOrder, salesOrderItem, material, requestedQuantity, requestedQuantityUnit, netAmount, materialGroup, productionPlant, storageLocation, salesDocumentRjcnReason, itemBillingBlockReason)

3. outbound_delivery_headers(deliveryDocument, creationDate, shippingPoint, overallGoodsMovementStatus, overallPickingStatus, deliveryBlockReason, headerBillingBlockReason, actualGoodsMovementDate)

4. outbound_delivery_items(deliveryDocument, deliveryDocumentItem, referenceSdDocument, referenceSdDocumentItem, actualDeliveryQuantity, deliveryQuantityUnit, plant, storageLocation, batch)

5. billing_document_headers(billingDocument, billingDocumentType, soldToParty, totalNetAmount, transactionCurrency, billingDocumentDate, billingDocumentIsCancelled, cancelledBillingDocument, companyCode, fiscalYear, accountingDocument, creationDate)

6. billing_document_items(billingDocument, billingDocumentItem, material, billingQuantity, billingQuantityUnit, netAmount, transactionCurrency, referenceSdDocument, referenceSdDocumentItem)

7. payments_accounts_receivable(companyCode, fiscalYear, accountingDocument, accountingDocumentItem, customer, amountInTransactionCurrency, transactionCurrency, amountInCompanyCodeCurrency, clearingDate, clearingAccountingDocument, postingDate, documentDate, invoiceReference, salesDocument, glAccount)

Relationships:
- sales_order_headers.salesOrder = sales_order_items.salesOrder
- outbound_delivery_items.referenceSdDocument = sales_order_headers.salesOrder
- outbound_delivery_headers.deliveryDocument = outbound_delivery_items.deliveryDocument
- billing_document_items.referenceSdDocument = outbound_delivery_items.deliveryDocument
- billing_document_headers.billingDocument = billing_document_items.billingDocument
- billing_document_headers.accountingDocument = payments_accounts_receivable.accountingDocument

Rules:
- ALWAYS use the exact camelCase column names listed above
- NEVER invent column names not listed above
- Use LEFT JOIN when checking for missing/incomplete data
- Use INNER JOIN when both sides must exist
- Return ONLY the SQL query, no explanation
- Always include LIMIT 20
- Column names are case-sensitive — use exact casing

Examples:

User: Find deliveries without billing documents
SQL:
SELECT dh.deliveryDocument, dh.creationDate
FROM outbound_delivery_headers dh
LEFT JOIN billing_document_items bi
ON dh.deliveryDocument = bi.referenceSdDocument
WHERE bi.billingDocument IS NULL
LIMIT 20;

User: Show cancelled billing documents
SQL:
SELECT billingDocument, billingDocumentDate, totalNetAmount, transactionCurrency
FROM billing_document_headers
WHERE billingDocumentIsCancelled = 1
LIMIT 20;

User: Show sales orders with their materials
SQL:
SELECT h.salesOrder, h.soldToParty, i.material, i.requestedQuantity, i.netAmount
FROM sales_order_headers h
INNER JOIN sales_order_items i ON h.salesOrder = i.salesOrder
LIMIT 20;

User Query:
{query}
"""


def call_llm(query):
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": PROMPT.format(query=query)}
                ]
            }
        )

        data = res.json()

        if "choices" not in data:
            print("❌ LLM ERROR:", data)
            return None

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ EXCEPTION:", e)
        return None


def extract_sql(text):
    if not text:
        return None

    # Case 1: SQL inside ```sql ... ```
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Case 2: SQL inside plain ``` ... ```
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        candidate = match.group(1).strip()
        if candidate.lower().startswith("select"):
            return candidate

    # Case 3: Plain SQL anywhere in the text (handles leading newlines/spaces)
    match = re.search(r"(SELECT\s+.+?)(?:;|$)", text, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
        if not sql.endswith(";"):
            sql += ";"
        return sql

    return None


def generate_sql(query):
    raw = call_llm(query)

    print("🔎 RAW LLM:", raw)

    sql = extract_sql(raw)

    if not sql:
        print("⚠️ Using fallback SQL")
        return "SELECT * FROM deliveries LIMIT 10;"

    return sql