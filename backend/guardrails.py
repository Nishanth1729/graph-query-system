def is_domain_query(q: str):
    keywords = ["order", "invoice", "delivery", "payment", "customer", "product"]
    return any(k in q.lower() for k in keywords)


def is_safe_sql(sql: str):
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT"]
    return not any(word in sql.upper() for word in forbidden)