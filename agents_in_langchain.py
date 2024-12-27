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


tools = [rectangle_area]

agent = create_react_agent(model, tools)

query = "What is the area of a rectangle with sides 5 and 7?"

response = agent.invoke({"messages": [("human", query)]})

# print agent's response
print(response["messages"][-1].content)


