# Lab 4: Connect Your Agent to a Foundry IQ Toolbox

Welcome to Lab 4. In this lab, you will extend the host agent so it can call **external tools** through an **Azure AI Foundry IQ toolbox**. You will connect a Microsoft Learn tool over **MCP (Model Context Protocol)** so the agent can look up up-to-date documentation and cite it.

This lab builds on Labs 2 and 3. You will keep working from the `begin` folder, and the end state of this lab is the file `begin/hostagent-toolbox.py`.

By the end of this lab, you will be able to:
- understand what a Foundry IQ toolbox is and how it differs from a knowledge base
- create a toolbox in your Foundry project and add the Microsoft Learn MCP tool
- connect the toolbox to your agent with `FoundryToolbox`
- add lightweight logging to watch the agent call tools
- run the agent locally and ask questions answered by the Microsoft Learn tools

---

## Prerequisites

Before you begin, make sure you have the following. Most of these carry over from the earlier labs.

### Required
- VS Code
- Python 3.10 or newer
- uv
- Git
- Azure CLI
- Azure Developer CLI (`azd`)
- Access to an Azure subscription and an Azure AI Foundry project
- An Azure AI Foundry service with a deployed `gpt-5.4-mini` model
- **A Foundry IQ toolbox with the Microsoft Learn MCP tool** (you will create this in Step 2)
- You have completed Lab 2 (and ideally Lab 3)

### Install links
- Visual Studio Code: https://code.visualstudio.com/download?_exp_download=d53503e735
- Python: https://www.python.org/downloads/
- Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Azure Developer CLI (azd): https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows
- Git: https://git-scm.com/downloads
- uv: https://docs.astral.sh/uv/

---

## Lab objective

In this lab, you will upgrade the host agent so that it:
- connects to a Foundry IQ toolbox
- calls the Microsoft Learn tools (exposed over MCP) when it needs documentation
- answers grounded in those results and cites its sources
- logs each tool call so you can see what the agent is doing

The starter and end-state file is:
- `begin/hostagent-toolbox.py`

### Knowledge base vs toolbox

| | Foundry IQ knowledge base (Lab 3) | Foundry IQ toolbox (Lab 4) |
| --- | --- | --- |
| What it provides | your own indexed documents | external tools / actions |
| How the agent uses it | `context_providers` | `tools` |
| Example | Contoso Outdoors product docs | Microsoft Learn documentation tools |

---

## Folder structure

For this lab, keep working in the `begin` folder.

The file you will complete is:
- `begin/hostagent-toolbox.py`

---

## Step 1: Open the project and the starter file

> **Already did Lab 1 and Lab 2?** You already have the `agent-framework-helloworld` folder cloned. Just pull the latest changes to get the Lab 3 and Lab 4 guides and starter files:
>
> ```bash
> git pull
> ```

1. Open VS Code and open the cloned `agent-framework-helloworld` folder (clone it first if you have not: `git clone https://github.com/liuhebian/agent-framework-helloworld.git`).
2. Navigate to the `begin` folder.
3. Open `begin/hostagent-toolbox.py`.

You will see a starter script with numbered `TODO` comments, similar to the earlier labs, plus a `FoundryToolbox`.

---

## Step 2: Create the toolbox and add the Microsoft Learn MCP tool

This lab depends on a **Foundry IQ toolbox** that contains the **Microsoft Learn** tool exposed over **MCP (Model Context Protocol)**. You will create the toolbox in your Foundry project and register the Microsoft Learn MCP tool inside it.

1. Open your **Azure AI Foundry project** in the portal.
2. In the left navigation, go to **Toolbox**.
3. Select **Add toolbox** and follow the prompts to create a new toolbox.
4. Inside the toolbox, add the **Microsoft Learn MCP tool** (add a tool via MCP and point it at the Microsoft Learn MCP server).
5. Note the **toolbox name** — you will reference it from code through the `TOOLBOX_NAME` environment variable in the next step.


When you finish this step, you should have:
- a **Foundry IQ toolbox** in your project
- the **Microsoft Learn MCP tool** registered inside that toolbox
- the **toolbox name**, which you will put in the `.env` file in the next step

---

## Step 3: Install the packages

The toolbox uses `FoundryToolbox`, which comes with the packages you already installed in the earlier labs. From the `begin` folder, with your virtual environment activated, make sure the requirements are installed:

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

