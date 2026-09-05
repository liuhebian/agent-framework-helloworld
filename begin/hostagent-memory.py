# Copyright (c) Microsoft. All rights reserved.

"""Foundry Memory hosted agent sample.

This agent uses :class:`FoundryMemoryProvider` to give an otherwise stateless
hosted agent persistent, semantic memory backed by a Microsoft Foundry
Memory Store. Running this script creates the memory store (if it does not
already exist) and then uses it. The store name comes from the
``MEMORY_STORE_NAME`` environment variable.

"""

import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient, FoundryMemoryProvider
from azure.ai.projects.models import MemoryStoreDefaultDefinition
from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    # Own the credential via ``async with`` so its aiohttp session is closed on exit,
    # avoiding "Unclosed client session / Unclosed connector" warnings. The memory
    # store APIs used by FoundryMemoryProvider are async, so use an async credential.
    # Scope isolates memories per user id.
    scope = "user_123"

    async with AzureCliCredential() as credential:
        # TODO 1: Create the FoundryChatClient using your Azure AI Foundry project endpoint.

        # TODO 2: Create the FoundryMemoryProvider connected to your memory store by name.

        # Enter the internal AIProjectClients so their aiohttp sessions are closed on
        # exit, avoiding "Unclosed client session / Unclosed connector" warnings.
        async with client.project_client, memory_provider:
            # TODO 3: Create the memory store if it does not already exist.

            # TODO 4: Create the Agent and attach the memory provider via context_providers.

            # TODO 5: Save a memory to the store.

            # TODO 6: Ask the agent a question that relies on the saved memory.
            pass


if __name__ == "__main__":
    asyncio.run(main())