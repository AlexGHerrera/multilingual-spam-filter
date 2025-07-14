import pytest
from fastapi.testclient import TestClient
from src.api_spam_multilingual import app

client = TestClient(app)

def test_predict_spam_english():
    response = client.post("/predict", json={"text": "Congratulations! You have won a prize."})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert data["original_language"] == "en"

def test_predict_spam_spanish():
    response = client.post("/predict", json={"text": "¡Felicidades! Has ganado un premio."})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert data["original_language"] == "es"

def test_predict_spam_french():
    response = client.post("/predict", json={"text": "Vous avez gagné un prix!"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert data["original_language"] == "fr"
