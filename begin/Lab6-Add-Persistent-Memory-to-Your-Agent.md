# Lab 6: Add Persistent Memory to Your Agent

Welcome to Lab 6. In this lab, you will give your agent **long-term memory**. Until now, your agent forgot everything the moment a conversation ended. Here you will connect it to a **Microsoft Foundry Memory Store** so it can remember facts a user shared and use them in later conversations.

This lab builds on the earlier labs. You will keep working from the `begin` folder, and the end state of this lab is the file `begin/hostagent-memory.py`.

By the end of this lab, you will be able to:
- understand what a Foundry Memory Store is and why persistent memory is useful
- create a memory store from your agent code and connect to it with `FoundryMemoryProvider`
- save a fact to the store for a specific user
- ask the agent a question and watch it answer using a remembered fact
- run the agent locally

---

## Prerequisites

Before you begin, make sure you have the following. Most of these carry over from the earlier labs.

### Required
- VS Code
- Python 3.10 or newer
- uv
- Git
- Azure CLI
- Access to an Azure subscription and an Azure AI Foundry project
- An Azure AI Foundry service with a deployed `gpt-5.4-mini` model
- **A deployed `text-embedding-3-small` embedding model in your Foundry project** (used by the memory store)
- You have completed Lab 1 (or you understand the agent pattern in `begin/basic.py`)

> You do **not** need to create a memory store ahead of time. `hostagent-memory.py` creates it for you the first time you run it.

### Install links
- Visual Studio Code: https://code.visualstudio.com/download?_exp_download=d53503e735
- Python: https://www.python.org/downloads/
- Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Git: https://git-scm.com/downloads
- uv: https://docs.astral.sh/uv/

---

## Lab objective

In this lab, you will upgrade the agent so that it:
- creates a Foundry Memory Store (if one does not already exist)
- saves a fact about the user (their coffee preference)
- answers a later question using that remembered fact

Everything happens in a single file that you run yourself:
- `begin/hostagent-memory.py`

### What is a memory store?

A **memory store** gives an otherwise stateless agent persistent, semantic memory. Instead of only knowing what is in the current chat, the agent can recall facts a user shared in earlier sessions.

| | Without memory (Lab 1) | With memory (Lab 6) |
| --- | --- | --- |
| What the agent remembers | only the current chat | facts across conversations |
| Where facts live | in memory, lost on exit | in a Foundry Memory Store |
| How the agent uses it | nothing | `context_providers` |
| Example | "What is the capital of France?" | "What are my coffee preferences?" |

Memories are isolated per user by a **scope** value, so one person's facts never leak into another person's conversation.

---

## Folder structure

For this lab, keep working in the `begin` folder.

The file you will complete is:
- `begin/hostagent-memory.py`

---

## Step 1: Open the project and the starter file

> **Already did the earlier labs?** You already have the `agent-framework-helloworld` folder cloned. Just pull the latest changes to get the Lab 6 guide and starter file:
>
> ```bash
> git pull
> ```

1. Open VS Code and open the cloned `agent-framework-helloworld` folder (clone it first if you have not: `git clone https://github.com/liuhebian/agent-framework-helloworld.git`).
2. Navigate to the `begin` folder.
3. Open `begin/hostagent-memory.py`.

You will see a starter script with numbered `TODO` comments, similar to the earlier labs. Unlike the earlier labs, this script also **creates the memory store** it needs, so there is no separate provisioning step — you only ever run `hostagent-memory.py`.

---

## Step 2: Install the packages

The memory store uses `FoundryMemoryProvider`, which comes with the packages you already installed in the earlier labs. From the `begin` folder, activate your virtual environment first:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Then make sure the requirements are installed:

```bash
uv pip install -r requirements.txt
```

---

## Step 3: Update the environment file

