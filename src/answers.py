import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI()

# Calculate the path to the root directory (one level up from the script directory)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# Now you can use the same import statements regardless of execution context
from src.utils import *
from config.config import *





def generate_answer_string(function_name, params, response, summary_flag=False):
    """Generate the answer string for the LLM. If summary_flag is set to true, calls an LLM to summarize the answer (where appropriate)."""
    if function_name == 'get_current_date':
        return format_current_date(response)
    elif function_name == 'find_recipe':
        return format_recipe_list(params, response, summary_flag)
    elif function_name == 'get_recipe_info':
        return format_recipe_info(params, response, summary_flag)
    elif function_name == 'fruit_and_veg_offers':
        return format_fruit_and_veg_offers(response, None)
    elif function_name == 'wine_selection_or_offers':
        return format_wine_selection_or_offers(response, params)
    elif function_name == 'fridge_items':
        return format_fridge_items(response)
    elif function_name == 'wine_pairing':
        return format_wine_pairing(params, response, summary_flag)
    elif function_name == 'dish_pairing_for_wine':
        return format_dish_pairing_for_wine(params, response, summary_flag)
    elif function_name  == 'image_classification':
        return format_image_classification(params, response, summary_flag)
    elif function_name == 'compute_shopping_list':
        return "The shopping list has been created successfully."
    elif function_name == 'translate':
        return response.get('data', {}).get('translations', [])[0].get('translatedText', 'No translation available.')
        


def format_fruit_and_veg_offers(vegetable_list, params=None):
    """Format the list of fruit and vegetable offers into a readable string."""
    fruit_and_veg_string = "This week, the following offers for fruit and vegetables are available: "
    for item in vegetable_list:
        fruit_and_veg_string += f"{item[1]} (EUR {item[2]}), "
    # Strip the trailing comma and space
    return fruit_and_veg_string[:-2]

def format_wine_selection_or_offers(wine_list, params):
    """Format the list of wine selections or offers into a readable string based on provided parameters."""
    wine_type = params.get('wine_type', None)
    date = params.get('date', None)

    if wine_type:
        wine_type_text = f"{wine_type} wines"
    else:
        wine_type_text = "wines"

    if date is not None:
        wine_selection_or_offers_string = f"This week, the following {wine_type_text} are available: "
    else:
        wine_selection_or_offers_string = f"The following {wine_type_text} are available: "

    for item in wine_list:
        if date is not None:
            wine_selection_or_offers_string += f"{item[1]} (EUR {item[2]}, originally EUR {item[3]}), "
        else:
            wine_selection_or_offers_string += f"{item[1]} (EUR {item[2]}), "

    # Strip the trailing comma and space
    return wine_selection_or_offers_string[:-2]
    
def format_fridge_items(fridge_items):
    """Format the list of fridge items into a readable string."""
    fridge_string = f"In your fridge, you have the following items: {fridge_items[0][0]}."
    return fridge_string

def format_current_date(date):
    """Format the current date into a readable string."""
    return f"Today is {date}."

def format_recipe_info(params, response, summary_flag=False):
    """Format the recipe information into a readable string based on provided parameters and summary flag."""
    # Start with the title and ID
    recipe_info = f"Title: {response.get('title', 'No Title')}, ID: {params['recipe_id']} "
    list_keys = params.get('list_keys', [])

    # Handle the time parameter
    if 'time' in list_keys:
        if response.get('isReadyInMinutes', None):
            recipe_info += f"The recipe takes {response.get('isReadyInMinutes')} minutes to prepare. "
        elif response.get('totalTime', None):
            recipe_info += f"The recipe takes {response.get('totalTime')} minutes to prepare. "
        elif response.get('prepTime', None) or response.get('cookTime', None):
            prep_time = response.get('prepTime', 'Not provided')
            cook_time = response.get('cookTime', 'Not provided')
            recipe_info += f"The recipe takes {prep_time} and {cook_time} to prepare. "

    # Handle the ingredients_id parameter
    if 'ingredients_id' in list_keys and response.get('ingredients_id', None):
        ingredient_ids = ', '.join(map(str, response.ingredients_id))
        recipe_info += f"The recipe needs ingredients with the following IDs: {ingredient_ids}. "

    # Handle the ingredients with or without measurements
    if 'ingredients' in list_keys:
        # Check if the ingredients are provided with measurements or without
        if 'measurements' in list_keys:
            ingredients_info = response.get('ingredients_with_measure', [])
        else:
            ingredients_info = response.get('ingredients_name', [])

        if summary_flag: # If summary flag is set, call LLM to summarize the ingredients
            # Summarize the ingredients
            ingredients_summary = call_llm_for_summary_recipe_info_ingredients(ingredients_info)
            recipe_info += f"Ingredients: {ingredients_summary} "
        else: # Use the ingredients as is
            if 'measurements' in list_keys: # If measurements are provided
                ingredients_str = ', '.join(
                    f"{ingredient['measures']['metric']['amount']} {ingredient['measures']['metric']['unitShort']} {ingredient['name']}"
                    for ingredient in ingredients_info
                )
                recipe_info += f"Ingredients: {ingredients_str}. "
            else: # If measurements are not provided
                ingredients_str = ', '.join(
                    ingredient for ingredient in ingredients_info
                )
                recipe_info += f"Ingredients: {ingredients_str}. "

    # Handle the instructions parameter
    if 'instructions' in list_keys:
        instructions = response.get('instructions', 'No Instructions')
        if summary_flag:
            instructions_summary = call_llm_for_summary_recipe_info_instructions(instructions)
            recipe_info += f"Instructions: {instructions_summary} "
        else:
            recipe_info += f"Instructions: {instructions}. "

    return recipe_info

