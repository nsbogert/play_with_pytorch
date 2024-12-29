from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
import math
import os

# Ensure the OPENAI_API_KEY environment variable is set
if 'OPENAI_API_KEY' not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Set up LLM 
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['OPENAI_API_KEY']
)

# Set up Tools
@tool
def rectangle_area(input: str) -> float:
    """Calculates the area of rectangle given lengths of sides a and b"""
    sides = input.split(',')
    a = float (sides[0].strip())
    b = float (sides[1].strip())
    return a*b

@tool
def hypotenuse_length(input: str) -> float:
    """Calculates the length of the hypotenuse of a right-angled triangle given the lengths of the other two sides."""
    sides = input.split(',')
    a = float(sides[0].strip())
    b = float(sides[1].strip())
    return math.sqrt(a**2 + b**2)

tools = [rectangle_area, hypotenuse_length]

# Function to invoke the agent with a query and message history
def invoke_agent(agent, query, message_history=[]):
    response = agent.invoke({"messages": message_history + [("human", query)]})
    return response["messages"]

# Create the ReAct agent
agent = create_react_agent(model, tools)

''' Queries to test the agent '''

## Submit first original query
query = "What is the area of a rectangle with sides 5 and 7?"
#query = "What is the length of a triangle with sides 5 and 7?"
message_history = invoke_agent(agent, query)

## Submit follow-up query
new_query = "What about one with sides 12 and 14?"
message_history = invoke_agent(agent, new_query, message_history)

## Submit Third query
new_query = "For that Triangle, what is its hypotenuse?"
message_history = invoke_agent(agent, new_query, message_history)

''' Share the results '''

# Extract the human and AI messages from the result
filtered_messages = [msg for msg in message_history if isinstance(msg, (HumanMessage, AIMessage)) and msg.content.strip()]

# Pass the new query as input and print the final outputs
print({"agent_output": [f"{msg.__class__.__name__}: {msg.content}" for msg in filtered_messages]})
