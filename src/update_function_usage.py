import pandas as pd
def update_function_usage(new_row, function_map):
    # Extract the row for easier handling if it's a DataFrame
    if isinstance(new_row, pd.DataFrame):
        new_row = new_row.iloc[0]

    # Update based on 'correct_functions'
    if pd.notna(new_row['correct_functions']) and new_row['correct_functions'] == True:
        for func, details in function_map.items():
            # Check if the function was intended to be used and not NA
            if pd.notna(new_row[func]) and new_row[func] == 1:
                new_row[details['used']] = 1  # Set used_function to 1 as intended
    elif pd.notna(new_row['correct_functions']) and new_row['correct_functions'] == False:
        for func, details in function_map.items():
            if pd.notna(new_row[func]) and new_row[func] == 1:
                new_row[details['used']] = -5  # Set to -5 as per the rule

    # Update based on 'correct_params'
    if pd.notna(new_row['correct_params']) and new_row['correct_params'] == True:
        for func, details in function_map.items():
            for param, used_param in zip(details['parameters'], details['used_parameters']):
                if pd.notna(new_row[param]) and new_row[param] == 1:
                    new_row[used_param] = 1  # Set used_parameter to 1 as intended
    elif pd.notna(new_row['correct_params']) and new_row['correct_params'] == False:
        for func, details in function_map.items():
            for param, used_param in zip(details['parameters'], details['used_parameters']):
                if pd.notna(new_row[param]) and new_row[param] == 1:
                    new_row[used_param] = -7  # Set to -7 as per the rule

    return new_row