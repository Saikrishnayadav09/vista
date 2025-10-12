from backend.language import translate_text
from backend.credit_agent import handle_credit_query
from backend.debit_agent import handle_debit_query

class OrchestratorAgent:
    transactional_phrases = [
        "transaction history", "last transaction", "recent transactions",
        "show my transactions", "credit card transaction", "debit card transaction",
        "card statement", "account activity", "monthly statement",
        "monthly spending", "spending details"
    ]

    def is_transactional(self, query, lang='auto'):
        translated = translate_text(query, source=lang, target='en').lower()
        print("\U0001F50D Checking if transactional:", translated)

        # Reject definition/how-to type queries
        if translated.startswith("what is") or translated.startswith("how to"):
            return False

        return any(phrase in translated for phrase in self.transactional_phrases)

    def orchestrate_transaction(self, query, lang='auto', customer_id=None, transaction_month=None):
        translated = translate_text(query, source=lang, target='en').lower()

        if "debit" in translated or "debit card" in translated:
            return handle_debit_query(customer_id, transaction_month)
        elif "credit" in translated or "credit card" in translated:
            return handle_credit_query(customer_id, transaction_month)
        elif "transaction history" in translated or "transactions" in translated:
            return translate_text(
                "Do you want to see debit card transaction history or credit card transaction history?",
                source='en', target=lang
            )
        else:
            return translate_text("Could not identify transaction type. Please clarify.", source='en', target=lang)

orchestrator_agent = OrchestratorAgent()
