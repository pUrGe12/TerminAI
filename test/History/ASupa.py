from supabase import create_client, Client
from address import function_dict, address_dict

'''This code is going to be present with the sequencer'''

url: str = "https://yvcmpdgbeopnscegtjoh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y21wZGdiZW9wbnNjZWd0am9oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzNjAxMzUsImV4cCI6MjA0NTkzNjEzNX0.n2FKKYLLO_IhtWtjsZfNSVic5mnuXmu5dCA9mbk1SfU"

supabase: Client = create_client(url, key)

name = f'client_5001'
prompt = 'I want coffee'
system_boolean = False

'''
System boolean -> This comes from the model response.
prompt -> the sequencer already have the user's prompt.
'''

Info = {'M_addr': f"{address_dict.get(name)}", 'SysBool': f"{system_boolean}", 'M_func': f"{function_dict.get(name)}", 'Prompt': f"{prompt}"}
response = supabase.table('History').insert(Info).execute()