Open the `.env` file in the `begin` folder (create one if it is missing) and make sure it has the values below. The memory-store values are new for this lab.

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME=<your-chat-model-deployment-name>
MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME=<your-embedding-model-deployment-name>
MEMORY_STORE_NAME=<your-memory-store-name>
```

Fictitious example (do not use these values for a real deployment):

```env
FOUNDRY_PROJECT_ENDPOINT=https://contoso-1234.services.ai.azure.com/api/projects/contoso-agent-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME=text-embedding-3-small
MEMORY_STORE_NAME=my-memory-store
```

Important:
- each person will have different values
- `MEMORY_STORE_NAME` is the name the script will create (or reuse) the store under

---

## Step 4: Review the starter code

Open `begin/hostagent-memory.py`.

The starter file already includes numbered `TODO` comments showing where each block of code goes. You will build the agent step by step: first the client, then the memory provider, then create the store, then the agent, then save a memory, and finally use it.

The file already includes:
- `load_dotenv()`
- imports for `Agent`, `FoundryChatClient`, `FoundryMemoryProvider`, `MemoryStoreDefaultDefinition`, and `ResourceNotFoundError`
- an async `AzureCliCredential` created with `async with`
- a `scope` value (`user_123`) that isolates memories per user
- the `async with client.project_client, memory_provider:` block that closes network sessions cleanly

The `TODO` comments mark the exact sections to complete:
1. `TODO 1` — the `FoundryChatClient` using environment variables
2. `TODO 2` — the `FoundryMemoryProvider`, connected to the store by name
3. `TODO 3` — create the memory store if it does not already exist
4. `TODO 4` — the `Agent`, with the memory provider attached via `context_providers`
5. `TODO 5` — save a memory to the store
6. `TODO 6` — ask the agent a question that relies on the saved memory

In the next steps you will copy the code for each `TODO` from this guide and paste it in place of the matching comment.

---

## Step 5: Create the Foundry client (`TODO 1`)

Find `TODO 1` and paste this in place of that comment to create the client from environment variables:

```python
        client = FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            credential=credential,
        )
```

Keep the indentation as shown — this code lives inside the `async with AzureCliCredential() as credential:` block.

---

## Step 6: Connect the memory provider (`TODO 2`)

This is the new part in Lab 6. Find `TODO 2` and paste this in place of that comment to connect to your memory store by name:

```python
        memory_provider = FoundryMemoryProvider(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            credential=credential,
            allow_preview=True,
            memory_store_name=os.environ["MEMORY_STORE_NAME"],
            scope=scope,
        )
```

Notes:
- `allow_preview=True` is required because the memory store API is still in preview.
- `memory_store_name` is the store the next step will create (or reuse).
- `scope` isolates memories to a single user.

---

## Step 7: Create the memory store (`TODO 3`)

This is what lets you run **only** `hostagent-memory.py` — the script creates the memory store it needs. Find `TODO 3` and paste this in place of that comment:

```python
            # Create the memory store on first run; reuse it on later runs.
            try:
                await memory_provider.project_client.beta.memory_stores.get(
                    os.environ["MEMORY_STORE_NAME"]
                )
            except ResourceNotFoundError:
                await memory_provider.project_client.beta.memory_stores.create(
                    name=os.environ["MEMORY_STORE_NAME"],
                    description="Memory store for the agent lab",
                    definition=MemoryStoreDefaultDefinition(
                        chat_model=os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"],
                        embedding_model=os.environ["MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME"],
                    ),
                )
                print(f"Created memory store: {os.environ['MEMORY_STORE_NAME']}")
```

The first time you run the script, the store does not exist, so `get` raises `ResourceNotFoundError` and the `create` call builds it. On later runs the store already exists, so nothing is recreated.

---

## Step 8: Create the agent with memory (`TODO 4`)

Find `TODO 4` and paste this in place of that comment. Notice that the memory provider is passed through `context_providers`:

```python
            agent = Agent(
                client=client,
                instructions=(
                    "You are a helpful assistant that remembers facts the user has shared "
                    "across conversations. Relevant memories from previous interactions are "
                    "automatically provided to you in the system context. Use them when "
                    "answering, and acknowledge when you are relying on remembered facts."
                ),
                context_providers=[memory_provider],
                # History is managed by the hosting infrastructure, so don't store it service-side.
                default_options={"store": False},
            )
