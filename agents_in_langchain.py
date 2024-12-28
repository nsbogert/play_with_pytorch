from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import math
import os

# LLM Setup
model = ChatOpenAI(
    #model="gpt-4o",
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['OPENAI_API_KEY']
)

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
    
    # Split the input string to get the lengths of the triangle
    sides = input.split(',')
    
    # Convert the input values to floats, removing extra spaces
    a = float(sides[0].strip())
    b = float(sides[1].strip())
    
    # Square each of the values, add them together, and find the square root 
    return math.sqrt(a**2 + b**2)


tools = [rectangle_area, hypotenuse_length]

agent = create_react_agent(model, tools)

query = "What is the area of a rectangle with sides 5 and 7?"
#query = "What is the length of a triangle with sides 5 and 7?"

response = agent.invoke({"messages": [("human", query)]})

# print agent's response
print(response["messages"][-1].content)


