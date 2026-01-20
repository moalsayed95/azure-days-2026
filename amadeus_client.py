"""
Amadeus Travel API Client and Tool Functions

This module provides a wrapper around the Amadeus API client
and implements AI tool functions for flight search and travel planning.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from amadeus import Client, ResponseError

class AmadeusClientWrapper:
    """Wrapper for Amadeus API client with credential management."""
    
    def __init__(self):
        """Initialize Amadeus client with credentials from environment."""
        api_key = os.environ.get("AMADEUS_API_KEY")
        api_secret = os.environ.get("AMADEUS_API_SECRET")
        
        if not api_key or not api_secret:
            raise ValueError(
                "Amadeus credentials not found. "
                "Please set AMADEUS_API_KEY and AMADEUS_API_SECRET in your .env file"
            )
        
        self.client = Client(
            client_id=api_key,
            client_secret=api_secret
        )
    
    def get_client(self) -> Client:
        """Get the underlying Amadeus client."""
        return self.client


# Create global client instance
_amadeus_wrapper = None


def get_amadeus_client() -> Client:
    """Get or create the global Amadeus client instance."""
    global _amadeus_wrapper
    if _amadeus_wrapper is None:
        _amadeus_wrapper = AmadeusClientWrapper()
    return _amadeus_wrapper.get_client()


def get_cheapest_travel_days(
    origin: str,
    destination: str,
    departure_date: Optional[str] = None,
    duration: Optional[str] = None
) -> str:
    """
    Find the cheapest travel days for a given route.
    
    This function queries the Amadeus Flight Cheapest Date Search API
    to find the most affordable dates to travel between two cities.
    
    Args:
        origin: IATA code of the departure city (e.g., "LAX" for Los Angeles)
        destination: IATA code of the arrival city (e.g., "CDG" for Paris)
        departure_date: Optional departure date in YYYY-MM-DD format.
                       If not provided, searches from today onwards.
        duration: Optional trip duration (e.g., "1-7" for 1 to 7 days).
                 If not provided, searches various durations.
    
    Returns:
        str: A formatted string with the cheapest travel dates and prices,
             or an error message if the search fails.
    
    Example:
        >>> get_cheapest_travel_days("LAX", "CDG", departure_date="2026-06-01")
        "Cheapest travel dates from LAX to CDG:
        1. June 5-12, 2026: $450
        2. June 8-15, 2026: $475
        3. June 12-19, 2026: $490"
    """
    try:
        client = get_amadeus_client()
        
        # If no departure date provided, use 30 days from now
        if not departure_date:
            future_date = datetime.now() + timedelta(days=30)
            departure_date = future_date.strftime("%Y-%m-%d")
        
        # Search for cheapest dates
        response = client.shopping.flight_dates.get(
            origin=origin,
            destination=destination,
            departureDate=departure_date,
            duration=duration
        )
        
        if not response.data:
            return f"No flight data found for route {origin} to {destination}."
        
        # Format results
        results = []
        for idx, offer in enumerate(response.data[:5], 1):  # Top 5 results
            date = offer.get('departureDate', 'N/A')
            return_date = offer.get('returnDate', 'N/A')
            price = offer.get('price', {}).get('total', 'N/A')
            currency = offer.get('price', {}).get('currency', '')
            
            if return_date != 'N/A':
                results.append(
                    f"{idx}. {date} to {return_date}: {currency} {price}"
                )
            else:
                results.append(
                    f"{idx}. {date} (one-way): {currency} {price}"
                )
        
        header = f"Cheapest travel dates from {origin} to {destination}:\n"
        return header + "\n".join(results)
        
    except ResponseError as error:
        return f"Amadeus API error: {error.description}"
    except Exception as e:
        return f"Error searching for cheapest travel days: {str(e)}"


def get_flight_offers(
    origin: str,
    destination: str,
    departure_date: str,
    adults: int = 1,
    return_date: Optional[str] = None,
    travel_class: str = "ECONOMY",
    max_results: int = 5,
    nonstop: bool = False,
    currency: str = "USD"
) -> str:
    """
    Search for flight offers with detailed parameters.
    
    This function queries the Amadeus Flight Offers Search API
    to find available flights with prices and details.
    
    Args:
        origin: IATA code of departure airport (e.g., "JFK")
        destination: IATA code of arrival airport (e.g., "LAX")
        departure_date: Departure date in YYYY-MM-DD format
        adults: Number of adult passengers (default: 1)
        return_date: Optional return date in YYYY-MM-DD format for round trips
        travel_class: Cabin class - "ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", or "FIRST"
        max_results: Maximum number of flight offers to return (default: 5)
        nonstop: If True, only return non-stop flights (default: False)
        currency: Preferred currency code (default: "USD")
    
    Returns:
        str: A formatted string with flight offers including times, prices, and airlines,
             or an error message if the search fails.
    
    Example:
        >>> get_flight_offers("JFK", "LAX", "2026-06-15", adults=2, return_date="2026-06-22")
        "Flight offers from JFK to LAX:
        
        Option 1: $450 per person
        Outbound: JFK → LAX on June 15, 2026 at 08:00 AM (American Airlines)
        Return: LAX → JFK on June 22, 2026 at 03:00 PM (American Airlines)
        Duration: 5h 30m outbound, 5h 15m return
        ..."
    """
    try:
        client = get_amadeus_client()
        
        # Build search parameters
        search_params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': adults,
            'currencyCode': currency,
            'max': max_results
        }
        
        # Add optional parameters
        if return_date:
            search_params['returnDate'] = return_date
        
        if nonstop:
            search_params['nonStop'] = 'true'
        
        if travel_class and travel_class != "ECONOMY":
            search_params['travelClass'] = travel_class
        
        # Search for flight offers
        response = client.shopping.flight_offers_search.get(**search_params)
        
        if not response.data:
            return f"No flight offers found for route {origin} to {destination} on {departure_date}."
        
        # Format results
        results = []
        trip_type = "round-trip" if return_date else "one-way"
        header = f"Flight offers ({trip_type}) from {origin} to {destination}:\n"
        
        for idx, offer in enumerate(response.data[:max_results], 1):
            price = offer.get('price', {}).get('total', 'N/A')
            currency_code = offer.get('price', {}).get('currency', currency)
            
            # Get itinerary details
            itineraries = offer.get('itineraries', [])
            
            flight_details = [f"\nOption {idx}: {currency_code} {price}"]
            
            for itin_idx, itinerary in enumerate(itineraries):
                segments = itinerary.get('segments', [])
                duration = itinerary.get('duration', 'N/A')
                
                if itin_idx == 0:
                    flight_type = "Outbound"
                else:
                    flight_type = "Return"
                
                if segments:
                    first_segment = segments[0]
                    last_segment = segments[-1]
                    
                    departure = first_segment.get('departure', {})
                    arrival = last_segment.get('arrival', {})
                    airline = first_segment.get('carrierCode', 'N/A')
                    
                    dep_time = departure.get('at', 'N/A')
                    arr_time = arrival.get('at', 'N/A')
                    
                    stops = len(segments) - 1
                    stops_text = "non-stop" if stops == 0 else f"{stops} stop(s)"
                    
                    flight_details.append(
                        f"  {flight_type}: {departure.get('iataCode', origin)} → "
                        f"{arrival.get('iataCode', destination)} "
                        f"on {dep_time[:10]} at {dep_time[11:16]} "
                        f"(Airline: {airline}, {stops_text})"
                    )
                    flight_details.append(f"  Duration: {duration}")
            
            results.append("\n".join(flight_details))
        
        return header + "\n".join(results)
        
    except ResponseError as error:
        return f"Amadeus API error: {error.description}"
    except Exception as e:
        return f"Error searching for flight offers: {str(e)}"


def get_airport_code(city_name: str) -> str:
    """
    Get IATA airport code(s) for a city name.
    
    This function searches for airports by city or airport name
    and returns the IATA codes.
    
    Args:
        city_name: Name of the city or airport to search for
    
    Returns:
        str: A formatted string with airport codes and names,
             or an error message if the search fails.
    
    Example:
        >>> get_airport_code("Paris")
        "Airports for 'Paris':
        1. CDG - Charles de Gaulle Airport
        2. ORY - Orly Airport"
    """
    try:
        client = get_amadeus_client()
        
        # Search for airports
        response = client.reference_data.locations.get(
            keyword=city_name,
            subType='AIRPORT'
        )
        
        if not response.data:
            return f"No airports found for '{city_name}'."
        
        # Format results
        results = []
        for idx, location in enumerate(response.data[:5], 1):  # Top 5 results
            iata_code = location.get('iataCode', 'N/A')
            name = location.get('name', 'N/A')
            city = location.get('address', {}).get('cityName', '')
            country = location.get('address', {}).get('countryName', '')
            
            location_str = f"{city}, {country}" if city and country else ""
            results.append(
                f"{idx}. {iata_code} - {name} {location_str}".strip()
            )
        
        header = f"Airports for '{city_name}':\n"
        return header + "\n".join(results)
        
    except ResponseError as error:
        return f"Amadeus API error: {error.description}"
    except Exception as e:
        return f"Error searching for airports: {str(e)}"
