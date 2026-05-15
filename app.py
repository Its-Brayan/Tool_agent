from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage,SystemMessage, ToolMessage
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGroq(
    model='llama-3.1-8b-instant',
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

#The State class defines what your agent remembers
class State(TypedDict):
    messages:Annotated[list,add_messages]

#get_tools() returns the tools your agent can use
def get_tools():
    return[
        TavilySearch(max_result =3, search_depth="advanced")
    ]

#The LLM node - where your agent thinks and decides
def llm_node(state:State):
      """Your agent's brain - decides whether to use tools or respond."""
      tools = get_tools()
      llm_with_tools = llm.bind_tools(tools) #bind_tools() informs the LLM about available tools, allowing it to decide whether to call a tool or respond directly.
      response = llm_with_tools.invoke(state['messages'])
      return{"messages":[response]}

def tool_node(state:State):
       """Your agent's hands - executes the chosen tools."""
       tools = get_tools()
       tools_registry = {tool.name:tool for tool in tools}
       last_message = state["messages"][-1]
       tool_messages = []

       # Execute each tool the agent requested
       for tool_call in last_message.tool_calls:
            tool = tools_registry[tool_call['name']]
            result = tool.invoke(tool_call['args'])

             # Send the result back to the agent

            tool_messages.append(ToolMessage(
                  content = str(result),
                  tool_call_id = tool_call['id']
             ))
            
       return{"messages":tool_messages}

# Decision function - should we use tools or finish?
def should_continue(state:State):
       """Decides whether to use tools or provide final answer."""
       last_message = state['messages'][-1]

       if hasattr(last_message,"tool_calls") and last_message.tool_calls:
             return "tools" #Agent wants to use tools
       return END #Agent is ready to respond

def create_agent():
      graph = StateGraph(State)

      #add the nodes
      graph.add_node("llm",llm_node)
      graph.add_node("tools",tool_node)

      #set the entry point
      graph.set_entry_point('llm')
    
        # Add the flow logic
      graph.add_conditional_edges('llm',should_continue,
                                  {'tools':'tools',
                                   END: END})
      graph.add_edge('tools','llm')
      return graph.compile()

agent = create_agent()

#test it out!
initial_state = {
      "messages" : [
            SystemMessage(content="You are a helpful assistant with access to web search. Use the search tool when you need current information."),
            HumanMessage(content="When did Raila Odinga die?")
      ]
}

result = agent.invoke(initial_state)
print(result['messages'][-1].content)

     