def format_recipe_list(params, response, summary_flag=False):
    # after testing: a summary of the response does not make sense (LLM does not have enough context to know which information needs to be contained; might leave out IDs which are needed in following steps of the execution plan)
    num_recipes_total = response.get('totalResults', 0)
    num_recipes = response.get('number', 0)
    num_recipes = min(num_recipes, num_recipes_total) # in case where the number of recipes is less than the requested number, set num_recipes to the total number of recipes to avoid index out of range errors in the following code
    recipes = response.get('results', [])
    answer = f"There are {num_recipes_total} recipes available for your query. The first {num_recipes} are: "
    for i in range(num_recipes):
        recipe = recipes[i]
        recipe_id = recipe.get('id')
        recipe_name = recipe.get('title')
        answer += (f"{i+1}. {recipe_name} (ID: {recipe_id}) ")
    return answer

        
def format_wine_pairing(params, response, summary_flag=False):
    wine_suggestion = response.get('pairedWines', 'No wine suggestion available.')
    wine_text = response.get('pairingText', 'No wine text available.')
    wine_string = f"Suggested wine for your dish: {wine_suggestion}. {wine_text}"
    return wine_string


def format_dish_pairing_for_wine(params, response, summary_flag=False):
    food_suggestion = response.get('pairings', 'No food suggestion available.')
    food_text = response.get('text', '')
    food_string = f"Suggested food for your wine: {food_suggestion}. {food_text}"
    return food_string


def format_image_classification(params, response, summary_flag=False):
    classified_image = response.get('category', 'No image classification available.')
    answer_string = f"The image has been classified as: {classified_image}"
    return answer_string


def format_shopping_list(params, response, summary_flag=False):
    return "The shopping list has been generated successfully."

# Summarization with LLM (GPT 3.5 Turbo)
# Load env file
load_dotenv()
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)
model_gpt = "gpt-3.5-turbo"

def call_llm_for_summary_recipe_info_instructions(recipe_info):
    """Call the LLM to summarize the provided recipe information."""
    # Prepare the message for the chat completion
    recipe_info_string = f"{recipe_info}"
    response = client.chat.completions.create(model = 'gpt-3.5-turbo',
    messages=[
        {
            "role": "system",
            "content": "Please summarize the following recipe instructions: "
        },
        {
            "role": "user",
            "content": recipe_info_string
        },
    ],
    max_tokens=200  # Limit the number of tokens for the summary)
    )
    summary = response.choices[0].message.content
    return summary

def call_llm_for_summary_recipe_info_ingredients(ingredients_info):
    """Call the LLM to summarize the provided recipe information."""
    # Prepare the message for the chat completion
    response = client.chat.completions.create(model = 'gpt-3.5-turbo',
    messages=[
        {
            "role": "system",
            "content": "Please summarize the following ingredients needed for the recipe: "
        },
        {
            "role": "user",
            "content": ", ".join(ingredients_info)
        },
    ],
    max_tokens=200  # Limit the number of tokens for the summary)
    )
    summary = response.choices[0].message.content
    return summary



# def call_llm_for_summary_recipe_list(recipe_info):
#     """Call the LLM to summarize the provided recipe list."""
#     # Prepare the message for the chat completion
#     recipe_info_string = f"{recipe_info}"
#     response = client.chat.completions.create(model = 'gpt-3.5-turbo',
#     messages=[
#         {
#             "role": "system",
#             "content": "Please summarize the following list of recipes: "
#         },
#         {
#             "role": "user",
#             "content": recipe_info_string
#         },
#     ],
#     max_tokens=200  # Limit the number of tokens for the summary)
#     )
#     summary = response.choices[0].message.content
#     return summary

