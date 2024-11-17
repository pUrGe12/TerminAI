import re
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai
from Ex_address import function_dict, prompt_init_dict, prompt_dict
from api_keys import apikey_dict

NAME = 'client_5001'

API_KEY = str(apikey_dict.get('gemini_key'))
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

model_init = genai.GenerativeModel('gemini-pro')
chat_init = model_init.start_chat(history=[])

def M_init(user_prompt, history):
    '''
    This model is checking if this file is even required. Its very basic, outputs a True or a False, depending on whether the file is needed.
    '''
    prompt_init = prompt_init_dict.get(f"{NAME}_init") + f"""
                    This is the history: {history}
                    This is the user's prompt: {user_prompt}
    """

    try:
        output_init = ""
        response_init = chat_init.send_message(prompt_init, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })

        for chunk in response_init:
            if chunk.text:
                output_init += str(chunk.text)

        if "yes" in output_init.lower():                        # This will give just one boolean value
            return True
        else:
            return False
    except Exception as e:
        print(f'An exception occurred: {e}')
        return 'failed'


def GPT_response(user_prompt, history):
    prompt = prompt_dict.get(NAME) + f"""
                    This is the history: {history}
                    This is the user's prompt: {user_prompt}
                """
    try:
        output = ''
        response = chat.send_message(prompt, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })
        
        for chunk in response:
            if chunk.text:
                output += str(chunk.text)

        json_init = re.findall('@@@json.*@@@', output, re.DOTALL)
        json = re.findall("{.*}", json_init[0].strip(), re.DOTALL)[0].strip() # getting a nice normal string here
        work_summary = re.findall('\$\$\$summary.*\$\$\$', output, re.DOTALL)
        
        return (json, work_summary)

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return 'Try again'


if __name__ == "__main__":
    try:
        while True:
            user_prompt = input("enter: ")
            history = ''

            answer = M_init(user_prompt, history)
            print(answer)
            if answer == True:
                ''' First check if the current model is required for the prompt '''
                (json, work_summary) = GPT_response(user_prompt, history)
                print(f"json: {json}\n")
                print(f"work_summary: {work_summary}\n")
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\nShutting down...")