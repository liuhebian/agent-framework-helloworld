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
- An Azure AI Foundry service with a deployed `gpt-5.4-mini` model
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

The starter file is:
- `begin/hostagent.py`

---

## Step 1: Clone and open the project folder

1. Clone the repository (skip this if you already cloned it in Lab 1):

   ```bash
   git clone https://github.com/liuhebian/agent-framework-helloworld.git
   ```

2. Open VS Code and open the cloned `agent-framework-helloworld` folder.
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
FOUNDRY_PROJECT_ENDPOINT=https://contoso-1234.services.ai.azure.com/api/projects/contoso-agent-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
```

Important:
- each person will have a different Azure AI Foundry endpoint
- each person will also have a different deployment name
- do not share or copy someone else's values

---

## Step 3: Review the starter code

Open `begin/hostagent.py`.

The starter file already includes numbered `TODO` comments showing where the code should go. You will build the host agent step by step: first the client, then the agent, then the host server, and finally the tool.

The file already includes:
- `load_dotenv()`
- imports for `Agent`, `tool`, `FoundryChatClient`, and `ResponsesHostServer`
- Azure credential setup

The `TODO` comments mark the exact sections to complete:
1. `TODO 1` — the `FoundryChatClient` using environment variables
2. `TODO 2` — the `Agent` setup
3. `TODO 3` — the `ResponsesHostServer` initialization and run call
4. `TODO 4` — the `@tool` function for customer lookup, added last

In the next steps you will copy the code for each `TODO` from this guide and paste it in place of the matching comment.

---

## Step 4: Complete the Foundry client setup (`TODO 1`)

Find `TODO 1` and paste this in place of that comment to create the client from environment variables:

```python
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )
```

This uses the values from your `.env` file and the Azure identity available on your machine.

---

## Step 5: Create the agent (`TODO 2`)

Find `TODO 2` and paste this in place of that comment to create the agent:

```python
    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
        default_options={"store": False},
    )
```

At this point the agent has no tools yet. You will add one later.

---

## Step 6: Start the host server (`TODO 3`)

Find `TODO 3` and paste this in place of that comment to start the server:

```python
    server = ResponsesHostServer(agent)
    server.run()
```

Remove the `pass` line at the end of `main()` since the function now has real code. This is the code path that allows the agent to be hosted in Azure AI Foundry and started locally for testing.

---

## Step 7: Add the `get_customer` tool (`TODO 4`)

Now give the agent a tool so it can answer questions using your own data.

Find `TODO 4` and paste this in place of that comment. It returns customer names by region:

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

Then update the `Agent` you created at `TODO 2` to include the tool:

```python
    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
        default_options={"store": False},
        tools=[get_customer],
    )
```

---

## Step 8: Sign in to Azure

Before running the app, authenticate with Azure:

```bash
az login
```

Then authenticate Azure Developer CLI:

```bash
azd auth login
```

This gives the tools permission to access your Azure resources and your Foundry project.

> **Tip: fix the multifactor authentication (MFA) error during deployment**
>
> Some subscriptions require multifactor authentication (MFA). If a later step such as `azd provision` or `azd up` fails with an error like:
>
> ```text
> ERROR: ... AzureDeveloperCLICredential: Azure Developer CLI requires multifactor authentication or additional claims.
> ```
>
> `azd` is using a stale cached token that did not go through MFA. Fixing it takes three steps: remove the cached token, sign in again with the device code flow (which forces the MFA prompt), then retry.
>
> **1. Remove the cached `azd` token** (PowerShell on Windows). The cache lives in your user profile at `~/.azd/auth.json`. Back it up first, then delete it:
>
> ```powershell
> Copy-Item "$env:USERPROFILE\.azd\auth.json" "$env:USERPROFILE\.azd\auth.json.bak" -Force -ErrorAction SilentlyContinue
> Remove-Item "$env:USERPROFILE\.azd\auth.json" -Force -ErrorAction SilentlyContinue
> ```
>
> **2. Sign in again with the device code flow** against the tenant in the error message:
>
> ```bash
> azd auth login --tenant-id <your-tenant-id> --use-device-code
> ```
>
> Replace `<your-tenant-id>` with the tenant ID shown in the error (the value after `--tenant-id` in the suggested command). Copy the code shown in the terminal, open https://microsoft.com/devicelogin, enter the code, and complete the sign-in **including the MFA prompt**.
>
> **3. Retry the deployment:**
>
> ```bash
> azd provision
> ```
>
> If you want to confirm the new token went through MFA, decode it and check the `acr` claim — a value of `"1"` means MFA was performed:
>
> ```powershell
> $token = (azd auth token -o json --scope https://management.core.windows.net//.default --tenant-id <your-tenant-id> | ConvertFrom-Json).token
> $p = $token.Split('.')[1].Replace('-','+').Replace('_','/')
> switch ($p.Length % 4) { 2 { $p += '==' } 3 { $p += '=' } }
> [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($p)) | ConvertFrom-Json | Select-Object acr, amr | ConvertTo-Json
> ```

---

## Step 9: Initialize the Azure Developer project

In the project folder, run:

```bash
azd ai agent init
```

This initializes the project for agent-based Azure development. Use the following example to complete the prompts:

```text
? How do you want to initialize your agent? Use the code in the current directory
? What is the name of your project? begin
? Enter a name for your agent: begin
? How would you like to deploy your agent? Container Image (Docker)
? Which protocols does your agent support? responses
? Select a Foundry project to host your agent and any models or tools it uses. Use an existing Foundry project
? Select subscription: <select your Azure subscription>
? Select a Foundry project: <select your Foundry project>
? Enter your ACR login server (e.g., myregistry.azurecr.io), or leave blank to create a new one:
? How would you like to configure model(s) for your agent? Use an existing model deployment
? Select a model deployment: gpt-5.4-mini
? Enter the command to start your agent (e.g., python main.py), or leave blank to skip: python hostagent.py
```

Important:
- For **Select subscription**, choose the Azure subscription assigned to you. The displayed subscription name and ID will be different for each user.
- For **Select a Foundry project**, choose your own Foundry project from the selected subscription. The project name and region will depend on your selection.
- For the ACR login server, leave the value blank if you want `azd up` to create a new Azure Container Registry. Otherwise, enter the login server of an existing ACR you can use.
- If your model deployment has a different name, select it and use that same name for `AZURE_AI_MODEL_DEPLOYMENT_NAME` in your `.env` file.

---

## Step 10: Run the agent locally

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

## Step 11: Test the agent locally

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

## Step 12: Deploy remotely with azd

Once the app works locally, deploy it with:

```bash
azd deploy
```

This pushes the app to the configured Azure environment and prepares it for remote use.

After deployment, test the remote endpoint and verify that the agent is responding.

---

## Step 13: Understand the difference between local and remote

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
