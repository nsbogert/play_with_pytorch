from openai import OpenAI
import os

# Ensure the OPENAI_API_KEY environment variable is set
if 'OPENAI_API_KEY' not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Create OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY']) 




'''    PROMPTS    '''
# Prompt 1 - System role
SP1 = "You are an expert data scientist that explains complex concepts in simple terms."
UP1 = "What is RAG in AI?"

# Prompt 2 - System with purpose, audience, tone
CB2_purpose = "You are an expert chatbot working for an e-commerce company specializing in electronics. Your purpose is to assist users with inquiries, order tracking, and troubleshooting common issues. "
CB2_audience = "Your audience are tech-savvy individuals interested in purchasing electronic gadgets. "
CB2_tone = "Use a professional and user-friendly tone when interacting with customers."

SP2 = CB2_purpose + CB2_audience + CB2_tone
UP2 = "My new headphones aren't connecting to my device."


'''  SELECT A PROMPT TO USE  '''
chosenSP = SP2
chosenUP = UP2

# Call the OpenAI API
def get_response(system_prompt, user_prompt):
  # Assign the role and content for each message
  messages = [{"role": "system", "content": system_prompt},
      		  {"role": "user", "content": user_prompt}]  
  response = client.chat.completions.create(
      model="gpt-4o-mini", messages = messages, temperature=0)
  
  return response.choices[0].message.content

# Try the function with a system and user prompts of your choice 
response = get_response(chosenSP, chosenUP)
print(response)

