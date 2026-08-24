# Lab 3: Connect Your Agent to a Foundry IQ Knowledge Base

Welcome to Lab 3. In this lab, you will extend the host agent from Lab 2 so it can answer questions using your **own documents** through an **Azure AI Foundry IQ knowledge base** backed by **Azure AI Search**.

This lab builds directly on Lab 2. You will keep working from the `begin` folder, and the end state of this lab is the file `begin/hostagent-iq.py`.

By the end of this lab, you will be able to:
- understand what a Foundry IQ knowledge base is and why it is useful
- create an Azure AI Search service and deploy a `text-embedding-3-small` embedding model
- install the new `agent-framework-azure-ai-search` package
- add the Azure AI Search knowledge base to your agent as a context provider
- run the agent locally and ask questions grounded in your own data

---

## Prerequisites

Before you begin, make sure you have the following. Most of these carry over from Lab 1 and Lab 2.

### Required
- VS Code
- Python 3.10 or newer
- uv
- Git
- Azure CLI
- Azure Developer CLI (`azd`)
- Access to an Azure subscription and an Azure AI Foundry project
- An Azure AI Foundry service with a deployed `gpt-5.4-mini` model
- **An Azure AI Search service** (you will create this in Step 2)
- **A deployed `text-embedding-3-small` embedding model in your Foundry project** (you will deploy this in Step 2)
- You have completed Lab 2 (or you understand the host agent pattern in `begin/hostagent.py`)

### Install links
- Visual Studio Code: https://code.visualstudio.com/download?_exp_download=d53503e735
- Python: https://www.python.org/downloads/
- Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Azure Developer CLI (azd): https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows
- Git: https://git-scm.com/downloads
- uv: https://docs.astral.sh/uv/

---

## Lab objective

In this lab, you will upgrade the agent from Lab 2 so that it:
- connects to an Azure AI Search knowledge base (a Foundry IQ knowledge base)
- retrieves relevant passages from your own documents at query time
- answers questions grounded in that content and cites its sources

The starter and end-state file is:
- `begin/hostagent-iq.py`

The goal is to see how little code it takes to move from a general assistant to one that answers from your own data.

---

## Folder structure

For this lab, keep working in the `begin` folder.

The file you will complete is:
- `begin/hostagent-iq.py`

---

## Step 1: Open the project and the starter file

> **Already did Lab 1 and Lab 2?** You already have the `agent-framework-helloworld` folder cloned. Just pull the latest changes to get the Lab 3 and Lab 4 guides and starter files:
>
> ```bash
> git pull
> ```

1. Open VS Code and open the cloned `agent-framework-helloworld` folder (clone it first if you have not: `git clone https://github.com/liuhebian/agent-framework-helloworld.git`).
2. Navigate to the `begin` folder.
3. Open `begin/hostagent-iq.py`.

You will see a starter script with numbered `TODO` comments, similar to the host agent in Lab 2, plus one new piece: an Azure AI Search context provider.

---

## Step 2: Create the Azure AI Search service and deploy the embedding model

This lab depends on two resources that you will set up in your Azure AI Foundry project before writing any code:

1. **An Azure AI Search service** — this stores and indexes your documents so the agent can retrieve them. Creating a knowledge base provisions this service for you.
2. **A `text-embedding-3-small` embedding model** — this turns your documents and questions into vectors so the search service can find the most relevant passages.

### 2a. Create the knowledge base (this creates the Azure AI Search service)

1. Open your **Azure AI Foundry project** in the portal.
2. In the left navigation, go to **Knowledge base**.
3. Select **Create knowledge base** and follow the prompts.
4. This step also **creates an Azure AI Search service** for you (or lets you connect an existing one) to store and index your documents.
5. Add a **knowledge source**: upload the file `data/contoso-outdoors-search-documents.json` from this repository so its documents are indexed into the knowledge base.

### 2b. Deploy the embedding model

1. In your Foundry project, go to **Models** (model catalog / deployments).
2. Search for and deploy the **`text-embedding-3-small`** base model.
3. The knowledge base uses this embedding model to convert your documents and questions into vectors.

> _<!-- ADD MORE DETAIL HERE IF NEEDED -->_
> _You can add screenshots or extra detail for creating the knowledge base and deploying the embedding model here._

When you finish this step, you should have:
- an Azure AI Search **endpoint**, for example `https://<your-search-service>.search.windows.net`
- a **knowledge base name** for your Foundry IQ knowledge base
- a deployed `text-embedding-3-small` model in your Foundry project

Keep these values handy — you will put the endpoint and knowledge base name in the `.env` file in the next step.

---

## Step 3: Install the new package

Lab 3 needs one additional package that was not used in Labs 1 and 2: `agent-framework-azure-ai-search`. It provides the `AzureAISearchContextProvider` that connects your agent to the knowledge base.

It is already listed in `begin/requirements.txt`:

```text
agent-framework-azure-ai-search
```

From the `begin` folder, with your virtual environment activated, install the requirements again to pick it up:

```bash
uv pip install -r requirements.txt
```

If your environment is not activated yet, activate it first:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

---

## Step 4: Update the environment file

