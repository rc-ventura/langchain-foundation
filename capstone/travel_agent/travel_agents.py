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
    You are a travel agent. Search for flights to the desired destination wedding location.
    You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
    - Price (lowest, economy class)
    - Duration (shortest)
    - Date (time of year which you believe is best for a wedding at this location)
    To make things easy, only look for one ticket, one way.
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


db_path = Path(__file__).parent / "resources" / "Chinook.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")


@tool
def query_playlist_db(query: str) -> str:

    """Query the database for playlist information"""

    try:
        return db.run(query)
    except Exception as e:
        return f"Error querying database: {e}"


# Coordinator tools

@tool
async def search_flights(runtime: ToolRuntime) -> str:
    """Travel agent searches for flights to the desired destination wedding location."""
    origin = runtime.state["origin"]
    destination = runtime.state["destination"]
    travel_agent = await build_travel_agent()
    response = await travel_agent.ainvoke(
        {"messages": [HumanMessage(content=f"Find flights from {origin} to {destination}")]},
        config={"recursion_limit": 20}
    )
    return response['messages'][-1].content

@tool
def search_venues(runtime: ToolRuntime) -> str:
    """Venue agent chooses the best venue for the given location and capacity."""
    destination = runtime.state["destination"]
    capacity = runtime.state["guest_count"]
    query = f"Find wedding venues in {destination} for {capacity} guests"
    response = venue_agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 20}
    )
    return response['messages'][-1].content

@tool
def suggest_playlist(runtime: ToolRuntime) -> str:
    """Playlist agent curates the perfect playlist for the given genre."""
    genre = runtime.state["genre"]
    query = f"Find {genre} tracks for wedding playlist"
    response = playlist_agent.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"recursion_limit": 20}
    )
    return response['messages'][-1].content

@tool
def update_state(origin: str, destination: str, guest_count: str, genre: str, runtime: ToolRuntime) -> str:
    """Update the state when you know all of the values: origin, destination, guest_count, genre"""
    return Command(update={
        "origin": origin, 
        "destination": destination, 
        "guest_count": guest_count, 
        "genre": genre, 
        "messages": [ToolMessage("Successfully updated state", tool_call_id=runtime.tool_call_id)]}
        )

# State

class WeddingState(AgentState):
    origin: str
    destination: str
    guest_count: str
    genre: str

# Sub Agents


# Venue agent
venue_agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    system_prompt="""
    You are a venue specialist. Search for venues in the desired location, and with the desired capacity.
    You are not allowed to ask any more follow up questions, you must find the best venue options based on the following criteria:
    - Price (lowest)
    - Capacity (exact match)
    - Reviews (highest)
    Return the best option after you have found it.
    """
)


# Playlist agent
playlist_agent = create_agent(
    model="gpt-5-nano",
    tools=[query_playlist_db],
    system_prompt="""
    You are a playlist specialist. Query the sql database and curate the perfect playlist for a wedding given a genre.
    Once you have your playlist, calculate the total duration and cost of the playlist, each song has an associated price.
    If you run into errors when querying the database, try to fix them by making changes to the query.
    Do not come back empty handed, keep trying to query the db until you find a list of songs.
    Return the best option after you have found it.
    """
)


async def build_coordinator():
    """Create the coordinator agent (doc-style async setup)."""
    return create_agent(
        model="gpt-5-nano",
        tools=[search_flights, search_venues, update_state, suggest_playlist],
        state_schema=WeddingState,
        system_prompt="""
    You are a wedding coordinator. Delegate tasks to your specialists for flights, venues and playlists.
    First find all the information you need to update the state. Once that is done you can delegate the tasks.
    Once you have received their answers, coordinate the perfect wedding for me.
    """
    )

# Main function for testing
async def main():
    """Main function to test the wedding coordinator system"""
    # Test the coordinator
    coordinator = await build_coordinator()
    response = await coordinator.ainvoke(
        {
            "messages": [HumanMessage(content="I'm from London and I'd like a wedding in Paris for 100 guests, jazz-genre")],
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