Open the `.env` file in the `begin` folder (create one if it is missing) and make sure it has the values below. The first two are the same as the earlier labs; `TOOLBOX_NAME` is new for this lab.

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
TOOLBOX_NAME=<your-foundry-iq-toolbox-name>
```

Fictitious example (do not use these values for a real deployment):

```env
FOUNDRY_PROJECT_ENDPOINT=https://contoso-1234.services.ai.azure.com/api/projects/contoso-agent-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
TOOLBOX_NAME=mslearn-toolbox
```

Important:
- each person will have different values
- `TOOLBOX_NAME` must match the toolbox you created in Step 2

---

## Step 5: Review the starter code

Open `begin/hostagent-toolbox.py`.

The starter file already includes numbered `TODO` comments showing where each block of code goes. You will build the agent step by step: first the toolbox, then the client, then the agent, and finally the host server.

The file already includes:
- `load_dotenv(override=True)`
- imports for `Agent`, `FoundryChatClient`, `ResponsesHostServer`, and `FoundryToolbox`
- `DefaultAzureCredential` setup

The `TODO` comments mark the exact sections to complete:
1. `TODO 1` — the `FoundryChatClient` using environment variables
2. `TODO 2` — the `FoundryToolbox`, connected by name
3. `TODO 3` — the `Agent`, with the toolbox attached via `tools`
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

---

## Step 7: Connect the toolbox (`TODO 2`)

This is the new part in Lab 4. Find `TODO 2` and paste this in place of that comment to connect to your Foundry IQ toolbox by name:

```python
    toolbox = FoundryToolbox(credential, name=os.environ["TOOLBOX_NAME"])
```

`FoundryToolbox` loads all the tools registered in that toolbox — including the Microsoft Learn MCP tool you added in Step 2.

---

## Step 8: Create the agent with the toolbox (`TODO 3`)

Find `TODO 3` and paste this in place of that comment. Notice that the toolbox is passed through `tools`:

```python
    agent = Agent(
        client=client,
        instructions=(
            "You are a friendly assistant. Keep your answers brief. "
            "When you use information returned by the Microsoft Learn tools, cite your "
            "sources: end the answer with a 'Sources:' list of markdown links using each "
            "document's title and URL. Only cite sources you actually used."
        ),
        default_options={"store": False},
        tools=[toolbox],
    )
```

The `tools=[toolbox]` line gives the agent every tool in the toolbox.

---

## Step 9: Start the host server (`TODO 4`)

Find `TODO 4` and paste this in place of that comment to start the server:

```python
    server = ResponsesHostServer(agent)
    server.run()
```

Remove the `pass` line at the end of `main()` since the function now has real code.

---

## Step 10: Sign in to Azure

Before running the app, authenticate with Azure:

```bash
azd auth login
```

This gives the app permission to access your Foundry project and the toolbox.

---

## Step 11: Run the agent locally

From the `begin` folder, start the agent:

```bash
python hostagent-toolbox.py
```

If you want to use the `azd` command instead, you can also test it with:

```bash
azd ai agent run --start-command "python hostagent-toolbox.py"
```

If the app starts successfully, you should see the local agent running and ready to accept requests.

---

## Step 12: Test the agent against the toolbox

Open the local endpoint provided by your toolchain and ask a question that the Microsoft Learn tools can answer, for example:

```text
How do I create an Azure AI Search index using the Azure CLI?
```

The agent should:
- call one of the Microsoft Learn tools from the toolbox
- ground its answer in the returned documentation
- end its reply with a `Sources:` list of the pages it used

If the answer is grounded in Microsoft Learn content and includes sources, the toolbox connection is working.

---

## Step 13: (Optional) Deploy remotely with azd

Once the app works locally, you can deploy it the same way as Lab 2. Make sure the `.env` values (including `TOOLBOX_NAME`) are configured in your Azure environment, then run:

```bash
azd deploy
```

After deployment, test the remote endpoint and verify that the agent still uses the toolbox.

---

## Common issues and how to fix them

### 1. `TOOLBOX_NAME` is missing or wrong
Make sure the value in `begin/.env` exactly matches the toolbox you created in Step 2.

### 2. The agent never calls a tool
- confirm the Microsoft Learn MCP tool is registered in the toolbox
- confirm the toolbox is in the same Foundry project as your model
- ask a question that clearly needs documentation

### 3. Permission or authentication errors
- confirm you ran `azd auth login` with the correct account
- confirm your account has access to the Foundry project and the toolbox

---

## What you built

You extended the host agent into a **tool-using agent**. Instead of relying only on the model or your own documents, it now:
- connects to a Foundry IQ toolbox
- calls the Microsoft Learn tools over MCP when it needs documentation
- answers grounded in those results and cites its sources

Together with Lab 3, you have now seen both ways Foundry IQ grounds an agent: **knowledge bases** for your own data, and **toolboxes** for external tools and actions.
