import requests
import os
from dotenv import load_dotenv

# Load env file
load_dotenv()
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
X_RAPIDAPI_KEY = os.getenv("X_RAPIDAPI_KEY")
X_RAPIDAPI_HOST = os.getenv("X_RAPIDAPI_HOST")

headers = {
	"X-RapidAPI-Key": X_RAPIDAPI_KEY ,
	"X-RapidAPI-Host": X_RAPIDAPI_HOST
}

def dish_pairing_for_wine(grape_name: str) -> object:
    """Get dishes that pair well with a wine.
    Returns a description of the wine (key: text) and  the pairings in a list (key: pairings)."""
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/wine/dishes"

    querystring = {"wine":grape_name}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def wine_pairing(dish_name:str):
    """Get wine pairings for a dish.
    Returns suggestion for wines (key: pairedWines), a desciption of the pairing with the dish (key: pairingText) and a list of product matches (key: productMatches)."""
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/wine/pairing"
    querystring = {"food":dish_name}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()