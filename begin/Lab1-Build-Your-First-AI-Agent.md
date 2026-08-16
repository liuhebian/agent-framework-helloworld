# Lab 1: Build Your First AI Agent

Welcome to Lab 1. This lab is designed for non-technical or less technical participants. The goal is simple: you will create a small AI agent that can answer a question by using a built-in tool to look up customer names.

By the end of this lab, you will have:
- created a Python environment
- installed the required packages
- connected the app to Azure AI Foundry
- run a working AI agent
- asked the agent a business question and received a response

This lab is intentionally beginner-friendly. You do not need to be a software developer to follow along.

---

## Prerequisites

Before you start, make sure you have all of the following:

### Required
- A laptop with VS Code installed (Windows or macOS)
- Python 3.10 or newer
- uv installed on your machine
- Internet access
- An Azure account with access to the lab project in Azure AI Foundry
- Azure CLI installed on your machine
- Azure Developer CLI (`azd`) installed on your machine
- Git installed on your machine
- The project files in this repository

### Install links for missing tools
- Visual Studio Code: https://code.visualstudio.com/download?_exp_download=d53503e735
- Python: https://www.python.org/downloads/
- Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
- Azure Developer CLI (azd): https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows
- Git: https://git-scm.com/downloads
- uv: https://docs.astral.sh/uv/

### Recommended
- A basic understanding of opening a folder in VS Code
- A willingness to run simple commands in a terminal
- A quiet time slot to complete the setup and the lab

### Check your setup
Open a terminal in VS Code and run:

```bash
python --version
uv --version
az --version
```

If Python, uv, or Azure CLI is not found, ask the instructor before continuing.

If `uv` is not installed, install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows PowerShell, use:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Lab Objective

In this lab, you will build a very simple AI agent that can answer questions such as:
- "Which customers are in Region A?"
- "Show me the customers for Region B."
- "What customers are in Region C?"

The agent will use a tool called `get_customer` to fetch the list from a predefined dictionary.

---

## Step 1: Open the project folder

1. Open VS Code.
2. Open the folder:
   - `AInstein-Agentlearninglab`
3. In the Explorer pane, locate the `begin` folder and the files inside it.
4. You will work from the `begin` folder for this lab.

The `final` folder is the completed reference solution and should only be used after you finish or if you need to compare your work.

In the `begin` folder, you will see the starter files for the exercise.

---

## Step 2: Create the Python environment with uv

uv helps us create a clean Python environment and install the libraries needed for the lab.

In the terminal, go to the project folder and run:

```bash
cd begin
uv venv
```

Then activate it:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

If activation works, your terminal prompt should show `(.venv)`.

---

## Step 3: Install the required packages

Run:

```bash
uv pip install -r requirements.txt
```

This installs the libraries needed for the AI agent and Azure AI Foundry.

If the command says there are no packages or shows a warning, do not panic. Check that you are inside the `begin` folder and that the file `requirements.txt` exists.

---

## Step 4: Sign in to Azure

The agent uses Azure identity to connect to the AI Foundry project.

In your terminal, run:

```bash
az login
```

This will open a browser for Azure sign-in. Log in with your lab account.

After logging in, verify the account is active:

```bash
az account show
```

You should see your subscription and account information.

---

## Step 5: Review the starter code

Open the starter file in the `begin` folder: `begin/basic.py`.

This file intentionally includes placeholder comments where the working code should go. Your task in the lab is to fill in each section with the correct code.

The main sections to complete are:

1. A tool named `get_customer`
   - This is the function the agent can call
   - It returns a list of customers by region

2. A client object using `FoundryChatClient`
   - This connects the Python code to Azure AI Foundry

3. An `Agent` instance
   - This is the AI assistant

4. A chat loop
   - It asks for input and sends each message to the agent

The file includes comments such as `TODO` and example code blocks to guide you. Follow those placeholders and replace them with the working code.

> The `final` folder contains the completed working version. Use it only after the lab or if you get stuck.

---

## Step 6: Add your own AI project endpoint

