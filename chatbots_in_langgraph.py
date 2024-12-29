import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langgraph.checkpoint.memory import MemorySaver

''' Script '''
# Ensure the OPENAI_API_KEY environment variable is set
if 'OPENAI_API_KEY' not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Set up LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['OPENAI_API_KEY']
)

# Initialize Wikipedia & create Wikipedia query tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
tools = [wikipedia_tool]
tool_node = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)

# Define & initialize StateGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define Chatbot function
def chatbot(state: State): 
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Set up Graph 
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)

graph_builder.add_edge("tools","chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Adding Memory
memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)

# Function to execute the chatbot based on user input
def stream_memory_responses(user_input: str):
    config = {"configurable": {"thread_id": "single_session_memory"}}
    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            if "messages" in value and value["messages"]:
                print("Agent:", value["messages"]) 

''' Test the chatbot'''
stream_memory_responses("What is Star Wars?")
stream_memory_responses("Who created it?")
stream_memory_responses("Did he create the first light saber?")

'''
# Produce Chatbot Graph
display(Image(graph.get_graph().draw_mermaid_png()))

# Define a function to execute the chatbot, streaming each message
def stream_tool_responses(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Agent:", value["messages"])

# Define the query and run the chatbot
user_query = "House of Lords"
stream_tool_responses(user_query)

'''


