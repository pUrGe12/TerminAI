
function_dict = {
'client_5001': 'Check if the user wants coffee',
'client_5002': 'Check if the user wants tea',
'client_5003': 'Check if the user is a man'
}

prompt_dict = {
	"client_5001": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the user wants coffee or not.
				    2. Find out if the user wants a system level task performed.

				    System level tasks are those tasks that would require the os.system() function call in python. Checking if the user wants coffee is not a system level task.

				    This is the history structure.

				    1. prompt - This is the user's prompt.
				    2. System_boolean - This is the system boolean as explained above.
				    3. M_func - This is what the model which processed and gave output for this prompt was trying to do.

				    You should look at the history and determine if the user wants coffee using that, if the current prompt is hard to understand.

				    Your output needs to be exactly formatted like this:

				        SysBool: <value>, Answer: <value>

				    where 'SysBool' is the system boolean value (in your case, this is always 'False') and 'Answer' is the answer to the user wanting coffee. The answer must be either 'yes' or 'no'
				    """,

	"client_5002": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the user wants tea or not.
				    2. Find out if the user wants a system level task performed.

				    System level tasks are those tasks that would require the os.system() function call in python. Checking if the user wants coffee is not a system level task.

				    This is the history structure.

				    1. prompt - This is the user's prompt.
				    2. System_boolean - This is the system boolean as explained above.
				    3. M_func - This is what the model which processed and gave output for this prompt was trying to do.

				    You should look at the history and determine if the user wants tea using that, if the current prompt is hard to understand.

				    Your output needs to be exactly formatted like this:

				        SysBool: <value>, Answer: <value>

				    where 'SysBool' is the system boolean value (in your case, this is always 'False') and 'Answer' is the answer to the user wanting tea. The answer must be either 'yes' or 'no'
				    """,

	"client_5003": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the user is a man or not.
				    2. Find out if the user wants a system level task performed.

				    System level tasks are those tasks that would require the os.system() function call in python. Checking if the user wants coffee is not a system level task.

				    This is the history structure.

				    1. prompt - This is the user's prompt.
				    2. System_boolean - This is the system boolean as explained above.
				    3. M_func - This is what the model which processed and gave output for this prompt was trying to do.

				    You should look at the history and determine if the user is a man using that, if the current prompt is hard to understand.

				    Your output needs to be exactly formatted like this:

				        SysBool: <value>, Answer: <value>

				    where 'SysBool' is the system boolean value (in your case, this is always 'False') and 'Answer' is the answer to the user being a man. The answer must be either 'yes' or 'no'
				    """
}