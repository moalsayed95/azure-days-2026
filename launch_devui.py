
import os
from random import randint
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from agent_framework.devui import serve

load_dotenv()

def get_random_destination() -> str:
    destinations = [
        "Barcelona, Spain", "Paris, France", "Berlin, Germany",
        "Tokyo, Japan", "Sydney, Australia", "New York, USA",
        "Cairo, Egypt", "Cape Town, South Africa", 
        "Rio de Janeiro, Brazil", "Bali, Indonesia"
    ]
    return destinations[randint(0, len(destinations) - 1)]

openai_chat_client = OpenAIChatClient(
    base_url=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"), 
    model_id=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
)

agent = ChatAgent(
    chat_client=openai_chat_client,
    instructions="You are a helpful AI Agent that can help plan vacations for customers at random destinations.",
    tools=[get_random_destination]
)

# Launch DevUI - this works in a standalone script
serve(entities=[agent], port=8080, auto_open=True)
