import asyncio
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Callable


from langchain.agents import AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.agents.middleware import dynamic_prompt
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from pprint import pprint


load_dotenv()


@dataclass
class EmailContext:
    email_address: str = "julie@example.com"
    password: str = "password123"


class AuthenticatedState(AgentState):
    authenticated: bool


@tool
def check_inbox() -> str:
    """Check the inbox for recent emails"""
    return """
    Hi Julie, 
    I'm going to be in town next week and was wondering if we could grab a coffee?
    - best, Jane (jane@example.com)
    """

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an response email"""
    return f"Email sent to {to} with subject {subject} and body {body}"

@tool
def authenticate(runtime: ToolRuntime) -> Command:
    """Authenticate the user with the given email and password"""
    if runtime.context.email_address and runtime.context.password:
        return Command(update={
            "authenticated": True, 
            "messages": [ToolMessage(
                "Successfully authenticated", 
                tool_call_id=runtime.tool_call_id)]
        })
    else:
        return Command(update={
            "authenticated": False,
            "messages": [ToolMessage(
                "Authentication failed", 
                tool_call_id=runtime.tool_call_id)]
        })


@wrap_model_call
async def dynamic_tool_call(request: ModelRequest, 
handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:

    """Allow read inbox and send email tools only if user provides correct email and password"""

    authenticated = request.state.get("authenticated")
    
    if authenticated:
        tools = [check_inbox, send_email]
    else:
        tools = [authenticate]

    request = request.override(tools=tools) 
    return await handler(request)


authenticated_prompt = "You are a helpful assistant that can check the inbox and send emails."
unauthenticated_prompt = "You are a helpful assistant that can authenticate users. " \
    "You must call the authenticate tool first before accessing inbox or sending emails. " \
    "The authenticate tool will use the available EmailContext credentials automatically. " \
    "Do not ask the user for credentials - just call the authenticate tool directly."

@dynamic_prompt
def dynamic_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on authentication status"""
    authenticated = request.state.get("authenticated")

    if authenticated:
        return authenticated_prompt
    else:
        return unauthenticated_prompt


agent = create_agent(
    "gpt-5-nano",
    tools=[authenticate, check_inbox, send_email],
    checkpointer=InMemorySaver(),
    state_schema=AuthenticatedState,
    context_schema=EmailContext,
    middleware=[
        dynamic_tool_call, 
        dynamic_prompt,
        HumanInTheLoopMiddleware(
            interrupt_on={
                "authenticate": False,
                "check_inbox": False,
                "send_email": True,
            })
        ]
    )


async def main():
    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
    {"messages": [HumanMessage(content="you must check my email box and reply to the last email received.")]},
    context=EmailContext(),
    config=config
)

    print(response['messages'][-1].content)


    if "__interrupt__" in response:
        print(response["__interrupt__"][0].value["action_requests"][0]["args"]["body"])
        
        response = await agent.ainvoke(
            Command( 
                resume={"decisions": [{"type": "approve"}]}  # or "reject"
            ), 
            config=config # Same thread ID to resume the paused conversation
        )

        print(response["messages"][-1].content)
        pprint(response)
    else:
        print("No interrupt triggered.")


# LangGraph Dev entrypoint uses the exported agent directly
def get_agent():
    return agent


if __name__ == "__main__":
   asyncio.run(main())