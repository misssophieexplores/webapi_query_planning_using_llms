import requests
import os
from dotenv import load_dotenv
from requests import JSONDecodeError, ConnectionError, ConnectTimeout
from typing import Optional, List

# Load env file
load_dotenv()
X_RAPIDAPI_KEY = os.getenv("X_RAPIDAPI_KEY")
X_RAPIDAPI_HOST = os.getenv("X_RAPIDAPI_HOST")

headers = {
	"X-RapidAPI-Key": X_RAPIDAPI_KEY ,
	"X-RapidAPI-Host": X_RAPIDAPI_HOST
}

# Complex Recipe Search 

food_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

headers = {
	"X-RapidAPI-Key": X_RAPIDAPI_KEY ,
	"X-RapidAPI-Host": X_RAPIDAPI_HOST
}

def find_recipe(
        query: str,
        diet: str = None,
        include_ingredients: Optional[List[str]] = None,  # Assuming this is a list of ingredient names
        exclude_ingredients: Optional[List[str]] = None,
        type: str = "main course",
        instructions_required: bool = True,
        fill_ingredients: bool = False,
        add_recipe_information: bool = False,
        cuisine: Optional[str] = None,
        exclude_cuisine: Optional[str] = None,
        max_ready_time: Optional[int] = None,
        ignore_pantry: bool = True,

        number: int = 1
        ):
    
    querystring = {
        "query": query,
        "type": type,
        "number": number
    }
    
    # Add optional parameters only if they are not None
    if diet is not None:
        querystring["diet"] = diet
    if include_ingredients is not None:
        querystring["includeIngredients"] = ",".join(include_ingredients)
    if exclude_ingredients is not None:
        querystring["excludeIngredients"] = ",".join(exclude_ingredients)
    if instructions_required is not None:
        querystring["instructionsRequired"] = str(instructions_required).lower()
    if fill_ingredients is not None:
        querystring["fillIngredients"] = str(fill_ingredients).lower()
    if cuisine is not None:
        querystring["cuisine"] = cuisine
    if exclude_cuisine is not None:
        querystring["excludeCuisine"] = exclude_cuisine
    if max_ready_time is not None:
        querystring["maxReadyTime"] = max_ready_time
    if add_recipe_information is not None:
        querystring["addRecipeInformation"] = str(add_recipe_information).lower(),
    if ignore_pantry is not None:
        querystring["ignorePantry"] = str(ignore_pantry).lower(),

        
    response = requests.get(food_url, headers=headers, params=querystring)
    return response.json()


def get_recipe_info(recipe_id: int, list_keys: list = None) -> dict:
    url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/information"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200: # Check if the response is successful
            return {"error": "Failed to fetch data"}
        data = response.json()
        answer = {'title': data.get('title', 'No Title')}
        # answer = {} # initialize an empty dictionary to store the answer
        answer = {'title': data.get('title', 'No Title')}
        # Checking if list_keys is not None and is a list
        if list_keys is not None and isinstance(list_keys, list):
            if 'time' in list_keys: # Handling 'time' key
                answer['prepTime'] = data.get('prepTime', 'Not provided')
                answer['cookTime'] = data.get('cookTime', 'Not provided')
                answer['totalTime'] = data.get('totalTime', 'Not provided')

            if 'ingredients_id' in list_keys: # Handling 'ingredients_id' key
                # Assuming ingredients are provided in a list of dictionaries under 'ingredients'
                ingredient_ids = [ingredient.get('id', 'No ID') for ingredient in data.get('ingredients', [])]
                answer['ingredients_id'] = ingredient_ids

            if 'instructions' in list_keys: # Handling 'instructions' key
                answer['instructions'] = data.get('instructions', 'No Instructions')

            if 'ingredients' in list_keys: # Check for 'ingredients' key in list_keys
                # Assuming 'extendedIngredients' is always present, but you might want to check for its existence
                extendedIngredients = data.get('extendedIngredients', [])
                if 'measurements' in list_keys:
                    # Extracting both ingredient names and their measurements
                    ingredients_and_measure = [
                        (ingredient.get('name', 'No Name'), ingredient.get('measures', {}).get('metric', 'No Measurement'))
                        for ingredient in extendedIngredients
                    ]
                    answer['ingredients_with_measure'] = ingredients_and_measure
                else:
                    # Extracting only ingredient names
                    ingredients = [ingredient.get('name', 'No Name') for ingredient in extendedIngredients]
                    answer['ingredients_name'] = ingredients
    except JSONDecodeError:
        return {"error": "Failed to decode JSON"}
    except ConnectionError:
        return {"error": "Failed to connect to the server"}
    except ConnectTimeout:
        return {"error": "Connection timed out"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    return answer

def compute_shopping_list(items_list: List[str]):
    """Given a list of items, computes a shopping list including the total a"""
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/mealplanner/shopping-list/compute"

    payload = { "items": items_list }
    headers_shopping_list = {
        "content-type": "application/json",
        "X-RapidAPI-Key": X_RAPIDAPI_KEY,
        "X-RapidAPI-Host": X_RAPIDAPI_HOST
    }
    response = requests.post(url, json=payload, headers=headers_shopping_list)

    # save the response in the folder "shopping_lists"
    # enumerate the files in the folder and save the file with the next number
    with open(f"shopping_lists/shopping_list_{len(os.listdir('shopping_lists')) + 1}.json", "w") as file:
        file.write(response.text)

    return response.json()



def image_classification(image_url: str):
    """Classify an image of food."""
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/images/classify"

    querystring = {"imageUrl": image_url}

    headers = {
        "X-RapidAPI-Key": X_RAPIDAPI_KEY,
        "X-RapidAPI-Host": X_RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()