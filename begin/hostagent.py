import os
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient, ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from pydantic import Field

# Load environment variables from .env file
# Example values in .env:
# FOUNDRY_PROJECT_ENDPOINT=https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>
# AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
load_dotenv()


# TODO 4: Add the @tool function "get_customer" that returns customer names by region.


def main():
    # TODO 1: Create the FoundryChatClient from the .env values.

    # TODO 2: Create the Agent with instructions and default options.

    # TODO 3: Start the host server.

    pass


if __name__ == "__main__":
    main()