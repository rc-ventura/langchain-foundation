import asyncio
from pathlib import Path
from typing import Dict, Any
from pprint import pprint

# Langchain
from langchain_community.utilities import SQLDatabase
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.tools import tool
from langchain.agents import AgentState
from langchain.agents import create_agent
from langchain.tools import ToolRuntime
from langchain.messages import HumanMessage, ToolMessage
from langgraph.types import Command

from tavily import TavilyClient

from dotenv import load_dotenv

load_dotenv()


# MCP Client Kiwi
client = MultiServerMCPClient(
    {
        "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com"
            }
    }
)

async def build_travel_agent():
    """Create the travel agent with MCP tools (doc-style pattern)."""
    tools = await client.get_tools()
    return create_agent(
        model="gpt-5-nano",
        tools=tools,
        system_prompt="""
    You are a travel agent. Search for flights to the desired tourist destination.
    You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
    - Price (lowest, economy class)
    - Duration (shortest)
    - Date flexibility (consider best season for the destination)
    To make things easy, only look for one ticket per traveler, one way.
    You may need to make multiple searches to iteratively find the best options.
    You will be given no extra information, only the origin and destination. It is your job to think critically about the best options.
    Once you have found the best options, let the user know your shortlist of options.
    """
    )


# Tavily Client
tavily_client = TavilyClient()


# Sub-agents Tools

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)


db_path = Path(__file__).parent / "resources" / "destinations.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")


@tool
def query_destination_db(query: str) -> str:

    """Query the database for destination and attraction information"""

    try:
        return db.run(query)
    except Exception as e:
        return f"Error querying database: {e}"


# Coordinator tools

@tool
async def search_flights(runtime: ToolRuntime) -> str:
    """Travel agent searches for flights to the desired tourist destination."""
    origin = runtime.state["origin"]
    destination = runtime.state["destination"]
    travel_agent = await build_travel_agent()
    response = await travel_agent.ainvoke(
        {"messages": [HumanMessage(content=f"Find flights from {origin} to {destination}")]},
        config={"recursion_limit": 20}
    )
    return response['messages'][-1].content

@tool
def search_accommodations(runtime: ToolRuntime) -> str:
    """Accommodation agent finds the best hotels/accommodations for the given location and number of travelers."""
    destination = runtime.state["destination"]
    travelers = runtime.state["travelers_count"]
    query = f"Find hotels and accommodations in {destination} for {travelers} travelers"
    response = accommodation_agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 20}
    )
    return response['messages'][-1].content

@tool
def suggest_activities(runtime: ToolRuntime) -> str:
    """Activity agent suggests attractions and activities for the destination based on traveler preferences."""
    destination = runtime.state["destination"]
    preference = runtime.state["activity_preference"]
    query = f"Find {preference} activities and attractions in {destination}"
    response = activity_agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 20}
    )
    return response['messages'][-1].content

@tool
def update_state(origin: str, destination: str, travelers_count: str, activity_preference: str, runtime: ToolRuntime) -> str:
    """Update the state when you know all of the values: origin, destination, travelers_count, activity_preference"""
    return Command(update={
        "origin": origin, 
        "destination": destination, 
        "travelers_count": travelers_count, 
        "activity_preference": activity_preference, 
        "messages": [ToolMessage("Successfully updated state", tool_call_id=runtime.tool_call_id)]}
        )

# State

class TravelState(AgentState):
    origin: str
    destination: str
    travelers_count: str
    activity_preference: str

# Sub Agents


# Accommodation agent
accommodation_agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    system_prompt="""
    You are an accommodation specialist. Search for hotels and accommodations in the desired location for the number of travelers.
    You are not allowed to ask any more follow up questions, you must find the best accommodation options based on the following criteria:
    - Price (best value for money)
    - Location (central, near attractions)
    - Reviews (highest ratings)
    - Amenities (suitable for the number of travelers)
    Return the best options after you have found them.
    """
)


# Activity agent
activity_agent = create_agent(
    model="gpt-5-nano",
    tools=[query_destination_db, web_search],
    system_prompt="""
    You are an activity and attraction specialist. Help travelers discover the best things to do in their destination.
    First, query the destinations database to get information about the city (timezone, best season, popular activities).
    Then, query the attractions database to find specific attractions matching the traveler's preferences.
    Use web search to supplement with current information, events, and additional recommendations.
    Provide a curated list of activities with estimated duration and practical tips.
    If you run into errors when querying the database, try to fix them by making changes to the query.
    Return comprehensive activity suggestions after you have researched them.
    """
)


async def build_coordinator():
    """Create the coordinator agent (doc-style async setup)."""
    return create_agent(
        model="gpt-5-nano",
        tools=[search_flights, search_accommodations, update_state, suggest_activities],
        state_schema=TravelState,
        system_prompt="""
    You are a travel coordinator. Delegate tasks to your specialists for flights, accommodations, and activities.
    First find all the information you need to update the state: origin, destination, number of travelers, and activity preferences.
    Once that is done, delegate the tasks to your specialists.
    Once you have received their answers, coordinate the perfect trip itinerary for the travelers.
    Provide a comprehensive travel plan with flights, accommodations, and suggested activities.
    """
    )

# Main function for testing
async def main():
    """Main function to test the travel coordinator system"""
    # Test the coordinator
    coordinator = await build_coordinator()
    response = await coordinator.ainvoke(
        {
            "messages": [HumanMessage(content="I'm from São Paulo and I'd like to visit Tokyo for 2 travelers, interested in cultural activities")],
        }
    )
    
    pprint(response)
    print("\n" + "="*50)
    print("FINAL RESPONSE:")
    print(response["messages"][-1].content)
    return response

# For LangGraph Dev - this will be the entry point

coordinator = asyncio.run(build_coordinator())

def get_coordinator():
    """Entry point for LangGraph Dev"""
    return coordinator

# For standalone script testing
if __name__ == "__main__":
    asyncio.run(main())