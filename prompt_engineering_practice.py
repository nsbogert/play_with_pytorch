from openai import OpenAI
import os

# Ensure the OPENAI_API_KEY environment variable is set
if 'OPENAI_API_KEY' not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Create OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY']) 




'''    PROMPTS    '''
# Define the conversation messages

# Prompt 1: ROLES. A conversation between a user and a helpful event management assistant
# Note - need to insert directly as "messages" in the API call
role_prompt = [
    {"role": "user", "content": "You are a helpful event management assistant."},
    {"role": "user", "content": "What are some good conversation starters at networking events?"},
    {"role": "user", "content": ""}
]

# Prompt 2: Complete a story
p2_story = "In a distant galaxy, there was a brave space explorer named Alex. Alex had spent years traveling through the cosmos, discovering new planets and meeting alien species. One fateful day, while exploring an uncharted asteroid belt, Alex stumbled upon a peculiar object that would change the course of their interstellar journey forever..."
story_prompt = f"""Write the next 2 paragraphs continuing the story that was started in the text delimited by triple backticks, maintaining the writing style exemplified in the given paragraph ```{p2_story}```"""

# Prompt 3: Generating Tables
table_prompt = """Generate a table of 10 books, with columns for Title, Author, and Year, that you should read given that you are a science fiction lover. """

# Prompt 4: Customizing Output Format & Conditional Prompts
p4_instructions = """Infer the language and number of sentences in the pre-loaded text excerpt that will be provided using triple backticks (```) delimiters. If the text contains more than one sentence, generate a suitable title for it. Otherwise, return "N/A" for the title."""
p4_output_format = """Include the text, language, Number of Sentences, and title, each on a separate line, using 'Text:', 'Language:', 'Number of Sentences:', and 'Title:' as prefixes for each line."""
p4_text = "The sun was setting behind the mountains, casting a warm golden glow across the landscape."
p4_prompt = prompt = p4_instructions + p4_output_format + f"```{p4_text}```"

# Prompt 5: Single-Shot Prompt
singleShot_prompt = """Extract the odd numbers from the list: 
Input: {1, 3, 7, 12, 19, Output: {1,3,7,19}
Input: {3, 5, 11, 12, 16},"""

# Prompt 6: Sentiment Analysis & Classification w/ Few Shot Prompts
# Note - need to insert directly as "messages" in the API call
sentiment_messages = [{"role": "user", "content": "The product quality exceeded my expectations"},
              {"role": "assistant", "content": "1"},
              {"role": "user", "content": "I had a terrible experience with this product's customer service"},
              {"role": "assistant", "content": "-1"},
              # Provide the text for the model to classify
              {"role": "user", "content": "The price of the product is really fair given its features"}
             ]

# Prompt 7: Multi-step prompt to plan a trip
multistep_prompt = """Make a plan for a beach vacation, which should include: four potential locations, each with some accommodation options, some activities, and an evaluation of the pros and cons."""

# Prompt 8: Analyze solution correctness
p8_code = '''
def calculate_rectangle_area(length, width):
    area = length * width
    return area
'''
analyze_prompt = f"""Review the code function provided in three back-ticks and 1) Evaluate it for correct syntax 2) Check that it recieves 2 inputs and 3) Check that it returns one output: ```{p8_code}```"""

# Prompt 9: Chain-of-Thought
chain_of_thought_prompt = "Calculate the age of my friend's father in 10 years, given that he is currently twice my friend's age, and my friend is 20? Show your thinking step by step"

# Prompt 10: One-Shot Chain of Thought
p10_example = """Q: Sum the even numbers in the following set: {9, 10, 13, 4, 2}.
             A: Even numbers: {10, 4, 2}. Adding them: 10+4+2=16"""
p10_question = """Q: Sum the even numbers in the following set: {15, 13, 82, 7, 14} 
              A:"""
p10_prompt = p10_example + p10_question

# Prompt 11: Self-Consistency
p11_self_consistency_instruction = "Imagine three completely independent expert store inventory managers are answering this question. The final answer is obtained by majority vote. Show the work and final answer from each expert, then give the final decision from the majority vote."
p11_problem_to_solve = "If you own a store that sells laptops and mobile phones. You start your day with 50 devices in the store, out of which 60 percent are mobile phones. Throughout the day, three clients visited the store, each of them bought one mobile phone, and one of them bought additionally a laptop. Also, you added to your collection 10 laptops and 5 mobile phones. How many laptops and mobile phones do you have by the end of the day?"
self_consistent_prompt = p11_self_consistency_instruction + p11_problem_to_solve




'''  SELECT A PROMPT TO USE  '''

prompt = self_consistent_prompt

# Call the OpenAI API
def get_response(prompt):
  # Create a request to the chat completions endpoint
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}], 
    temperature = 0)
  return response.choices[0].message.content

# Print the response
print(get_response(prompt))

