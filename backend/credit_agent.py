from backend.db_connector import run_query

def handle_credit_query(customer_id, transaction_period):
    """
    Retrieves credit transactions for a customer in a given day, month, or year.
    transaction_period can be: '2024-05' (month), '2024-05-12' (day), or '2024' (year)
    """
    sql = f"""
    SELECT [Date], [Merchant], [Category], [Amount (INR)], [Type], [Description]
    FROM credit_transactions 
    WHERE [Customer ID] = '{customer_id}' 
    AND [Date] LIKE '{transaction_period}%'
    ORDER BY [Date] ASC
    """

    rows = run_query(sql, db_path='transactions.db')

    if not rows:
        return f"❌ No credit transactions found for Customer ID {customer_id} in {transaction_period}."

    response = f"\n📄 Credit Transactions for {customer_id} in {transaction_period}:\n"
    for row in rows:
        try:
            response += (
                f"🗓️ Date: {row[0]}\n"
                f"🏬 Merchant: {row[1]}\n"
                f"🏷️ Category: {row[2]}\n"
                f"💰 Amount: ₹{row[3]}\n"
                f"🔁 Type: {row[4]}\n"
                f"📝 Description: {row[5]}\n"
                "---------------------------\n"
            )
        except Exception as e:
            response += f"⚠️ Could not format transaction: {e}\n"

    return response

