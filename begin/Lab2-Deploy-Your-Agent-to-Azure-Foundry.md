# Lab 2: Deploy Your Agent to Azure AI Foundry

Welcome to Lab 2. In this lab, you will build a lightweight Azure AI Foundry host agent and deploy it using Azure Developer CLI (`azd`).

This lab is designed for people who are new to Python, agent development, and deployment. You will work from the `begin` folder and use the starter file `begin/hostagent.py`.

By the end of this lab, you will be able to:
- set up environment variables in a `.env` file
- complete a starter host agent that connects to Azure AI Foundry
- run the agent locally with `azd`
- deploy the app to Azure AI Foundry or Azure-hosted environment using `azd deploy`
- understand the difference between local testing and remote deployment

---

## Prerequisites

Before you begin, make sure you have the following tools installed:

### Required
- VS Code
- Python 3.10 or newer
- uv
- Git
- Azure CLI
- Azure Developer CLI (`azd`)
- Access to an Azure subscription and an Azure AI Foundry project
- The project files in this repository

### Install links
- Visual Studio Code: https://code.visualstudio.com/download?_exp_download=d53503e735
- Python: https://www.python.org/downloads/
- Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Azure Developer CLI (azd): https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows
- Git: https://git-scm.com/downloads
- uv: https://docs.astral.sh/uv/

### Recommended
- A basic understanding of opening folders in VS Code
- A willingness to run commands in a terminal
- A quiet time slot to complete setup and testing

---

## Lab objective

In this lab, you will create an agent that:
- reads values from a `.env` file
- connects to your Azure AI Foundry project
- uses a customer tool to return customer names by region
- runs as a host agent through `ResponsesHostServer`

The goal is not to build a huge production system. The goal is to understand how a simple agent can be hosted and deployed for Azure AI Foundry scenarios.

---

## Folder structure

For this lab, you should work in the `begin` folder.

Important:
- `begin` = where you complete the exercise
- `final` = completed reference solution

The starter file is:
- `begin/hostagent.py`

---

## Step 1: Open the project folder

1. Open VS Code.
2. Open the repository folder.
3. Navigate to the `begin` folder.
4. Open `begin/hostagent.py`.

You will see a starter script with placeholders and missing logic.

---

## Step 2: Create the environment file

The app expects values in a `.env` file.

The `begin` folder already contains an empty `.env` file. Open it (or create one named `.env` in the `begin` folder if it is missing).

Add the following values, replacing the placeholders with your own resource details:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

Example:

```env
FOUNDRY_PROJECT_ENDPOINT=https://myproject-1234.services.ai.azure.com/api/projects/proj-learninglab
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
```

Important:
- each person will have a different Azure AI Foundry endpoint
- each person will also have a different deployment name
- do not share or copy someone else's values

---

## Step 3: Review the starter code

Open `begin/hostagent.py`.

The starter file already includes placeholders and comments showing where the code should go. The main idea is that you will complete the missing sections during the lab.

The file already includes:
- `load_dotenv()`
- imports for `Agent`, `tool`, `FoundryChatClient`, and `ResponsesHostServer`
- Azure credential setup

The `TODO` comments in the file show you the exact sections to complete:
1. the `@tool` function for customer lookup
2. the `FoundryChatClient` using environment variables
3. the `Agent` setup with `tools=[get_customer]`
4. the `ResponsesHostServer` initialization and run call

Follow the comments and replace the placeholder sections with working code. The `final` folder contains the completed version if you need to compare your work.

---

## Step 4: Complete the tool function

In the starter file, add a function that returns customer names by region.

Use a generic sample, for example:

```python
@tool(approval_mode="never_require")
def get_customer(
    scope: Annotated[str, Field(description="Optional customer scope")] = "all",
) -> str:
    customers = {
        "all": ["Customer A", "Customer B", "Customer C", "Customer D", "Customer E", "Customer F"],
        "region a": ["Customer A", "Customer B"],
        "region b": ["Customer C", "Customer D"],
        "region c": ["Customer E", "Customer F"],
    }
    selected = customers.get(scope.lower(), customers["all"])
    return f"Customers for scope '{scope}' are: {', '.join(selected)}."
```

This provides the agent with a simple lookup mechanism.

---

## Step 5: Complete the Foundry client setup

Add the code to create the client from environment variables:

```python
client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    credential=DefaultAzureCredential(),
)
```

