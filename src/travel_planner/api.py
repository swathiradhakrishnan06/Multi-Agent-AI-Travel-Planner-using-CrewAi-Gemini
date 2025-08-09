# src/travel_planner/api.py
import logging
from typing import List, Optional, Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from starlette.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from travel_planner.crew import crew  # your existing crew object
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("travel_planner_api")

app = FastAPI(
    title="Multi-Agent AI Travel Planner",
    description="Plan meaningful journeys (not just cheapest flights) powered by CrewAI + Gemini",
    version="0.1.0",
)


class TripRequest(BaseModel):
    origin: str = Field(..., min_length=3, max_length=5, description="Origin IATA code, e.g., MEL")
    destination: str = Field(..., min_length=3, max_length=5, description="Destination IATA code, e.g., BLR")
    date: str = Field(..., description="Departure date in YYYY-MM-DD format")
    interests: Optional[List[str]] = Field(default_factory=list, description="List of user interests, e.g., ['food','culture']")
    max_price: Optional[float] = Field(None, ge=0, description="Optional max price in EUR")
    preferred_airlines: Optional[List[str]] = Field(default_factory=list, description="Optional airline preferences")

    @validator("origin", "destination")
    def uppercase_iata(cls, v: str) -> str:
        return v.strip().upper()


class TripResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]]


@app.get("/healthz", tags=["health"])
def healthz():
    """Simple healthcheck endpoint."""
    return {"status": "ok"}


@app.post("/plan-trip", response_model=TripResponse, tags=["trip"])
async def plan_trip(payload: TripRequest):
    """
    Plan a trip — runs the crew kickoff which orchestrates flight search, evaluation, and itinerary generation.
    The crew.kickoff is run in a threadpool to avoid blocking the event loop.
    """
    inputs = {
        "origin": payload.origin,
        "destination": payload.destination,
        "date": payload.date,
        "interests": payload.interests or [],
        "max_price": payload.max_price,
        "preferred_airlines": payload.preferred_airlines or [],
    }

    logger.info("Received plan-trip request: %s -> %s on %s (interests=%s)",
                inputs["origin"], inputs["destination"], inputs["date"], inputs["interests"])

    try:
        # run the crew synchronously in a thread to avoid blocking the event loop
        result = await run_in_threadpool(crew.kickoff, inputs)
    except Exception as exc:
        logger.exception("Error running crew.kickoff: %s", exc)
        # Return a helpful error to the client
        raise HTTPException(status_code=500, detail=f"Internal error while planning trip: {str(exc)}")

    # If crew returns a string, wrap it; if it's already dict-like, pass through
    if isinstance(result, str):
        data = {"raw": result}
    else:
        data = result

    return TripResponse(status="success", data=data)
