
import asyncio
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field


# TODO: Add the @tool function here.
# Purpose: return customer names by region.
# Example structure:
# @tool(approval_mode="never_require")
# def get_customer(
#     scope: Annotated[str, Field(description="Optional customer scope, for example all, Region A, Region B, Region C")] = "all",
# ) -> str:
#     """Get my customer list."""
#     customers = {
#         "all": ["Customer A", "Customer B", "Customer C", "Customer D", "Customer E", "Customer F"],
#         "region a": ["Customer A", "Customer B"],
#         "region b": ["Customer C", "Customer D"],
#         "region c": ["Customer E", "Customer F"],
#     }
#     selected = customers.get(scope.lower(), customers["all"])
#     return f"Customers for scope '{scope}' are: {', '.join(selected)}."


async def main() -> None:
    # TODO: Create the FoundryChatClient using your Azure AI Foundry project endpoint.
    # Example:
    # client = FoundryChatClient(
    #     project_endpoint="https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>",
    #     model="gpt-5.4-mini",
    #     credential=AzureCliCredential(),
    # )

    # TODO: Create the Agent with a friendly name and instructions.
    # Example:
    # agent = Agent(
    #     client=client,
    #     name="HelloAgent",
    #     instructions="You are a friendly assistant. Keep your answers brief.",
    #     tools=[get_customer],
    # )

    # TODO: Create a session and start the chat loop.
    # Example:
    # session = agent.create_session()
    # print("Chat started. Type 'exit' or 'bye' to quit.\n")
    # while True:
    #     user_input = input("You: ").strip()
    #     if user_input.lower() in ["exit", "bye"]:
    #         print("Agent: Goodbye!")
    #         break
    #     result = await agent.run(user_input, session=session)
    #     print(f"Agent: {result}\n")

    pass


if __name__ == "__main__":
    asyncio.run(main())