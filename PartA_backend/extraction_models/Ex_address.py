# Create a 500 word essay on abraham lincon and save that to a file in the desktop --> This prompt is triggering 1 2 and 3. When it should trigger 1 and 3 at max. 
# Cause it does require opening of the text editor and writing content is a file application.
# Why is 2 being triggered when there are no os level operations.
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
		You will be given a prompt and some history. Your task is to determine if the given prompt requires any file operations.

		**File Operations**:
		1. If the user wants to create, open, close, read, write, or delete a file, or perform any other action related to files.
		2. Requests involving directories (e.g., creating, deleting, or managing folders) are also considered file operations.
		3. Any user request, based on the prompt or history, that involves file manipulation counts as a file operation.
		4. Examples:
		   - Writing content to a specific file path.
		   - Creating or moving files or directories.

		If the prompt requires any file operation, output "yes".
		If the prompt does not involve file operations, output "no".

		**Examples**:
		Prompt: Write a 500-word essay to a file on the desktop.
		Output: yes (reason: Writing content to a file is a file operation.)

		Prompt: Write a 500-word essay about Lincoln.
		Output: no (reason: This only requests content generation without file operations.)

		Use the history for additional context.
	""",

	'client_5002_init': f"""
		You will be given a prompt and some history. Your task is to determine if the given prompt requires any OS-level operations.

		Note on operating system applications:

		There is a difference between user programs and operating system. Any program that is not using the restricted instructions of the micro-processor and if using then using it through APIs is a user program.
		If the prompt and history demand the use of a user program then it is not an operating system level application.

		In general, you will have to classify the following as operating system operations as well. There may be more, but this is the general trend.

		**OS-Level Operations**:
		1. Requests for system information (e.g., CPU cores, available storage, hardware info).
		2. Managing system processes or configurations (e.g., changing file permissions, killing processes, using system services).
		3. Requests to perform system-wide actions like rebooting, updating, shutting down, or checking system status (e.g., battery, brightness, volume).
		4. Any other system operation that directly interacts with or required hardware information, that is, requires interaction with the operating system.
		5. Examples:
		   - Rebooting the system or viewing system settings.

		If the prompt requires any OS-level operation, output "yes".
		If the prompt does not involve OS-level operations, output "no".

		**Examples**:
		Prompt: Check the available system storage.
		Output: yes (reason: Retrieving system storage is an OS-level operation.)

		Prompt: Write a paragraph on renewable energy.
		Output: no (reason: The request only involves content generation, not system-level interaction.)

		Prompt: Write a 500 word essay on xyz and save it on the desktop.
		Output: no (reason: This requires file operations, and no direct correlation with the operating system, rather uses only user applications.)

	""",

	'client_5003_init': f"""
		You will be given a prompt and some history. Your task is to determine if the given prompt requires any application-level operations.

		**Application-Level Operations**:
		1. Opening, closing, or interacting with GUI applications (e.g., opening a web browser, viewing a PDF).
		2. Launching applications that require a graphical interface.
		3. Any operation that requires the use of an application to access or display content (e.g., opening a document in a text editor).
		4. Examples:
		   - Opening a web page in a browser or a PDF in a PDF reader.

		If the prompt requires any application-level operation, output "yes".
		If the prompt does not involve application-level operations, output "no".

		**Examples**:
		Prompt: Open the calculator app.
		Output: yes (reason: This requires launching a GUI application.)

		Prompt: List all prime numbers under 50.
		Output: no (reason: This is a content generation task without application-specific interaction.)
	""",

	'client_5004_init': f"""
		You will be given a prompt and some history. Your task is to determine if the given prompt requires any network operations.

		**Network Operations**:
		1. Managing network connections or devices (e.g., enabling/disabling Wi-Fi or Bluetooth, scanning devices).
		2. Requests involving network security or monitoring tools (e.g., using Wireshark, performing IP scans, SSH connections).
		3. Any task that requires interacting with network interfaces, such as checking IP configurations or managing Bluetooth connections.
		4. Examples:
		   - Enabling Wi-Fi, connecting to a Bluetooth device, or performing network scans.

		If the prompt requires any network-related operation, output "yes".
		If the prompt does not involve network-related operations, output "no".

		**Examples**:
		Prompt: Connect to Wi-Fi network "Home_Network".
		Output: yes (reason: Managing Wi-Fi is a network operation.)

		Prompt: Explain network topologies.
		Output: no (reason: This only involves generating content, not performing network operations.)
	""",

	'client_5005_init': f"""
		You will be given a prompt and some history. Your task is to determine if the given prompt requires any installation operations.

		**Installation Operations**:
		1. Requests to install applications, libraries, or packages (e.g., Python packages, system applications).
		2. Commands or tasks that involve "install" operations, such as "sudo apt-get install", "pip install", or "snap install".
		3. Any installation command, regardless of package type (e.g., Ruby gems, NPM packages).
		4. Examples:
		   - Installing a new application or library.

		If the prompt requires any installation operation, output "yes".
		If the prompt does not involve installation operations, output "no".

		**Examples**:
		Prompt: Install NumPy for Python.
		Output: yes (reason: This request requires installing a Python package.)

		Prompt: Describe the uses of NumPy.
		Output: no (reason: This only requests content without installation.)
	""",

	'client_5006_init': f"""
		You will be given a prompt and some history. Your task is to determine if the given prompt requires content generation operations.

		**Content Generation Operations**:
		1. Requests to generate text or information without any further action, such as "explain", "summarize", or "list".
		2. Content requests that do not require system commands (e.g., `os.system()`) or interaction with files or applications.
		3. Any prompt asking for displayed or printed content without additional operations.
		4. Examples:
		   - Generating summaries, essays, or examples.

		If the user is in a conversational tone, then the output should be "yes"

		If the prompt requires content generation, output "yes".
		If the prompt does not involve content generation, output "no".

		**Examples**:
		Prompt: Write a 300-word essay on climate change.
		Output: yes (reason: This requires content creation without other operations.)

		Prompt: Write a 300-word essay to a file on the desktop.
		Output: no (reason: This includes file operations for saving content.)
	""",
}


prompt_dict = {
	"client_5001": """
				    You will be given a prompt and a history of prompts and responses. The user wants to perform file or directory operations.

					**File or Directory Operations** are any actions that directly interact with files or directories. These include:
					  - Opening, closing, reading, writing, deleting, or creating files.
					  - Changing permissions, modifying, or listing directories.
					  - Any command that requires interaction with a file or directory based on the current prompt or history.

					**Your Task**:
					1. Generate a JSON object containing **all required parameters** for the operation based on the user's request.
					   - **Required Fields in JSON**:
					     - **operation**: Specify the action (e.g., "open", "write", "delete").
					     - **path**: Full path of the target file or directory.
					     - **additional_params**: Any other parameters relevant to the operation (e.g., "mode: read-only" for file reads, "permissions: 755" for chmod).
					   
					   There might be more relevant fields, include that as well. Include everything that is necessary.

					2. Generate a summary of the operation in **under 20 words**.
					   - The summary should **describe the action performed** and include essential parameters (e.g., "Opened file in read mode at /path/to/file").

					**Output Format**:
					- **JSON Object**: Start the JSON with `@@@json` and end it with `@@@`.
					- **Summary**: Start the summary with `$$$summary` and end it with `$$$`.

					**Example Output** (These are examples, you do not have to follow them exactly but they are a good reference point):

					@@@json
					{
					  "operation": "open",
					  "path": "/path/to/file",
					  "mode": "read-only"
					}
					@@@

					$$$summary
					Opened file in read-only mode at /path/to/file.
					$$$

					**Important**: Generate only the JSON and summary as specified, formatted exactly as instructed.


				    That's it.
				    """,

	"client_5002": """
				You will be given a prompt and a history of prompts and responses. The user wants to perform OS-level operations on their system.

				**OS-Level Operations** include any actions that interact with the operating system directly. These may include, but are not limited to:
				  1. **System Information**: Retrieving details like the number of CPU cores, total available storage, RAM usage, or other hardware-related information.
				  2. **System Management**: Managing processes, changing file permissions, using `systemctl` commands in Linux (e.g., to start, stop, enable, or disable services).
				  3. **System Control**: Rebooting, shutting down, installing updates, or other actions that affect the system's state.
				  4. **Device Settings**: Adjusting brightness, changing volume, or other hardware settings.
				  
				**Your Task**:
				1. **Generate a JSON object** that contains all necessary fields for the OS-level action requested. Tailor each field specifically to the type of operation.
				   - **Required Fields in JSON**:
				     - **operation**: Specify the action (e.g., "get_cpu_cores", "shutdown", "change_volume").
				     - **target**: Describe the target if applicable (e.g., "CPU", "volume", "brightness", or "service name" for systemctl actions).
				     - **parameters**: List any additional parameters or settings relevant to the action (e.g., "level: 75" for volume, "permissions: 755" for chmod).
				     - **confirmation_required**: Specify if the operation requires confirmation (e.g., `true` for reboot or shutdown actions).
				   
				   There might be more relevant fields, include that as well. Include everything that is necessary.

				2. **Generate a summary** of the action performed in under 20 words.
				   - The summary should **describe the action** (e.g., "Adjusted volume to 50%" or "Retrieved CPU core count").

				**Output Format**:
				- **JSON Object**: Format the JSON output exactly as shown below. Begin with `@@@json` and end with `@@@`.
				  
				@@@json
				{
				  "operation": "value",
				  "target": "value",
				  "parameters": {
				    "param_1": "value",
				    "param_2": "value",
				    ...
				  },
				  "confirmation_required": true/false
				}
				@@@

				- **Summary**: Format the summary exactly as shown below. Begin with `$$$summary` and end with `$$$`.

				$$$summary
				<summary text>
				$$$

				**Example Output** (These are examples, you do not have to follow them exactly but they are a good reference point):

				For a request to adjust system volume:
				  
				@@@json
				{
				  "operation": "change_volume",
				  "target": "volume",
				  "parameters": {
				    "level": 75
				  },
				  "confirmation_required": false
				}
				@@@

				$$$summary
				Set volume to 75%.
				$$$

				For a request to retrieve CPU core count:

				@@@json
				{
				  "operation": "get_cpu_cores",
				  "target": "CPU",
				  "parameters": {},
				  "confirmation_required": false
				}
				@@@

				$$$summary
				Retrieved CPU core count.
				$$$

				**Important**: Generate only the JSON and summary exactly as specified, following the formatting strictly.

				    """,

	"client_5003": """
				    You will be given a prompt and a history of prompts and responses. The user wants to perform application-level operations on their system.

					**Application-Level Operations** include any actions that involve opening or managing GUI applications. Examples include:
					  1. **Launching Applications**: Starting applications like a web browser, PDF reader, or media player.
					  2. **Closing Applications**: Closing an open GUI application.
					  3. **Interacting with GUI Applications**: Opening specific files (e.g., reading a PDF), visiting websites, or performing tasks that require launching a graphical user interface.
					  
					  **Note**: Application-level operations always involve actions that launch or interact with GUI-based applications. Running commands without a GUI (e.g., terminal commands) does **not** count as an application-level operation.

					**Your Task**:
					1. **Generate a JSON object** that includes all required fields for the user’s application-level action. Structure each field based on the type of application-level operation.
					   - **Required Fields in JSON**:
					     - **operation**: Specify the action (e.g., "open", "close").
					     - **application_name**: The name of the application to open or close (e.g., "Chrome", "PDF Reader").
					     - **file_path** (optional): Specify the file to open if applicable (e.g., path to a PDF for a PDF reader).
					     - **url** (optional): Specify the website URL if the action is to open a specific webpage in a browser.
					  
					   There might be more relevant fields, include that as well. Include everything that is necessary. 

					2. **Generate a summary** of the action performed in under 20 words.
					   - The summary should **describe the action** clearly and succinctly (e.g., "Opened Chrome and navigated to website" or "Closed PDF reader").

					**Output Format**:
					- **JSON Object**: Format the JSON output exactly as shown below. Begin with `@@@json` and end it with `@@@`.

					@@@json
					{
					  "operation": "value",
					  "application_name": "value",
					  "file_path": "optional value",
					  "url": "optional value"
					}
					@@@

					- **Summary**: Format the summary exactly as shown below. Begin with `$$$summary` and end with `$$$`.

					$$$summary
					<summary text>
					$$$

					**Example Outputs** (These are examples, you do not have to follow them exactly but they are a good reference point):

					1. For a request to open a PDF file with a PDF reader:
					  
					@@@json
					{
					  "operation": "open",
					  "application_name": "PDF Reader",
					  "file_path": "/path/to/document.pdf"
					}
					@@@

					$$$summary
					Opened PDF Reader with document at /path/to/document.pdf.
					$$$

					2. For a request to close a browser:
					  
					@@@json
					{
					  "operation": "close",
					  "application_name": "Chrome"
					}
					@@@

					$$$summary
					Closed Chrome browser.
					$$$

					3. For a request to open a website in Chrome:

					@@@json
					{
					  "operation": "open",
					  "application_name": "Chrome",
					  "url": "https://example.com"
					}
					@@@

					$$$summary
					Opened Chrome and navigated to https://example.com.
					$$$

					**Important**: Generate only the JSON and summary exactly as specified, following the formatting strictly.

				    """,
	"client_5004": """
				    You will be given a prompt and a history of prompts and responses. The user wants to perform network-level operations on their system.

					**Network-Level Operations** include any actions related to network management, monitoring, and device connectivity. Examples include:
					  1. **Managing Connections**: Switching on or off Wi-Fi or Bluetooth, and listing available devices for these connections.
					  2. **Device Connectivity**: Checking which devices are connected via USB, Bluetooth, or other network interfaces.
					  3. **Network Monitoring**: Using tools like Wireshark for packet recording, or Aircrack-ng for analyzing Wi-Fi networks (e.g., packet recording, password cracking).
					  4. **IP and Port Scans**: Running IP scans, connecting to a specific IP and port, or using SSH, OpenSSL, or similar tools.
					  
					  **Note**: These tasks do not require a GUI application. Network-level operations may involve command-line utilities but should pertain strictly to networking, connectivity, or device communication.

					**Your Task**:
					1. **Generate a JSON object** that includes all necessary fields for the user’s network-level action. Tailor each field specifically to the type of operation.
					   - **Required Fields in JSON**:
					     - **operation**: Specify the action (e.g., "turn_on_wifi", "scan_network", "connect_via_ssh").
					     - **target**: Describe the target device, IP address, or interface if applicable (e.g., "Wi-Fi", "00:11:22:33:44:55" for a Bluetooth device, or "192.168.1.1").
					     - **parameters**: List additional parameters relevant to the action (e.g., "port: 22" for SSH, "timeout: 60s" for a scan).
					     - **confirmation_required**: Specify if the operation requires confirmation (e.g., `true` for sensitive actions like network scans).
					   
					   There might be more relevant fields, include that as well. Include everything that is necessary. 

					2. **Generate a summary** of the action performed in under 20 words.
					   - The summary should **describe the action** briefly and clearly (e.g., "Turned on Wi-Fi" or "Scanned network for active devices").

					**Output Format**:
					- **JSON Object**: Format the JSON output exactly as shown below. Begin with `@@@json` and end with `@@@`.

					@@@json
					{
					  "operation": "value",
					  "target": "value",
					  "parameters": {
					    "param_1": "value",
					    "param_2": "value",
					    ...
					  },
					  "confirmation_required": true/false
					}
					@@@

					- **Summary**: Format the summary exactly as shown below. Begin with `$$$summary` and end with `$$$`.

					$$$summary
					<summary text>
					$$$

					**Example Outputs** (These are examples, you do not have to follow them exactly but they are a good reference point):

					1. For a request to turn on Wi-Fi:

					@@@json
					{
					  "operation": "turn_on_wifi",
					  "target": "Wi-Fi",
					  "parameters": {},
					  "confirmation_required": false
					}
					@@@

					$$$summary
					Turned on Wi-Fi connection.
					$$$

					2. For a request to perform an IP scan:

					@@@json
					{
					  "operation": "scan_network",
					  "target": "192.168.1.0/24",
					  "parameters": {
					    "timeout": "30s",
					    "scan_type": "ping"
					  },
					  "confirmation_required": true
					}
					@@@

					$$$summary
					Scanned network 192.168.1.0/24 with a 30-second timeout.
					$$$

					3. For a request to connect to an IP via SSH:

					@@@json
					{
					  "operation": "connect_via_ssh",
					  "target": "192.168.1.15",
					  "parameters": {
					    "port": 22,
					    "username": "user"
					  },
					  "confirmation_required": false
					}
					@@@

					$$$summary
					Connected to 192.168.1.15 via SSH.
					$$$

					**Important**: Generate only the JSON and summary exactly as specified, following the formatting strictly.

				    """,
	"client_5005": """
					You will be given a prompt and some history. Your task is to determine if the given prompt requires any installation operations.

					**Installation Operations** include any user requests that involve adding software, packages, or dependencies to the system. Examples include:
					  1. **Installing Applications**: If the user requests the installation of a specific application, file, or other software.
					  2. **Installing Programming Packages**: Installing Python packages (e.g., via `pip install`), Ruby packages (e.g., via `gem install`), or system packages (e.g., via `sudo apt-get install` or `snap install`).
					  3. **Related Commands**: Any command that installs software, libraries, or dependencies, such as "install", "add", "setup", using commands like `sudo apt-get`, `pip install`, or similar.
					  
					  **Note**: Any operation that involves adding new software, packages, or dependencies should be categorized as an installation operation.

					**Your Task**:
					1. **Generate a JSON object** containing all necessary fields for the installation action specified by the user. Each field should be tailored to the installation requirements.
					   - **Required Fields in JSON**:
					     - **operation**: Specify the action, such as "install_application" or "install_package".
					     - **package_name**: Specify the name of the application or package to be installed (e.g., "numpy", "curl").
					     - **install_method**: Specify the installation method (e.g., "apt-get", "pip", "snap").
					     - **options**: Include any additional options or flags (e.g., `--upgrade` for pip).

					  There might be more relevant fields, include that as well. Include everything that is necessary.

					2. **Generate a summary** of the installation action performed in under 20 words.
					   - The summary should **describe the action** concisely and clearly (e.g., "Installed numpy using pip" or "Installed curl via apt-get").

					**Output Format**:
					- **JSON Object**: Format the JSON output exactly as shown below. Begin with `@@@json` and end it with `@@@`.

					@@@json
					{
					  "operation": "value",
					  "package_name": "value",
					  "install_method": "value",
					  "options": ["optional_value_1", "optional_value_2", ...]
					}
					@@@

					- **Summary**: Format the summary exactly as shown below. Begin with `$$$summary` and end it with `$$$`.

					$$$summary
					<summary text>
					$$$

					**Example Outputs** (These are examples, you do not have to follow them exactly but they are a good reference point):

					1. For a request to install numpy using pip:

					@@@json
					{
					  "operation": "install_package",
					  "package_name": "numpy",
					  "install_method": "pip",
					  "options": ["--upgrade"]
					}
					@@@

					$$$summary
					Installed numpy with pip and upgrade flag.
					$$$

					2. For a request to install VLC using apt-get:

					@@@json
					{
					  "operation": "install_application",
					  "package_name": "vlc",
					  "install_method": "apt-get",
					  "options": []
					}
					@@@

					$$$summary
					Installed VLC using apt-get.
					$$$

					**Important**: Generate only the JSON and summary exactly as specified, following the formatting strictly.

	""",
	"client_5006": """
					You will be given a prompt and a history of prompts and responses. The user wants to perform a content generation operation.

					**Content Generation Operations** include requests where the user requires generated content only, without any command execution or system-level operations. Examples include:
					  1. **Direct Content Creation**: The user requests text, messages, summaries, examples, or other content without needing interaction with the operating system.
					  2. **No System Commands**: The request does not involve system-level commands (e.g., `os.system()` in Python) or require interacting with applications or files.
					  3. **Output-Only**: The generated content only needs to be displayed or printed without further processing or external action.

					**Your Task**:
					1. **Generate a JSON object** containing necessary fields for the content generation action requested by the user. Include only fields relevant to the content generation request.
					   - **Required Fields in JSON**:
					     - **operation**: Describe the action, such as "generate_text", "summarize_content", or "generate_example".
					     - **content_type**: Specify the type of content requested (e.g., "text", "summary", "example").
					     - **details**: Include any additional details relevant to the content (e.g., "Generate a summary of the provided paragraph").

					  There might be more relevant fields, include that as well. Include everything that is necessary.

					2. **Generate a summary** of the content generation action in under 20 words.
					   - The summary should **clearly state the content generation task performed** (e.g., "Generated a summary of the input text" or "Created an example based on user input").

					**Output Format**:
					- **JSON Object**: Format the JSON output exactly as shown below. Begin with `@@@json` and end it with `@@@`.

					@@@json
					{
					  "operation": "value",
					  "content_type": "value",
					  "details": "value"
					}
					@@@

					- **Summary**: Format the summary exactly as shown below. Begin with `$$$summary` and end it with `$$$`.

					$$$summary
					<summary text>
					$$$

					**Example Outputs** (These are examples, you do not have to follow them exactly but they are a good reference point):

					1. For a request to generate an example sentence:

					@@@json
					{
					  "operation": "generate_example",
					  "content_type": "text",
					  "details": "Generate an example sentence using the word 'inquisitive'."
					}
					@@@

					$$$summary
					Generated an example sentence with the word 'inquisitive'.
					$$$

					2. For a request to summarize a paragraph:

					@@@json
					{
					  "operation": "summarize_content",
					  "content_type": "summary",
					  "details": "Summarize the provided paragraph on climate change."
					}
					@@@

					$$$summary
					Created a summary of the paragraph on climate change.
					$$$

					**Important**: Follow the formatting strictly and generate only the JSON and summary as specified.

				    """,

}