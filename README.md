# 🚀 Azure Days 2026 - AI Travel Agent Hackathon

Build an intelligent travel planning agent using the **Microsoft Agent Framework** for Python and **Azure AI Foundry**!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/moalsayed95/azure-days-2026?quickstart=1)

## 🎯 What You'll Build

An AI-powered travel agent that:
- 🎲 Selects random vacation destinations using custom tool functions
- 🗺️ Generates detailed day-trip itineraries with local recommendations
- 🤖 Demonstrates function calling capabilities in AI agents

## ⚡ Quick Start with GitHub Codespaces

### Option 1: One-Click Setup (Recommended)

1. Click the **"Open in GitHub Codespaces"** button above
2. Wait for the environment to build (~2-3 minutes)
3. Set up your Azure credentials (see below)
4. Open `python-agent-framework-travelagent.ipynb` and start coding!

### Option 2: Manual Codespace Creation

1. Click the green **"Code"** button on this repo
2. Select the **"Codespaces"** tab
3. Click **"Create codespace on main"**

## 🔑 Setting Up Your Azure Credentials

### In GitHub Codespaces

After your Codespace is ready, create a `.env` file with your Azure AI credentials:

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   AZURE_OPENAI_ENDPOINT=https://<your-resource-name>.openai.azure.com/openai/v1/
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_MODEL_ID=gpt-4o-mini
   ```

### Getting Azure AI Foundry Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create or navigate to your **Azure OpenAI** resource
3. Go to **Keys and Endpoint** section
4. Copy your **Endpoint** and **Key**
5. Note your deployed model name (e.g., `gpt-4o-mini`)

> 💡 **Hackathon Tip**: Your hackathon organizers may provide shared credentials!

## 📓 Running the Notebook

1. Open `python-agent-framework-travelagent.ipynb`
2. When prompted, select the Python kernel
3. Run cells sequentially (Shift + Enter)
4. Watch the AI agent plan your vacation! 🏖️

## 🏗️ Project Structure

```
├── .devcontainer/          # GitHub Codespaces configuration
│   └── devcontainer.json   # Container setup with Python & Jupyter
├── .env.example            # Template for environment variables
├── python-agent-framework-travelagent.ipynb  # 🎯 Main hackathon notebook
└── requirements.txt        # Python dependencies
```

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| AI Framework | Microsoft Agent Framework |
| AI Backend | Azure AI Foundry (OpenAI) |
| Model | GPT-4o-mini |
| Environment | GitHub Codespaces |

## 📚 Key Concepts

### Agent Framework Components

```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

# Create AI client
client = OpenAIChatClient(
    base_url=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    model_id=os.environ.get("AZURE_OPENAI_MODEL_ID")
)

# Create agent with tools
agent = ChatAgent(
    chat_client=client,
    instructions="You are a helpful travel planning agent.",
    tools=[get_random_destination]  # Custom function tools
)

# Run the agent
response = await agent.run("Plan me a day trip")
```

### Tool Functions

The agent can call custom Python functions as "tools":

```python
def get_random_destination() -> str:
    """Get a random vacation destination."""
    destinations = ["Paris", "Tokyo", "New York", ...]
    return random.choice(destinations)
```

## 🎓 Hackathon Challenges

Once you complete the basic notebook, try these extensions:

1. **🌍 Add More Destinations**: Expand the destination list
2. **📅 Multi-Day Trips**: Modify the agent to plan week-long vacations
3. **💰 Budget Planning**: Add a tool to estimate trip costs
4. **🍽️ Restaurant Finder**: Create a new tool for food recommendations
5. **✈️ Flight Search**: Integrate with a flight API

## 🆘 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "API Key Invalid" Error
- Double-check your `.env` file credentials
- Ensure there are no extra spaces or quotes
- Verify your Azure OpenAI resource is deployed

### "Resource not found" Error
- Double check your `.env` file
- The `AZURE_OPENAI_ENDPOINT` has to follow this format: https://XXXXX.openai.azure.com/openai/v1/
- If you need to fix, also restart kernel

### Kernel Not Found
- Click "Select Kernel" in the top-right of the notebook
- Choose "Python 3.12" or the recommended Python interpreter

## 📖 Resources

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service)
- [GitHub Codespaces Docs](https://docs.github.com/codespaces)

## 🤝 Contributing

Found a bug or have an improvement? Open an issue or PR!

---

**Happy Hacking! 🎉**

*Built for Azure Days 2026 Hackathon*
