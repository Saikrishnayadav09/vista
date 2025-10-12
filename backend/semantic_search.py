import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from backend.language import translate_text

# Load data and model once
df = pd.read_csv("C:\\Users\\DELL\\OneDrive\\Desktop\\vista\\vista\\backend\\cleaned_banking_data_v2.csv")
model = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = model.encode(df['question'].tolist(), convert_to_tensor=True)

def get_best_answer(user_query, source_lang='auto', top_k=1):
    translated_query = translate_text(user_query, source=source_lang, target='en')
    query_embedding = model.encode([translated_query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding.cpu(), question_embeddings.cpu())[0]
    top_idx = np.argsort(similarities)[:top_k]
    result_row = df.iloc[top_idx[0]]
    translated_answer = translate_text(result_row['answer'], source='en', target=source_lang)
    return {
        "original_question": user_query,
        "translated_question": translated_query,
        "matched_dataset_question": result_row['question'],
        "translated_answer": translated_answer
    }
