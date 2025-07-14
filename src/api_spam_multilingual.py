# FastAPI app for multilingual email spam detection using Hugging Face model and translation pipeline
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from langdetect import detect
from deep_translator import GoogleTranslator

# Load Hugging Face email spam model (AventIQ-AI/bert-spam-detection)
classifier = pipeline(
    "text-classification",
    model="AventIQ-AI/bert-spam-detection",
    top_k=1
)

app = FastAPI(title="Multilingual Email Spam Detection API")

class Message(BaseModel):
    text: str

# Pipeline: detect language and translate if needed
def preprocess_text(text):
    lang = detect(text)
    if lang != "en":
        try:
            translated = GoogleTranslator(source=lang, target="en").translate(text)
            return translated, lang
        except Exception as e:
            print(f"Error traduciendo: {e}")
            return text, lang
    return text, lang

from fastapi import HTTPException

@app.post("/predict")
def predict_spam(message: Message):
    try:
        if not message.text or not message.text.strip():
            raise HTTPException(status_code=400, detail="El campo 'text' no puede estar vacío.")
        # Traducción automática si no es inglés
        preprocessed_text, detected_lang = preprocess_text(message.text)
        if not preprocessed_text or not preprocessed_text.strip():
            raise HTTPException(status_code=422, detail="El texto procesado está vacío tras la traducción o el preprocesamiento.")
        # Recorta texto largo para evitar errores de BERT (>512 tokens)
        max_length = 512
        truncated_text = " ".join(preprocessed_text.split()[:max_length])
        try:
            result = classifier(truncated_text)[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al clasificar el texto: {str(e)}")
        label = result.get('label', None)
        score = float(result.get('score', 0.0))
        if label is None:
            raise HTTPException(status_code=500, detail="No se pudo obtener la etiqueta del modelo.")
        return {
            "label": label,
            "score": score,
            "original_language": detected_lang
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

