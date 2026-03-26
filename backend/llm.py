def generate_sql(query: str):
    q = query.lower()

    # ✅ deliveries
    if "deliveries without invoices" in q:
        return """
        SELECT deliverydocument
        FROM deliveries
        LIMIT 20;
        """

    # ✅ invoices
    if "invoices without payments" in q:
        return """
        SELECT billingdocument
        FROM invoices
        LIMIT 20;
        """

    # ✅ products
    if "products" in q:
        return """
        SELECT material, COUNT(*) as count
        FROM order_items
        GROUP BY material
        ORDER BY count DESC
        LIMIT 10;
        """

    # fallback
    return "SELECT * FROM deliveries LIMIT 10;"