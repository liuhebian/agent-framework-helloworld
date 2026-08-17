
import asyncio
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field


# TODO 4: Add the @tool function "get_customer" that returns customer names by region.


async def main() -> None:
    # TODO 1: Create the FoundryChatClient using your Azure AI Foundry project endpoint.

    # TODO 2: Create the Agent with a friendly name and instructions.

    # TODO 3: Run the agent once to test it, then later replace this with a chat loop.

    pass


if __name__ == "__main__":
    asyncio.run(main())