from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

load_dotenv()

tavily_client = TavilyClient()

@tool 
def web_search(query:str) -> Dict[str, Any]:
    """
    Search the web for the given query.
    
    Args:
        query: The query to search for
        
    Returns:
        The search results
    """
    return tavily_client.search(query)

system_prompt = """
You are a personal dietitian. The user will request a subsitute for a recipe ingredient.
Use the web search tool to find a suitable substitute with the same nutritional value and return the result.
"""

agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    system_prompt=system_prompt,
    #checkpointer=InMemorySaver()
)


# config = {"configurable": {"thread_id": "1"}}

# response = agent.invoke(
#     {"messages": [HumanMessage(content="I want to substitute the rice in my diet. What can I use?")]},
#     config
# )

# print(response['messages'][-1].content)

# pprint(response)
