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

# Prompt 2 - System role - Note: Specify personality and expertise
SP2 = "Act as a seasoned technology journalist covering the latest trends in the tech industry. You're known for your thorough research and insightful analysis, with an optimistic outlook on the future of technology."
UP2 = "What is the impact of AI on the technical Product Manager Job market?"

# Prompt 3 - System with purpose, audience, tone
CB3_purpose = "You are an expert chatbot working for an e-commerce company specializing in electronics. Your purpose is to assist users with inquiries, order tracking, and troubleshooting common issues. "
CB3_audience = "Your audience are tech-savvy individuals interested in purchasing electronic gadgets. "
CB3_tone = "Use a professional and user-friendly tone when interacting with customers."

SP3 = CB2_purpose + CB2_audience + CB2_tone
UP3 = "My new headphones aren't connecting to my device."

# Prompt 4 - More practice adding extra instruction
SP4_base_prompt = "Act as a learning advisor who receives queries from users mentioning their background, experience, and goals, and accordingly provides a response that recommends a tailored learning path of textbooks, including both beginner-level and more advanced options."
SP4_behavior_guidelines = "You should ask the user about their background, experience, and goals, whenever any of these is not provided in their query."
SP4_response_guidelines = "Recommend no more than three textbooks to any given query."

SP4_system_prompt = UP4_base_prompt + UP4_behavior_guidelines + UP4_response_guidelines
up4 = "Hello there! I'm a beginner with a marketing background, and I'm really interested in learning about Python, data analytics, and machine learning. Can you recommend some books?"


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