The script needs your own Azure AI Foundry project endpoint. Each participant will have a different project URL.

Find the line in the code that looks like this:

```python
project_endpoint="https://<your-project-prefix>.services.ai.azure.com/api/projects/<your-project-name>"
```

Replace the placeholder values with your own project details from the lab instructions or your Azure AI Foundry project.

For example, your instructor may give you a value like:

```python
project_endpoint="https://myproject-1234.services.ai.azure.com/api/projects/proj-learninglab"
```

Important: do not copy someone else's endpoint. Each learner should use their own project endpoint.

---

## Step 7: Run the lab script

In the terminal, run:

```bash
python basic.py
```

You should see something like:

```text
Chat started. Type 'exit' or 'bye' to quit.
You:
```

At this point, the program is waiting for your question.

---

## Step 8: Test the agent

Try asking the agent:

```text
Which customers are in Region A?
```

Or:

```text
Show me the customers in Region B.
```

Or:

```text
What customers are in Region C?
```

The agent should answer using the tool and return the customer names stored in the sample data.

Example response:

```text
Agent: Customers for scope 'Region A' are: Customer A, Customer B.
```

---

## Step 9: Understand what happened

The agent responded because:
- it had a tool called `get_customer`
- the tool knows the customer lists
- the AI model decided to use the tool when it needed a factual answer

This is a simple example of an agent using a tool to answer a user question.

In real-world use, the tool could call:
- a CRM system
- a database
- an Excel file
- an internal business application
- a web service

---

## Step 10: Exit the chat

Type either of the following:

```text
exit
```

or

```text
bye
```

The program will end and print a goodbye message.

---

## Common issues and how to fix them

### 1. The command says `python` is not recognized
Try one of these:

On Windows:

```bash
py -3 --version
```

Then run:

```bash
py -3 basic.py
```

On macOS:

```bash
python3 --version
```

Then run:

```bash
python3 basic.py
```

### 2. `az login` fails
- confirm Azure CLI is installed
- sign in with the correct lab account
- make sure your account has access to the Azure AI project

### 3. Import errors appear
Make sure you activated the virtual environment and installed the packages:

```bash
uv pip install -r requirements.txt
```

### 4. The app cannot connect to AI Foundry
- verify the project endpoint in the script
- confirm that your Azure account has access
- ask the instructor to confirm the correct project URL

### 5. The agent does not answer as expected
Try asking a simple question with one region name:
- Region A
- Region B
- Region C
- all

The sample tool supports these values.

---

## If you need to continue after class

If you could not finish the lab during class, you can continue at home using the same steps.

### Continue later checklist
1. Open the project folder in VS Code.
2. Go to the `begin` folder.
3. Activate the virtual environment.
   - Windows: `\.venv\Scripts\Activate.ps1`
   - macOS: `source .venv/bin/activate`
4. Run `uv pip install -r requirements.txt` if needed.
5. Run `az login` if you are not already signed in.
6. Start the app with:

```bash
python basic.py
```

If Python points to the wrong version on macOS, use:

```bash
python3 basic.py
```

7. Ask a simple customer question.
8. Keep the script open and test a few variations.
9. If needed, compare your work with the solution in the `final` folder.

### Helpful reminder
Use very simple prompts like:
- "Which customers are in Region A?"
- "Show me all customers"
- "What customers are in Region B?"

These are easier for a beginner agent to understand than long or vague questions.

---

## Lab summary

In this first lab, you learned how to:
- set up a Python environment
- install project dependencies
- connect to Azure AI Foundry
- create a simple AI agent
- use a tool to answer a business question

This is the foundation for the next labs.

---

## Optional homework

Before Lab 2, try these tasks:

1. Change one customer list in the code.
2. Add a new region such as `singapore`.
3. Ask the agent a new question.
4. Write down one business scenario where this kind of agent could help your team.

Bring your notes to the next lab.

---

## Next Lab

Lab 2 will go deeper into agent behavior, tool design, and more advanced usage patterns.

For now, the most important thing is that you have a working AI agent that can respond to a business question using a tool.
