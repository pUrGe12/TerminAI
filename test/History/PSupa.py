from supabase import create_client, Client

url: str = "https://yvcmpdgbeopnscegtjoh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y21wZGdiZW9wbnNjZWd0am9oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzNjAxMzUsImV4cCI6MjA0NTkzNjEzNX0.n2FKKYLLO_IhtWtjsZfNSVic5mnuXmu5dCA9mbk1SfU"

supabase: Client = create_client(url, key)

response = supabase.table('History').select("*").order('id', desc=True).limit(5).execute().data

''' We're pulling the last 3 records to add to the broadcast message, cause only this much will probably be necessary '''

for _, val in enumerate(response):
	model_address = val.get('M_addr')
	system_boolean = val.get('SysBool')
	model_function = val.get('M_func')
	prompt = val.get('Prompt')
	print(model_address, system_boolean, model_function)