This uses the values from your `.env` file and the Azure identity available on your machine.

---

## Step 6: Create the agent and host server

Create the agent and bind the tool:

```python
agent = Agent(
    client=client,
    instructions="You are a friendly assistant. Keep your answers brief.",
    default_options={"store": False},
    tools=[get_customer],
)
```

Then start the server:

```python
server = ResponsesHostServer(agent)
server.run()
```

This is the code path that allows the agent to be hosted in Azure AI Foundry and started locally for testing.

---

## Step 7: Sign in to Azure

Before running the app, authenticate with Azure:

```bash
az login
```

Then authenticate Azure Developer CLI:

```bash
azd auth login
```

This gives the tools permission to access your Azure resources and your Foundry project.

---

## Step 8: Initialize the Azure Developer project

In the project folder, run:

```bash
azd ai agent init
```

This initializes the project for agent-based Azure development.

If the command asks for project details or Azure configuration, follow the prompts or ask your instructor for help.

---

## Step 9: Run the agent locally

Use the following command to start the agent locally:

```bash
python hostagent.py
```

This is the direct local run command for the host agent in this lab.

If you want to use the `azd` command instead, you can also test it with:

```bash
azd ai agent run --start-command "python hostagent.py"
```

If the app starts successfully, you should see the local agent running and ready to accept requests.

---

## Step 10: Test the agent locally

Open a browser or use the local endpoint provided by your toolchain and ask the agent a question such as:

```text
Which customers are in Region A?
```

Or:

```text
Show me all customers.
```

The agent should use the `get_customer` tool and respond with the list of customers in the sample data.

---

## Step 11: Deploy remotely with azd

Once the app works locally, deploy it with:

```bash
azd deploy
```

This pushes the app to the configured Azure environment and prepares it for remote use.

After deployment, test the remote endpoint and verify that the agent is responding.

---

## Step 12: Understand the difference between local and remote

### Local run
Use `azd ai agent run` when you want to:
- test quickly
- debug issues in your code
- validate your `.env` values
- confirm the agent behaves as expected before deployment

### Remote deploy
Use `azd deploy` when you want to:
- host the app in Azure-managed infrastructure
- share the agent with broader users
- test the deployed environment end-to-end

---

## Common issues and how to fix them

### 1. `.env` values are missing
Make sure the file exists in the `begin` folder and includes both values:

```env
FOUNDRY_PROJECT_ENDPOINT=...
AZURE_AI_MODEL_DEPLOYMENT_NAME=...
```

### 2. `azd` is not recognized
Install Azure Developer CLI and verify it works:

```bash
azd version
```

### 3. `az login` fails
- make sure you are signed in with the correct Azure account
- confirm you have access to the subscription and Foundry project

### 4. The app cannot connect to Azure AI Foundry
Check:
- the project endpoint value in `.env`
- the model deployment name value in `.env`
- your Azure permissions
- whether the model deployment is active in your project

### 5. `DefaultAzureCredential` cannot authenticate
Make sure you have logged in using:

```bash
az login
```

If needed, verify your account context with:

```bash
az account show
```

---

## If you cannot finish during class

If you do not complete the steps in class, you can continue later using the same process.

### Continue later checklist
1. Open the project folder in VS Code.
2. Go to the `begin` folder.
3. Confirm your `.env` file contains your project values.
4. Activate the environment if needed.
5. Run:

```bash
azd auth login
azd ai agent init
python hostagent.py
```

If you prefer the `azd` local run pattern, you can also use:

```bash
azd ai agent run --start-command "python hostagent.py"
```

6. If the app works locally, run:

```bash
azd deploy
```

7. Test the app again.
8. Compare your result with the completed solution in the `final` folder if needed.

---

## Lab summary

In this lab, you learned how to:
- configure environment variables for Azure AI Foundry
- complete a starter host agent in the `begin` folder
- use `azd` for local agent testing and deployment
- move from local validation to remote hosting

This is the foundation for more advanced Azure AI agent scenarios.

---

## Optional homework

Before Lab 3, try the following:
1. change the tool data to a different set of sample customers
2. add a new region name such as `region c`
3. try a new question prompt for the agent
4. write down one business use case where a hosted agent could help your team

---

## Next steps

In Lab 3, you will continue building more advanced agent experiences and expand the business scenario beyond the simple tool-based example.

For now, your main focus is to make sure the app runs locally and successfully deploys using `azd`.