Open the `.env` file in the `begin` folder (create one if it is missing) and make sure it has all the values below. The first two are the same as Lab 2; the last two are new for this lab.

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_KNOWLEDGE_BASE_NAME=<your-foundry-iq-knowledge-base-name>
```

Fictitious example (do not use these values for a real deployment):

```env
FOUNDRY_PROJECT_ENDPOINT=https://contoso-1234.services.ai.azure.com/api/projects/contoso-agent-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
AZURE_SEARCH_ENDPOINT=https://contoso-search.search.windows.net
AZURE_SEARCH_KNOWLEDGE_BASE_NAME=contoso-outdoors-kb
```

Important:
- each person will have different values
- do not share or copy someone else's values

---

## Step 5: Review the starter code

Open `begin/hostagent-iq.py`.

The starter file already includes numbered `TODO` comments showing where each block of code goes. You will build the agent step by step: first the client, then the knowledge base provider, then the agent, and finally the host server.

The file already includes:
- `load_dotenv(override=True)`
- imports for `Agent`, `FoundryChatClient`, `ResponsesHostServer`, and `AzureAISearchContextProvider`
- `DefaultAzureCredential` setup

The `TODO` comments mark the exact sections to complete:
1. `TODO 1` — the `FoundryChatClient` using environment variables
2. `TODO 2` — the `AzureAISearchContextProvider` (the knowledge base connection)
3. `TODO 3` — the `Agent`, with the knowledge base attached via `context_providers`
4. `TODO 4` — the `ResponsesHostServer` initialization and run call

In the next steps you will copy the code for each `TODO` from this guide and paste it in place of the matching comment.

---

## Step 6: Complete the Foundry client setup (`TODO 1`)

Find `TODO 1` and paste this in place of that comment to create the client from environment variables:

```python
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=credential
    )
```

This uses the values from your `.env` file and the Azure identity available on your machine.

---

## Step 7: Connect the knowledge base (`TODO 2`)

This is the new part in Lab 3. Find `TODO 2` and paste this in place of that comment to create the Azure AI Search context provider:

```python
    search_provider = AzureAISearchContextProvider(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        knowledge_base_name=os.environ["AZURE_SEARCH_KNOWLEDGE_BASE_NAME"],
        credential=credential,
        mode="agentic",
    )
```

What this does:
- `endpoint` points to your Azure AI Search service
- `knowledge_base_name` is the Foundry IQ knowledge base you created in Step 2
- `mode="agentic"` lets the model decide when and how to query the knowledge base as it reasons about the question

---

## Step 8: Create the agent with the knowledge base (`TODO 3`)

Find `TODO 3` and paste this in place of that comment. Notice that instead of `tools=[...]`, you pass the knowledge base through `context_providers`:

```python
    agent = Agent(
        client=client,
        instructions=(
            "You are a friendly assistant. Keep your answers brief. "
            "When you use information returned by the knowledge base, cite your "
            "sources: end the answer with a 'Sources:' list of markdown links using each "
            "document's title and URL. Only cite sources you actually used."
        ),
        default_options={"store": False},
        context_providers=[search_provider]
    )
```

The `context_providers` list is how the agent pulls in relevant passages from your documents before it answers.

---

## Step 9: Start the host server (`TODO 4`)

Find `TODO 4` and paste this in place of that comment to start the server:

```python
    server = ResponsesHostServer(agent)
    server.run()
```

Remove the `pass` line at the end of `main()` since the function now has real code. This hosts the agent so it can be started locally for testing and, later, deployed to Azure AI Foundry.

---

## Step 10: Sign in to Azure

Before running the app, authenticate with Azure:

```bash
az login
```

This gives the app permission to access your Foundry project and your Azure AI Search service.

---

## Step 11: Run the agent locally

From the `begin` folder, start the agent:

```bash
python hostagent-iq.py
```

If you want to use the `azd` command instead, you can also test it with:

```bash
azd ai agent run --start-command "python hostagent-iq.py"
```

If the app starts successfully, you should see the local agent running and ready to accept requests.

---

## Step 12: Test the agent against your knowledge base

Open the local endpoint provided by your toolchain and ask a question that can only be answered from your documents, for example:

```text
How long will it take to receive my refund?
```

The agent should:
- query the knowledge base
- ground its answer in the retrieved passages
- end its reply with a `Sources:` list of the documents it used

If the answer is grounded in your content and includes sources, the knowledge base connection is working.

---

## Step 13: (Optional) Deploy remotely with azd

Once the app works locally, you can deploy it the same way as Lab 2. Make sure the four `.env` values (including the two new search values) are configured in your Azure environment, then run:

```bash
azd deploy
```

After deployment, test the remote endpoint and verify that the agent still answers from your knowledge base.

---

## Common issues and how to fix them

### 1. `AZURE_SEARCH_ENDPOINT` or `AZURE_SEARCH_KNOWLEDGE_BASE_NAME` is missing
Make sure both new values are present in the `begin/.env` file and match the resource you created in Step 2.

### 2. `ModuleNotFoundError: agent_framework.azure`
The `agent-framework-azure-ai-search` package is not installed. Re-run:

```bash
uv pip install -r requirements.txt
```

### 3. The agent answers but never cites sources
- confirm the knowledge base name is correct
- confirm your documents were indexed into the knowledge base
- confirm the `text-embedding-3-small` model is deployed and active

### 4. Permission or authentication errors
- confirm you ran `az login` with the correct account
- confirm your account has access to both the Foundry project and the Azure AI Search service

---

## What you built

You extended the Lab 2 host agent into a **retrieval-augmented agent**. Instead of answering only from what the model already knows, it now:
- retrieves relevant passages from your own documents through a Foundry IQ knowledge base
- answers grounded in that content
- cites the sources it used

In Lab 4, you will connect the agent to a **Foundry IQ toolbox** so it can call external tools, such as the Microsoft Learn documentation tools, over MCP.
