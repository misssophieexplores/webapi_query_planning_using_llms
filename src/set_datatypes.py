import pandas as pd



#TODO: adjust for new columns
def set_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Set the data types for the columns in the DataFrame. Uses nullable datatypes.
    """
    dtype_map = {
        # 'steps': 'Int64',  # Nullable integer type
        # 'completion': 'boolean',
        'correct_functions': 'boolean',
        'correct_params': 'boolean',
        'correct_interpretation': 'boolean',
        'external_error': 'boolean',
        'api_output_correct': 'boolean',
        'comments': 'object',
        'database': 'object',
        'domain': 'object',
        'error': 'object',
        'messages': 'object',
        # # Columns that should be integers or nullable integers
        # 'function_fruit_and_veg_offers': 'Int64',
        # 'used_fruit_and_veg_offers': 'Int64',
        # 'parameter_date_fruit_and_veg_offers': 'Int64',
        # 'used_date_fruit_and_veg_offers': 'Int64',
        # 'function_wine_selection_or_offers': 'Int64',
        # 'used_wine_selection_or_offers': 'Int64',
        # 'parameter_date_wine_selection_or_offers': 'Int64',
        # 'used_date_wine_selection_or_offers': 'Int64',
        # 'function_fridge_items': 'Int64',
        # 'used_fridge_items': 'Int64',
        # 'parameter_date_fridge_items': 'Int64',
        # 'used_date_fridge_items': 'Int64',
        # 'function_date': 'Int64',
        # 'used_date': 'Int64',
        # 'function_get_recipe_info': 'Int64',
        # 'used_get_recipe_info': 'Int64',
        # 'parameter_recipe_id': 'Int64',
        # 'used_recipe_id': 'Int64',
        # 'parameter_instructions': 'Int64',
        # 'used_instructions': 'Int64',
        # 'parameter_time': 'Int64',
        # 'used_time': 'Int64',
        # 'parameter_ingredients': 'Int64',
        # 'used_ingredients': 'Int64',
        # 'parameter_measurements': 'Int64',
        # 'used_measurements': 'Int64',
        # 'function_find_recipe': 'Int64',
        # 'used_find_recipe': 'Int64',
        # 'parameter_query': 'Int64',
        # 'used_query': 'Int64',
        # 'parameter_diet': 'Int64',
        # 'used_diet': 'Int64',
        # 'parameter_include_ingredients': 'Int64',
        # 'used_include_ingredients': 'Int64',
        # 'parameter_exclude_ingredients': 'Int64',
        # 'used_exclude_ingredients': 'Int64',
        # 'parameter_type': 'Int64',
        # 'used_type': 'Int64',
        # 'parameter_cuisine': 'Int64',
        # 'used_cuisine': 'Int64',
        # 'parameter_exclude_cuisine': 'Int64',
        # 'used_exclude_cuisine': 'Int64',
        # 'parameter_max_ready_time': 'Int64',
        # 'used_max_ready_time': 'Int64',
        # 'function_dish_pairing_for_wine': 'Int64',
        # 'used_dish_pairing_for_wine': 'Int64',
        # 'parameter_grape_name': 'Int64',
        # 'used_grape_name': 'Int64',
        # 'function_wine_pairing': 'Int64',
        # 'used_wine_pairing': 'Int64',
        # 'parameter_dish_name': 'Int64',
        # 'used_dish_name': 'Int64',
        # 'function_image_classification': 'Int64',
        # 'used_image_classification': 'Int64',
        # 'parameter_image_url': 'Int64',
        # 'used_image_url': 'Int64',
        # 'function_compute_shopping_list': 'Int64',
        # 'used_compute_shopping_list': 'Int64',
        # 'parameter_items_list': 'Int64',
        # 'used_items_list': 'Int64'

    }
    # Apply the defined data types
    # Apply the dtype_map
    for column, dtype in dtype_map.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(dtype)
            except TypeError as e:
                print(f"Error converting column {column}: {e}")

    return df