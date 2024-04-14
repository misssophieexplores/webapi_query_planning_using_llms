import requests
import os
from dotenv import load_dotenv

# Load env file
load_dotenv()
X_RAPIDAPI_KEY = os.getenv("X_RAPIDAPI_KEY")
X_RAPIDAPI_HOST = os.getenv("X_RAPIDAPI_HOST")
X_RAPIDAPI_HOST_TRANSLATION = os.getenv("X_RAPIDAPI_HOST_TRANSLATION")

headers = {
	"X-RapidAPI-Key": X_RAPIDAPI_KEY ,
	"X-RapidAPI-Host": X_RAPIDAPI_HOST
}


def translate(text:str):
    """Translate text from Gernan to English."""
    url = "https://google-translator9.p.rapidapi.com/v2"

    payload = {
        "q": text,
        "source": "de",
        "target": "en",
        "format": "text"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": X_RAPIDAPI_KEY,
        "X-RapidAPI-Host": X_RAPIDAPI_HOST_TRANSLATION
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()