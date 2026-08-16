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


# TODO: Add the @tool function here.
# Purpose: return customer names by region.
# Example structure:
# @tool(approval_mode="never_require")
# def get_customer(
#     scope: Annotated[str, Field(description="Optional customer scope")] = "all",
# ) -> str:
#     customers = {
#         "all": ["Customer A", "Customer B", "Customer C", "Customer D", "Customer E", "Customer F"],
#         "region a": ["Customer A", "Customer B"],
#         "region b": ["Customer C", "Customer D"],
#         "region c": ["Customer E", "Customer F"],
#     }
#     selected = customers.get(scope.lower(), customers["all"])
#     return f"Customers for scope '{scope}' are: {', '.join(selected)}."


def main():
    # TODO: Create the FoundryChatClient from the .env values.
    # Example:
    # client = FoundryChatClient(
    #     project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    #     model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    #     credential=DefaultAzureCredential(),
    # )

    # TODO: Create the Agent, include the tool, and set default options.
    # Example:
    # agent = Agent(
    #     client=client,
    #     instructions="You are a friendly assistant. Keep your answers brief.",
    #     default_options={"store": False},
    #     tools=[get_customer],
    # )

    # TODO: Start the host server.
    # Example:
    # server = ResponsesHostServer(agent)
    # server.run()

    pass


if __name__ == "__main__":
    main()