```

The `context_providers=[memory_provider]` line lets the agent automatically pull in relevant memories when it answers.

---

## Step 9: Save a memory (`TODO 5`)

Find `TODO 5` and paste this in place of that comment to store a fact about the user:

```python
            update_poller = await memory_provider.project_client.beta.memory_stores.begin_update_memories(
                name=memory_provider.memory_store_name,
                scope=scope,
                items="I prefer dark roast coffee and usually drink it in the morning",
                update_delay=0,  # Trigger update immediately without waiting for inactivity
            )
            update_result = await update_poller.result()
            print(f"Updated with {len(update_result.memory_operations)} memory operations")
            for operation in update_result.memory_operations:
                print(
                    f"  - Operation: {operation.kind}, Memory ID: {operation.memory_item.memory_id}, Content: {operation.memory_item.content}"
                )
```

This writes a fact ("I prefer dark roast coffee...") into the store for the current `scope`. In a real app, memories are usually saved automatically from the conversation — here you save one explicitly so you can see it work.

> Tip: after you have run the script once and the memory is saved, you can comment out this block. The fact stays in the store, and later runs will still recall it.

---

## Step 10: Use the memory (`TODO 6`)

Find `TODO 6` and paste this in place of the `pass` line to ask the agent a question that relies on the saved fact:

```python
            result = await agent.run("What are my coffee preferences?")
            print(f"Agent: {result}")
```

Remove the `pass` line since the function now has real code.

---

## Step 11: Sign in to Azure

Before running the app, authenticate with Azure:

```bash
az login
```

This gives the app permission to access your Foundry project and memory store.

---

## Step 12: Run the agent

From the `begin` folder, run the agent:

```bash
python hostagent-memory.py
```

The first run creates the memory store, saves the fact, and answers the question. You should see output like this:

```text
Created memory store: my-memory-store
Updated with 1 memory operations
  - Operation: created, Memory ID: ..., Content: I prefer dark roast coffee and usually drink it in the morning
Agent: You prefer dark roast coffee, and you usually drink it in the morning.
```

If the agent answers using the fact you saved — even though you never mentioned coffee in your question — the memory store is working.

---

## Step 13: Prove the memory persists

To really see persistent memory in action:

1. Comment out the `TODO 4` block (the `begin_update_memories` code) so no new memory is saved.
2. Run the script again:

   ```bash
   python hostagent-memory.py
   ```

3. The agent should still answer "You prefer dark roast coffee..." because the fact was already stored in the Foundry Memory Store from your earlier run.

This is the difference from Lab 1: the fact survives between runs.

---

## Common issues and how to fix them

### 1. `MEMORY_STORE_NAME` is missing or wrong
Make sure `MEMORY_STORE_NAME` is set in `begin/.env`. The script creates the store under this name on the first run.

### 2. The memory store was not created
- confirm the `TODO 3` block is in place and ran without error
- confirm `MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME` and `MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME` in `.env` point to models deployed in your Foundry project

### 3. Authentication failed on the memory service
The memory service uses the **project's managed identity** to call the model, not your local login. If you see an authentication error, the project managed identity may be missing roles on the AI Services account (`Foundry User` and `Cognitive Services OpenAI User`). Ask your instructor or an Azure administrator to check the role assignments, and note that data-plane role changes can take 10–15 minutes to take effect.

### 4. The agent does not use the remembered fact
- confirm the `TODO 4` block ran at least once and printed a memory operation
- confirm the `scope` value is the same for saving and asking
- ask a question that clearly relates to the saved fact

### 5. "Unclosed client session / Unclosed connector" warnings
Make sure you kept the `async with AzureCliCredential() as credential:` and `async with client.project_client, memory_provider:` blocks from the starter file. These close the network sessions cleanly.

---

## What you built

You gave your agent **long-term memory**. Instead of forgetting everything at the end of a conversation, it now:
- connects to a Foundry Memory Store
- saves facts a user shared, isolated per user by scope
- recalls those facts in later conversations and uses them to answer

This is the foundation for agents that feel personalized and remember context over time.
