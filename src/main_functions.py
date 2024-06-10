import json
import os
import requests
import sys
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
# Calculate the path to the root directory (one level up from the script directory)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)
from config.config import *
from src.answers import *
from src.pairings import *
from src.recipe import *
from src.supermarket_and_fridge import *
from src.translation import *
from src.utils import *
from src.function_description import functions
from src.error_handling import handle_error
from src.set_datatypes import set_datatypes
from src.function_mapping import function_mapping
from src.update_function_usage import update_function_usage
from src.main_functions import *

load_dotenv()
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY) # Initialize OpenAI API client

# Configuration for retries in conversation
MAX_RETRIES = 10 # Maximum number of retries for connection with the OpenAI API
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff factor
INITIAL_RETRY_DELAY = 1  # Initial delay in seconds
MAX_FUNCTION_CALLS = 10  # Maximum number of function calls in a conversation
MAX_ERRORS = 5  # Maximum number of errors in a conversation


def main(user_prompt, model_gpt, summary_flag):
    messages = [
        {
            "role": "system",
            "content": """You are asked to complete a task by a user. Please help the user in achieving the task without asking for any additional information. If needed, make a reasonable choice and explain how you interpreted vague instructions. You might need multiple steps to complete the task. Please solve each step after the other. All steps can be solved with the help of the provided functions, for example, take note of the 'translate' or 'get_current_day' functions. Make use of them whenever possible."""
        },
        {
            "role":"user",
            "content": user_prompt
        }
    ]

    attempt_timeout = 0 # Initialize timeout attempt counter
    function_call_count = 0 # Counter for total function calls
    error_count = 0 # Counter for errors
    func_name = None  # Initialize func_name to handle it safely in exception blocks
    params = None  # Initialize params similarly
    error_log = []  # Initialize error log
    try:
        completion = client.chat.completions.create(
            model=model_gpt,
            messages=messages,
            functions=functions,
            function_call="auto",
            temperature=0
        )
        
        # Loop to handle function calls until completion
        while completion.choices[0].finish_reason == "function_call" and function_call_count < MAX_FUNCTION_CALLS:
            function_call_count += 1 # Increment function call count
            try:
                func_name = completion.choices[0].message.function_call.name # Get function name
                params = json.loads(completion.choices[0].message.function_call.arguments) # Get function parameters
                chosen_function = eval(func_name)  # Get function object from function name

                function_result = chosen_function(**params) # Call the function with parameters

                # call summarization function
                answer = generate_answer_string(func_name, params, function_result, summary_flag)

                
                messages.append({ 
                    "role": "function",
                    "name": func_name,
                    "content": f"Function: {func_name}, Parameters: {json.dumps(params)}, Result: {answer}", # append formatted answer
                    # "content": f"Function: {func_name}, Parameters: {json.dumps(params)}, Result: {str(function_result)}", 
                })
            except Exception as e:
                error_message = handle_error(e, func_name, params, messages, error_log)
                error_count += 1

                if error_count >= MAX_ERRORS:
                    break # Exit if maximum errors reached
                messages.append({"role": "system", "content": str(error_message)})

                completion = client.chat.completions.create(  # Resubmit with updated conversation
                    model=model_gpt,
                    messages=messages,
                    functions=functions,
                    function_call="auto",
                    temperature=0
                )
                continue

            completion = client.chat.completions.create( # submit the updated conversation to the model     # Loop to handle function calls until completion
                model=model_gpt,
                messages=messages,
                functions=functions,
                function_call="auto",
                temperature=0
            )
        # Append the last message
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return messages, error_log

    except requests.Timeout:
        # Handle timeout errors
        attempt_timeout += 1
        if attempt_timeout == MAX_RETRIES:
            raise  # Re-raise the timeout exception if max retries reached
        time.sleep(INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** (attempt_timeout - 1)))  # Exponential backoff
    except Exception as e:
        handle_error(e, func_name, params, messages, error_log)


    # # print the full conversation
    # print(messages)


def execution_plan(user_prompt, model_gpt, summary_flag):
    # define the functions available to the LLM
    function_catalog = functions
    messages = [
        {
            "role": "system",
            "content": f"""You are asked to complete a task by a user. Please help the user by outlining a detailed query plan in natural language. The query plan should describe the steps you would take and the functions you might use to achieve the user's goal. Here is a catalog of available functions: {json.dumps(function_catalog)}."""
        },
        {
            "role":"user",
            "content": user_prompt
        }
    ]

    attempt_timeout = 0 # Initialize timeout attempt counter
    func_name = None  # Initialize func_name to handle it safely in exception blocks
    params = None  # Initialize params similarly
    error_log = []  # Initialize error log
    try:
        completion = client.chat.completions.create(
            model=model_gpt,
            messages=messages,
            temperature=0
        )
        # Append the assistant's response
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return messages
    except requests.Timeout:
        # Handle timeout errors
        attempt_timeout += 1
        if attempt_timeout == MAX_RETRIES:
            raise  # Re-raise the timeout exception if max retries reached
        time.sleep(INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** (attempt_timeout - 1)))  # Exponential backoff
    except Exception as e:
        handle_error(e, func_name, params, messages, error_log)


def response_check(user_prompt, messages, model_gpt, summary_flag):
    # setting up a table to store in W&B
    responses = {
        "user_prompt": user_prompt,
        "messages": messages,
        "completion": None,
        "correct_functions": None,
        "correct_params": None,
        "correct_interpretation": None,
        "external_error": "False",
        "api_output_correct": None,
        "caused_error": None,
        "corrected_error": None,
        "LLM": model_gpt, 
        "comments": None,
        "summary_flag": summary_flag,
        }
    # Get number of steps as an integer
    responses["steps"] = count_function_calls(messages)

    # User inputs for T/F questions, converted to boolean
    responses["completion"] = input("Completed task? (T/F): ").strip().capitalize() == 'T'
    responses["correct_functions"] = input("Correct functions? (T/F): ").strip().capitalize() == 'T'
    responses["correct_params"] = input("Correct parameters? (T/F): ").strip().capitalize() == 'T'
    responses["correct_interpretation"] = input("Correct interpretation? (T/F): ").strip().capitalize() == 'T'
    responses["external_error"] = input("External error? (T/F): ").strip().capitalize() == 'T'
    responses["api_output_correct"] = input("API correct? (T/F): ").strip().capitalize() == 'T'
    responses["caused_error"] = input("Caused Error? (T/F): ").strip().capitalize() == 'T'
    if responses["caused_error"]:
        responses["corrected_error"] = input("Corrected Error? (T/F): ").strip().capitalize() == 'T' # Change to True/False/None

    # Adding comments, ensuring it's treated as a string
    comments_input = input("Comments: ").strip()
    responses["comments"] = " " if comments_input == None else comments_input

    return responses


def count_function_calls(messages):
    # count how many times 'role' is 'function' in messages:
    function_count = 0
    for i in messages:
        if i["role"] == "function":
            function_count += 1
    return function_count

def print_responses(responses):
    for key, value in responses.items():
        if key == "messages" or key == "user_prompt":
            continue
        else:
            print(f"{key}: {value}")


def safe_replace_na_with_none(df):
    for col in df.columns:
        # if col == 'messages':
        #     continue
        # else:
        # Check if the first element of the column is a list or a dictionary
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            print(f"Skipping column {col} due to complex data type.")
            continue  # Skip this column if it contains complex data types
        # Apply the NA replacement only to columns with scalar types
        df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)
    return df

