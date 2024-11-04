
function_dict = {
'client_5001': 'Check for file operations',
'client_5002': 'Check for os operations',
'client_5003': 'Check for application operations',
'client_5004': 'check for network operations',
'client_5005': 'check for installation operations',
'client_5006': 'check for content generation operations'
}

prompt_init_dict = {
	'client_5001_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any file operations.

							<add details here>
						""",
	'client_5002_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any os operations.

							<add details here>
						""",
	'client_5003_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any application operations.
							
							<add details here>
						""",
	'client_5004_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any network operations.

							<add details here>
						""",
	'client_5005_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any installation operations.

							<add details here>
						""",
	'client_5006_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any content generation operations.

							<add details here>							
						""",
}

prompt_dict = {
	"client_5001": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the .
				    2. Find out if the user wants a system level task performed.

				    System level tasks are those tasks that would require the os.system() function call in python. Checking if the user wants coffee is not a system level task.

				    This is the history structure.

				    1. prompt - This is the user's prompt.
				    2. System_boolean - This is the system boolean as explained above.
				    3. M_func - This is what the model which processed and gave output for this prompt was trying to do.

				    You should look at the history and determine if the user wants coffee using that, if the current prompt is hard to understand.

				    Your output needs to be exactly formatted like this:

				        , Answer: <value>

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
				    """,
	"client_5004": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the .
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
	"client_5005": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the .
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
	"client_5006": f"""
				    You will be given a prompt and a history of prompts. Your task is to do this:

				    1. Find out if the .
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

}