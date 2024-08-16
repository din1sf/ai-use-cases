from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "put-key-here" 
os.environ["OPENAI_BASE_URL"] = "https://ews-emea.api.bosch.com/knowledge/insight-and-analytics/llms/d/v1" 

llm = OpenAI(default_headers={"api-key": os.getenv("OPENAI_API_KEY")})

model = "meta-llama/Meta-Llama-3.1-8B-Instruct"  
messages = [{"role": "user", "content": "Hello! What is your name?"}]

response = llm.chat.completions.create(
       model=model,
       messages=messages
)

print(response.choices[0].message.content)