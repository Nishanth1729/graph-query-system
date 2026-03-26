def build_graph():
    return {
        "nodes": [
            {"id": "Customer"},
            {"id": "Order"},
            {"id": "Delivery"},
            {"id": "Invoice"},
            {"id": "Payment"},
            {"id": "Product"}
        ],
        "edges": [
            {"source": "Customer", "target": "Order"},
            {"source": "Order", "target": "Delivery"},
            {"source": "Delivery", "target": "Invoice"},
            {"source": "Invoice", "target": "Payment"},
            {"source": "Order", "target": "Product"}
        ]
    }


def extract_ids(rows):
    ids = []
    for row in rows:
        for val in row:
            if isinstance(val, str):
                ids.append(val)
    return list(set(ids))