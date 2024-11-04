
function_dict = {
'client_5001': 'Check for file operations',
'client_5002': 'Check for OS operations',
'client_5003': 'Check for application operations',
'client_5004': 'check for network operations',
'client_5005': 'check for installation operations',
'client_5006': 'check for content generation operations'
}

prompt_init_dict = {
	'client_5001_init': f"""
							You will be given a prompt and some history. Your task is to figure out if the given prompt requires any file operations.

							File operations means:
							1. If the user wants to open, close, read, write, create, delete etc. has anything to do with files.
							2. We are not restricted to files, if the user wants to create a directory, then it required file operations as well.
							3. Any user request (based on the history as well) that requires them to perform operations in a file.
							4. There may be more cases which you will have to judge accordingly.

							If the prompt has anything to do with file operations, output a simple "yes".
							If the prompt has nothing to do with file operations, output a simple "no".

							Eg. Write a 500 word essay in a file in desktop
							your output = yes

							reason > writing a file to desktop means there are file operations being performed here. 

							Eg. Crack the hash "abcd" and write the answer to a new directory in the desktop, create a file.
							your output = yes

							reason > creating a directory and file are file operations.
						""",
	'client_5002_init': f"""
							You will be given a prompt and some history. Your task is to figure out if the given prompt requires any OS operations.

							OS level operations means:
							1. If the user wants to get the number of CPU cores, the total available storage, or any processor or hardware related information.
							2. If the user wants to change file permissions, kill running process, anything that might involve the use of systemctl in linux.
							3. If the user wants to reboot, install an update, shut down the computer. 
							4. If the user wants to change brightness, change volume etc.
							5. There might be more cases, but use these examples to create a sphere of possible entries in this category.

							If the prompt has anything to do with OS level operations, output a simple "yes".
							If the prompt has nothing to do with OS level operations, output a simple "no".

						""",
	'client_5003_init': f"""
							you will be given a prompt and some history. Your task is to figure out if the given prompt requires any application operations.
							
							Application level operations means:
							1. If the user wants to open or close an application like a web-browser 
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
				    You will be given a prompt and a history of prompts and responses. The user wants to perform some file operations. 
				    File operations means:
							1. If the user wants to open, close, read, change permissions, write, create, delete etc. has anything to do with files.
							2. We are not restricted to files, if the user wants to create a directory, then it required file operations as well.
							3. Any user request (based on the history as well) that requires them to perform operations in a file.
							4. There may be more cases which you will have to judge accordingly.

					Your task is two folds, 

				    1. Generate a json type object that contains necessary fields for the action the user wants to perform.
				    2. Generate a summary in less than 20 words, of what you did and the necessary parameters to achieve the user's actions.

				    First output the json object. It should be formatted exactly as below. It should begin with three '@' followed by the word 'json', that is, '@@@json' 
				    and it should end with three '@', that is, '@@@'.
				    
				    @@@json
				    'param_1': 'value_1',
				    'param_2': 'value_2',
				    ...
				    'param_n': 'value_n'
				    @@@
				    
				    After this, output the summary. It should be formatted exactly as below. It should begin with three "$" followed by the word 'summary', that is, '$$$summary'
				    and it should end with three '$', that is, '$$$'.

				    $$$summary
				    <text here>
				    $$$

				    That's it.
				    """,

	"client_5002": f"""
				    You will be given a prompt and a history of prompts and responses. The user wants to perform some OS level operations. 

				    os level operations means:
							1. If the user wants to get the number of CPU cores, the total available storage, or any processor or hardware related information.
							2. If the user wants to change file permissions, kill running process, anything that might involve the use of systemctl in linux.
							3. If the user wants to reboot, install an update, shut down the computer. 
							4. If the user wants to change brightness, change volume etc.
							5. There might be more cases, but use these examples to create a sphere of possible entries in this category.

				    Your task is two folds, 

				    1. Generate a json type object that contains necessary fields for the action the user wants to perform.
				    2. Generate a summary in less than 20 words, of what you did and the necessary parameters to achieve the user's actions.

				    First output the json object. It should be formatted exactly as below. It should begin with three '@' followed by the word 'json', that is, '@@@json' 
				    and it should end with three '@', that is, '@@@'.
				    
				    @@@json
				    'param_1': 'value_1',
				    'param_2': 'value_2',
				    ...
				    'param_n': 'value_n'
				    @@@
				    
				    After this, output the summary. It should be formatted exactly as below. It should begin with three "$" followed by the word 'summary', that is, '$$$summary'
				    and it should end with three '$', that is, '$$$'.

				    $$$summary
				    <text here>
				    $$$

				    That's it.
				    """,

	"client_5003": f"""
				    You will be given a prompt and a history of prompts and responses. The user wants to perform some application level operations. Your task is two folds, 

				    1. Generate a json type object that contains necessary fields for the action the user wants to perform.
				    2. Generate a summary in less than 20 words, of what you did and the necessary parameters to achieve the user's actions.

				    First output the json object. It should be formatted exactly as below. It should begin with three '@' followed by the word 'json', that is, '@@@json' 
				    and it should end with three '@', that is, '@@@'.
				    
				    @@@json
				    'param_1': 'value_1',
				    'param_2': 'value_2',
				    ...
				    'param_n': 'value_n'
				    @@@
				    
				    After this, output the summary. It should be formatted exactly as below. It should begin with three "$" followed by the word 'summary', that is, '$$$summary'
				    and it should end with three '$', that is, '$$$'.

				    $$$summary
				    <text here>
				    $$$

				    That's it.
				    """,
	"client_5004": f"""
				    You will be given a prompt and a history of prompts and responses. The user wants to perform some network level operations. Your task is two folds, 

				    1. Generate a json type object that contains necessary fields for the action the user wants to perform.
				    2. Generate a summary in less than 20 words, of what you did and the necessary parameters to achieve the user's actions.

				    First output the json object. It should be formatted exactly as below. It should begin with three '@' followed by the word 'json', that is, '@@@json' 
				    and it should end with three '@', that is, '@@@'.
				    
				    @@@json
				    'param_1': 'value_1',
				    'param_2': 'value_2',
				    ...
				    'param_n': 'value_n'
				    @@@
				    
				    After this, output the summary. It should be formatted exactly as below. It should begin with three "$" followed by the word 'summary', that is, '$$$summary'
				    and it should end with three '$', that is, '$$$'.

				    $$$summary
				    <text here>
				    $$$

				    That's it.
				    """,
	"client_5005": f"""
				    You will be given a prompt and a history of prompts and responses. The user wants to perform some installation level operations. Your task is two folds, 

				    1. Generate a json type object that contains necessary fields for the action the user wants to perform.
				    2. Generate a summary in less than 20 words, of what you did and the necessary parameters to achieve the user's actions.

				    First output the json object. It should be formatted exactly as below. It should begin with three '@' followed by the word 'json', that is, '@@@json' 
				    and it should end with three '@', that is, '@@@'.
				    
				    @@@json
				    'param_1': 'value_1',
				    'param_2': 'value_2',
				    ...
				    'param_n': 'value_n'
				    @@@
				    
				    After this, output the summary. It should be formatted exactly as below. It should begin with three "$" followed by the word 'summary', that is, '$$$summary'
				    and it should end with three '$', that is, '$$$'.

				    $$$summary
				    <text here>
				    $$$

				    That's it.
				    """,
	"client_5006": f"""
				    You will be given a prompt and a history of prompts and responses. The user wants to perform some content genration operations. Your task is two folds, 

				    1. Generate a json type object that contains necessary fields for the action the user wants to perform.
				    2. Generate a summary in less than 20 words, of what you did and the necessary parameters to achieve the user's actions.

				    First output the json object. It should be formatted exactly as below. It should begin with three '@' followed by the word 'json', that is, '@@@json' 
				    and it should end with three '@', that is, '@@@'.
				    
				    @@@json
				    'param_1': 'value_1',
				    'param_2': 'value_2',
				    ...
				    'param_n': 'value_n'
				    @@@
				    
				    After this, output the summary. It should be formatted exactly as below. It should begin with three "$" followed by the word 'summary', that is, '$$$summary'
				    and it should end with three '$', that is, '$$$'.

				    $$$summary
				    <text here>
				    $$$

				    That's it.
				    """,

}