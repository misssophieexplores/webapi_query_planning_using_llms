functions = [
    {
        "name": "get_current_date",
        "description": "Returns current the date, time, and weekday.",
        "parameters": { }
    },
    {
        "name": "is_public_holiday",
        "description": "Retrieves all public holidays of a German state. Default is 'Baden-Württemberg'.",
        "parameters": {
            "type": "object",
            "properties": {
                "state": {
                    "type": "string",
                    "description": "Name of state."
                },
            },
            "required": ["state"]
        }
    },
    {
        "name": "fruit_and_veg_offers",
        "description": "Retrieve supermarket offers for fruit and veg.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date for which the offers should be retrieved. Offers always start on a Monday of a week. Format: 'YYYY-MM-DD'."
                },
            },
            "required": ["date"]
        }
    },
    {
        "name": "wine_selection_or_offers",
        "description": "Retrieve the wine selection from the supermarket. You can filter by wine type (red, rose, white) or offers on a specific date.",
        "parameters": {
            "type": "object",
            "properties": {
                "wine_type": {
                    "type": "string",
                    "description": "Filter the wine selection by wine type. Options: 'red', 'rose', 'white'. Default is None."
                },
                "date": {
                    "type": "string",
                    "description": "Date for which the offers should be retrieved. Format: 'YYYY-MM-DD'."
                },
            },
            "required": []
        }
    },
    {
        "name": "get_recipe_info",
        "description": "Retrieves detailed information about a recipe given its ID. This information includes the recipe's title and, optionally, cooking instructions, ingredient details such as names, IDs, and measurements, as well as preparation and cooking times.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipe_id": {
                    "type": "integer",
                    "description": "The unique identifier of the recipe."
                },
                "list_keys": {
                    "oneOf": [
                        {
                            "type": "null"
                        },
                        {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    ],
                    "description": "Optional. A list of information you want to retrieve. Options include 'time' for total, preparation, and cooking times;'instructions' for cooking instructions; 'ingredients_id' for ingredient IDs; 'ingredients' for ingredient names (optionally include 'measurements' for quantities). Can be None."
                }

            },
            "required": ["recipe_id"]
        }
    },
    {
        "name": "find_recipe",
            "description": "Finds recipes based on the name, ingredients, dietary preferences, cuisines, or maximal preparation time. Returns a list of recipes with their titles, IDs, and URL for images.", 
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Name or main ingredient of recipe."
                    },
                    "diet": {
                        "type": "string",
                        "description": "Dietary preferences. Options are: 'vegetarian', 'lacto vegetarian', 'ovo vegetarian', 'vegan', 'pescetarian', 'paleo', 'primal'."
                    },
                    "include_ingredients": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Ingredients that should be included."
                    },
                    "exclude_ingredients": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Ingredients that should not be contained in the recipe."
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of meal. Default is 'main course'."
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Cuisine preferences. Options are: 'African', 'Asian', 'American', 'British', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Irish', 'Italian', 'Japanese', 'Jewish', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Southern', 'Spanish', 'Thai', 'Vietnamese'."
                    },
                    "exclude_cuisine": {
                        "type": "string",
                        "description": "Cuisines which should be avoided. Options are: 'African', 'Asian', 'American', 'British', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Irish', 'Italian', 'Japanese', 'Jewish', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Southern', 'Spanish', 'Thai', 'Vietnamese'"
                    },
                    "max_ready_time": {
                        "type": "integer",
                        "description": "Maximal time for preparation and cooking (in minutes)."
                    }
            },
            "required": ["query"]
        }
    },
    {
        "name": "translate",
        "description": "Translates German text to English.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text in German that should be translated to English."
                },
            },
            "required": ["text"]
        }
    },
    {
        "name": "dish_pairing_for_wine",
        "description": "Suggests food pairings for a given wine, providing a general description of the wine and a list of dishes that pair well with it.",
        "parameters": {
            "type": "object",
            "properties": {
                "grape_name": {
                    "type": "string",
                    "description": "The wine for which to suggest food pairings. Please provide the grape variety for best results. "
                }
            },
            "required": ["grape_name"]
        }
    },
    {
        "name": "wine_pairing",
        "description": "Provides wine pairing suggestions for a specified dish. Returns a selection of suitable wines along with a detailed description and, when applicable, a specific product recommendation.",
        "parameters": {
            "type": "object",
            "properties": {
                "dish_name": {
                    "type": "string",
                    "description": "The name of the food or dish for which wine suggestions are desired."
                }
            },
            "required": ["dish_name"]
        }
    },
    {
        "name": "image_classification",
        "description": "Retrieves the name of a dish given the URL of an image.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "The URL of an image."
                }
            },
            "required": ["image_url"]
        }
    },
    {
        "name": "compute_shopping_list",
        "description": "Adds items to a shopping list. The resulting shopping list includes the quantity and unit of each item as well as their aisle in the supermarket.",
        "parameters": {
            "type": "object",
            "properties": {
                "items_list": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of items to add to the shopping list. Each item should be a string in the format 'quantity unit item'.",
                }
            },
            "required": ["items_list"]
        }
    },
    {
        "name": "fridge_items",
        "description": "Retrieves a list of vegetables that are currently in the fridge.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The current date in the format 'YYYY-MM-DD'."
                }
            },
            "required": ["date"]
        }
    },
]