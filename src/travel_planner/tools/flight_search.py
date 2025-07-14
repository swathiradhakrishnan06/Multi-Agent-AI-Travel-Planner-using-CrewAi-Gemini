# src/travel_planner/tools/flight_search.py
import os
from amadeus import Client, ResponseError
from crewai.tools import BaseTool
from typing import List, Dict, Any
from pydantic import PrivateAttr

class FlightSearch(BaseTool):
    name: str = "flight_search"
    description: str = "Search for flights using Amadeus API"
    _client: Client = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = Client(
            client_id=os.getenv("AMADEUS_CLIENT_ID"),
            client_secret=os.getenv("AMADEUS_CLIENT_SECRET"),
        )

    def _run(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        try:
            res = self._client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=date,
                adults=1,
                max=10
            )
            return res.data or []
        except ResponseError as e:
            print("Amadeus error:", e)
            return []
