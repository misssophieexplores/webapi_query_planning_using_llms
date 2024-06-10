from requests import JSONDecodeError, ConnectionError, ConnectTimeout
import json

def handle_error(e, func_name, params, messages, error_log):
    if isinstance(e, JSONDecodeError):
        error_message = "JSONDecodeError"
    elif isinstance(e, ConnectionError):
        error_message = "ConnectionError"
    else:
        if func_name is not None:
            error_message = f"Error in function {func_name} with parameters {json.dumps(params)}: {str(e)}"
        else:
            error_message = f"Error: {str(e)}"
    print(error_message)
    error_log.append(error_message)
    return error_log