from collections import defaultdict
def function_mapping(df):
    """
    Create a dictionary to access all columns of function names and their associated parameters, together with the columns of actual usage
    """
    # create dictionary to access all columns of function names and their associated parameters, together with the columns of actual usage


    # determine the last start of the relevant columns (starts after the column "messages")
    num_column_start = df.columns.get_loc("messages")
    # Given column names
    column_names = df.columns[num_column_start:].tolist() # All columns after the 'messages' column

    # # Define shared parameters
    # shared_parameters = {
    #     'parameter_date': ['function_wine_selection_or_offers','function_fruit_and_veg_offers', 'function_wine_selection_or_offers', 'function_fridge_items']
    # }
    # Data structure to store function and associated parameters
    function_map = defaultdict(lambda: {"parameters": [], "used_parameters": []})

    current_function = None
    # Parse columns and fill the dictionary
    for col in column_names:
        if col.startswith('function_'):
            current_function = col
            function_map[current_function]['used'] = column_names[column_names.index(col) + 1]  # Assume the next column is used_function
        elif col.startswith('parameter_') or col.startswith('optional parameter_'):
            if current_function:
                function_map[current_function]['parameters'].append(col)
                function_map[current_function]['used_parameters'].append(column_names[column_names.index(col) + 1])

    # # Now handle shared parameters (only needed in the 'old' csv file)
    # for param, functions in shared_parameters.items():
    #     used_param = 'used_' + param.split('_')[1]  
    #     for function in functions:
    #         if param not in function_map[function]['parameters']:
    #             function_map[function]['parameters'].append(param)
    #             function_map[function]['used_parameters'].append(used_param)


    # # remove 'parameter_measurements' and 'used_parameter_measurements' from the dictionary
    # for function, details in function_map.items():
    #     if 'parameter_measurements' in details['parameters']:
    #         details['parameters'].remove('parameter_measurements')
    #     if 'used_parameter_measurements' in details['used_parameters']:
    #         details['used_parameters'].remove('used_parameter_measurements')
    return function_map