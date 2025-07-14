import pytest
from langdetect import detect
from deep_translator import GoogleTranslator
from src.api_spam_multilingual import preprocess_text

@pytest.mark.parametrize("text,expected_lang", [
    ("This is an English email.", "en"),
    ("Esto es un correo en español.", "es"),
    ("Ceci est un email en français.", "fr"),
])
def test_language_detection(text, expected_lang):
    _, detected_lang = preprocess_text(text)
    assert detected_lang == expected_lang

@pytest.mark.parametrize("text,expected_translation", [
    ("Esto es spam", "This is spam"),
    ("Vous avez gagné", "You have won"),
])
def test_translation_to_english(text, expected_translation):
    translated, lang = preprocess_text(text)
    assert expected_translation.lower() in translated.lower()
    assert lang != "en"
