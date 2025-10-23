import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from backend.language import translate_text

# Load data and model once
# backend/semantic_search.py
import os
import threading

# lazy singletons
_model = None
_question_embeddings = None
_df = None
_model_lock = threading.Lock()

def _load_resources():
    """
    Try to load the model and dataset. Use a lock so concurrent requests don't load multiple times.
    If loading fails (OOM or missing libs), we set model to None and behave gracefully.
    """
    global _model, _question_embeddings, _df
    with _model_lock:
        if _model is not None or _df is not None:
            return

        try:
            import pandas as pd
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
        except Exception as e:
            # If heavy libs aren't available, we keep model as None and log the error.
            print("Semantic search libraries unavailable:", e)
            _model = None
            _df = None
            _question_embeddings = None
            return

        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(BASE_DIR, "cleaned_banking_data_v2.csv")
            _df = pd.read_csv(csv_path)
            # load a lightweight sentence transformer model (all-MiniLM-L6-v2 is small-ish)
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            # compute question embeddings (may be memory heavy if dataset is large)
            _question_embeddings = _model.encode(_df['question'].tolist(), convert_to_tensor=True)
            print("Semantic search resources loaded successfully.")
        except Exception as e:
            print("Failed to load semantic search resources:", e)
            _model = None
            _df = None
            _question_embeddings = None

def get_best_answer(user_query, source_lang='auto', top_k=1):
    """
    Public function to get best answer. If semantic resources are not available,
    return a safe fallback message that doesn't crash the web server.
    """
    # Lazy-load resources on first call
    if _model is None and _df is None:
        _load_resources()

    if _model is None or _df is None or _question_embeddings is None:
        # fallback behavior — avoid heavy computation and return a helpful message
        return {
            "original_question": user_query,
            "translated_question": user_query,
            "matched_dataset_question": None,
            "translated_answer": "Semantic search currently unavailable on this instance. Please try again later."
        }

    # If resources loaded, proceed with search
    try:
        from backend.language import translate_text
        import numpy as np
        translated_query = translate_text(user_query, source=source_lang, target='en')
        query_embedding = _model.encode([translated_query], convert_to_tensor=True)
        similarities = cosine_similarity(query_embedding.cpu(), _question_embeddings.cpu())[0]
        top_idx = np.argsort(similarities)[-top_k:][::-1]
        result_row = _df.iloc[top_idx[0]]
        translated_answer = translate_text(result_row['answer'], source='en', target=source_lang)
        return {
            "original_question": user_query,
            "translated_question": translated_query,
            "matched_dataset_question": result_row['question'],
            "translated_answer": translated_answer
        }
    except Exception as e:
        print("Error in semantic search:", e)
        return {
            "original_question": user_query,
            "translated_question": user_query,
            "matched_dataset_question": None,
            "translated_answer": "An error occurred while searching. Please try again later."
        }
