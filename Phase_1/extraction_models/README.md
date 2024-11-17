# **The Extraction Layer**

This layer categorizes user prompts into six general buckets to streamline functionality and enhance efficiency.

---

## **How It Works**

For detailed information about client operations, refer to the [Workflow Documentation](./idea/Workflow_clients.md).

---

## **Prompt Categories**

The Extraction Layer organizes user prompts into the following six categories:

1. **File Operations**  
   Tasks involving file and directory management, such as:  
   - Opening files  
   - Writing to files  
   - Creating directories  

2. **Operating System Operations**  
   System-level tasks, including:  
   - Adjusting brightness  
   - Killing processes  
   - Changing file or directory permissions  

3. **Application-Level Operations**  
   Interactions with applications, such as:  
   - Starting a browser  
   - Searching for specific content  
   - Opening, using, or closing specific software  

4. **Network-Level Operations**  
   Tasks related to network and connectivity, including:  
   - Switching Wi-Fi or Bluetooth on and off  
   - Checking connected USB devices  

5. **Installation Operations**  
   Handling installations and updates, such as:  
   - Installing new software  
   - Running `pip install`  
   - Executing `sudo apt-get` commands  

6. **Content Generation Operations**  
   Generating and displaying content directly on the terminal.  
   **Note**: Content displayed **on the terminal** is a key focus for this category. Examples include:  
   - Printing greetings  
   - Generating formatted terminal outputs  

---

## **Adding New Models**

If you need to create new models, follow these steps:  

1. Copy the `client_500x.py` code into a new file.  
2. Update the port number for the new client.  
3. Configure the sequencer to broadcast prompts to the new model. For more details visit the [sequencer](../Sequencer) 
4. Add the new model's prompt to the [Prompt File](./Ex_address.py).  

---

## **Additional Notes**

> **Note**:  
> This framework is designed to be extensible. By leveraging the categorized buckets, developers can easily create or expand upon existing functionalities without disrupting the overall structure.
