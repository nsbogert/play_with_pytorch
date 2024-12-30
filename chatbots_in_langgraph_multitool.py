import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
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

@tool
def check_palindrome(text: str):
    """Check if the given text is a palindrome."""
    cleaned_text = ''.join(char.lower() for char in text if char.isalnum())

    if cleaned_text == cleaned_text[::-1]:
        return f"The phrase or word '{text}' is a palindrome."
    else: 
        return f"The phrase or word '{text}' is not a palindrome."

@tool
def check_date(date: str) -> str:
    """ Provides a list of important historical events that happened for a given date in any format """
    try: 
        answer = llm.invoke(f"List important historical events that occurred on {date}.")
        return answer.content
    except Exception as e:
        return f"Error rerieving events: {str(e)}"

@tool
def wikipedia_tool(text: str):
    """Check wikipedia for answers."""
    api_wrapper = WikipediaAPIWrapper(top_k_results=1)

# Setup Tools
tools = [wikipedia_tool, check_date, check_palindrome]
#tools = [check_date, check_palindrome]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

''' Dynamic Tool Caller '''
# Use MessagesState to define the state of the stopping function
def should_continue(state: MessagesState): 
    # Get the last message from the state
    last_message = state["messages"][-1]
    # Check - does the last message contain tool calls?
    if last_message.tool_calls:
        return "tools"
    # End conversation if no tool calls are present
    return END

# Extract the last messsage from history
def call_model(state: MessagesState):
    last_message = state["messages"][-1]

    # If the last message has tool calls, return the tool's response
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return {"messages": [AIMesssage(content=last_message.tool_calls[0]["response"])]}
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Define & initialize StateGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define Chatbot function
def chatbot(state: State): 
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

''' Set up Graph '''

# Set up Graph 
workflow = StateGraph(State)
workflow.add_node("chatbot", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", should_continue, ["tools", END])
workflow.add_edge("tools", "chatbot")

# Adding Memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Function to execute the chatbot based on user input
def stream_memory_responses(user_input: str):
    config = {"configurable": {"thread_id": "single_session_memory"}}
    for event in graph.stream({"messages": [("user", user_input)]}, config):
        for value in event.values():
            if "messages" in value and value["messages"]:
                print("Agent:", value["messages"]) 

# stream multiple tool outputs
config = {"configurable": {"thread_id": "1"}}

#create input message with user's query
def multi_tool_output(query):
    inputs = {"messages": [HumanMessage(content=query)]}
    print(f"User: {query}")
    # stream messages and medadata from the chatbot
    response = ""
    for msg, metadata in app.stream(inputs, config, stream_mode="messages"):
        # check if the message has content and is from AI
        if msg.content and not isinstance(msg, HumanMessage) and msg.name is not None:
            response += msg.content
    print(f"Agent: {response}")
    print ("\n")

def user_agent_multiturn(queries):
    for query in queries:
        multi_tool_output(query)


''' Test the chatbot'''
#multi_tool_output("Is 'Stella won no wallets' a palindrome?")
#multi_tool_output("What happened on April 12th, 1955?")

queries = ["What happened on July 16, 1969?", "What about October 24, 1929?", "Is 'Stella won no wallets' a palindrome?", "what about 'palladium stadium'?"]
user_agent_multiturn(queries)