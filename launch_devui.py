
import os
import sys
from random import randint
from datetime import datetime, timezone
from collections.abc import MutableSequence
from typing import Any
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# Enable sensitive data capture in instrumentation (includes system prompts)
os.environ["ENABLE_SENSITIVE_DATA"] = "true"

from agent_framework import ChatAgent, Context, ContextProvider, ChatMessage
from agent_framework.openai import OpenAIChatClient
from agent_framework.devui import serve
from amadeus_client import (
    get_cheapest_travel_days,
    get_flight_offers,
    get_airport_code
)

load_dotenv(override=True)

class CurrentDateContextProvider(ContextProvider):
    """A context provider that informs the agent about the current date, time, and timezone."""

    async def invoking(self, messages: ChatMessage | MutableSequence[ChatMessage], **kwargs: Any) -> Context:
        """Provide current date context before each agent invocation."""
        # Get local time with timezone info
        local_now = datetime.now().astimezone()
        timezone_name = local_now.tzname() or "Local"
        
        # Get UTC time
        utc_now = datetime.now(timezone.utc)
        
        date_info = (
            f"Current date: {local_now.strftime('%A, %B %d, %Y')}. "
            f"Local time: {local_now.strftime('%I:%M %p')} ({timezone_name}). "
            f"UTC time: {utc_now.strftime('%I:%M %p')} (UTC)."
        )
        """ log date_info for debugging """
        print(date_info)
        return Context(instructions=date_info)

def get_random_destination() -> str:
    destinations = [
        # United States
        "New York City, New York, USA",
        "Los Angeles, California, USA",
        "San Francisco, California, USA",
        "Miami, Florida, USA",
        "Las Vegas, Nevada, USA",
        "Orlando, Florida, USA",

        # Spain
        "Barcelona, Spain",
        "Madrid, Spain",
        "Seville, Spain",
        "Valencia, Spain",
        "Granada, Spain",

        # United Kingdom
        "London, England, United Kingdom",
        "Edinburgh, Scotland, United Kingdom",
        "Manchester, England, United Kingdom",
        "Bath, England, United Kingdom",
        "Belfast, Northern Ireland, United Kingdom",

        # Germany
        "Berlin, Germany",
        "Munich, Germany",
        "Hamburg, Germany",
        "Frankfurt, Germany",
        "Cologne, Germany",

        # India
        "New Delhi, India",
        "Mumbai, India",
        "Jaipur, India",
        "Agra, India",
        "Goa, India",
        "Bengaluru, India",
        "Kolkata, India",
    ]
    return destinations[randint(0, len(destinations) - 1)]

openai_chat_client = OpenAIChatClient(
    base_url=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"), 
    model_id=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
)

agent = ChatAgent(
    chat_client=openai_chat_client,
    instructions="""You are a helpful AI Travel Agent that can help plan vacations and search for flights.
    
    You have access to the following capabilities:
    - Get random vacation destination suggestions
    - Find the cheapest travel days for any route
    - Search for detailed flight offers with prices
    - Look up airport codes for any city

    Be aware that currently, the functions only cover a limited set of countries.
    If lookups for a specific city or route fail or contain no data, inform the user politely.
    Currently the following countries are supported: United States, Spain, United Kingdom, Germany and India
    
    When users ask about flights, always ask for their origin and destination cities if not provided.
    Use the get_airport_code function to find IATA codes when needed.
    Provide helpful, detailed information about flight options and prices.""",
    tools=[
        get_random_destination,
        get_cheapest_travel_days,
        get_flight_offers,
        get_airport_code
    ],
    context_provider=CurrentDateContextProvider()
)

# Launch DevUI - this works in a standalone script
serve(entities=[agent], port=8080, auto_open=True, instrumentation_enabled=True)
