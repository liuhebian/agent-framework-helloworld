import os

from agent_framework import Agent, tool, function_middleware, FunctionInvocationContext
from pydantic import Field
from agent_framework.foundry import FoundryChatClient, ResponsesHostServer, FoundryToolbox
from azure.identity import DefaultAzureCredential
from agent_framework.azure import AzureAISearchContextProvider
from typing import Annotated
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


def main():
    credential = DefaultAzureCredential()

    # TODO 1: Create the FoundryChatClient from the .env values.

    # TODO 2: Connect to the Foundry IQ toolbox by its name.

    # TODO 3: Create the Agent and give it the toolbox as a tool.
    
    # TODO 4: Start the host server.


if __name__ == "__main__":
    main()