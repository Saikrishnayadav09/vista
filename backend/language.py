from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en'  # fallback

def translate_text(text, source='auto', target='en'):
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return text 