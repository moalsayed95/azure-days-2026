"""
🌍 Azure AI Agent Framework - Travel Agent Demo
================================================

This script demonstrates how to create an AI agent using the 
Microsoft Agent Framework with Azure AI Foundry.

Prerequisites:
1. Copy .env.example to .env and fill in your Azure AI Foundry credentials
2. Run with: uv run python travel_agent.py
"""

import os
import asyncio
from random import randint
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


# 🔧 Load environment variables from .env file
load_dotenv()


# 🎲 Tool Function: Random Destination Generator
def get_random_destination() -> str:
    """Get a random vacation destination.
    
    Returns:
        str: A randomly selected destination from our predefined list
    """
    destinations = [
        "Barcelona, Spain",
        "Paris, France", 
        "Berlin, Germany",
        "Tokyo, Japan",
        "Sydney, Australia",
        "New York, USA",
        "Cairo, Egypt",
        "Cape Town, South Africa",
        "Rio de Janeiro, Brazil",
        "Bali, Indonesia"
    ]
    return destinations[randint(0, len(destinations) - 1)]


async def main():
    """Main function to run the travel agent."""
    
    # ✅ Check environment variables
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    model_id = os.environ.get("AZURE_OPENAI_MODEL_ID")
    
    if not all([endpoint, api_key, model_id]):
        print("❌ Error: Missing environment variables!")
        print("   Please copy .env.example to .env and fill in your Azure credentials.")
        print()
        print("   Required variables:")
        print("   - AZURE_OPENAI_ENDPOINT")
        print("   - AZURE_OPENAI_API_KEY")
        print("   - AZURE_OPENAI_MODEL_ID")
        return
    
    print("🚀 Starting Azure AI Travel Agent...")
    print(f"   Endpoint: {endpoint}")
    print(f"   Model: {model_id}")
    print()
    
    # 🔗 Create OpenAI Chat Client for Azure AI Foundry
    openai_chat_client = OpenAIChatClient(
        base_url=endpoint,
        api_key=api_key, 
        model_id=model_id
    )
    
    # 🤖 Create the Travel Planning Agent
    agent = ChatAgent(
        chat_client=openai_chat_client,
        instructions="You are a helpful AI Agent that can help plan vacations for customers at random destinations.",
        tools=[get_random_destination]
    )
    
    # 🚀 Run the Agent
    print("📤 Sending request: 'Plan me a day trip'")
    print("-" * 50)
    
    response = await agent.run("Plan me a day trip")
    
    # 📖 Extract and display the response
    last_message = response.messages[-1]
    text_content = last_message.contents[0].text
    
    print()
    print("🏖️ Travel Plan:")
    print("-" * 50)
    print(text_content)
    print()
    print("✅ Agent completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
