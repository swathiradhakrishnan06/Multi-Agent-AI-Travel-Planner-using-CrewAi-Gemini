# src/travel_planner/main.py
import os
from dotenv import load_dotenv
from travel_planner.crew import crew

load_dotenv()

if __name__ == "__main__":
    inputs = {
        "origin": "MEL",
        "destination": "BLR",
        "date": "2025-08-01",
        "interests": ["food", "culture", "shopping"],
    }
    result = crew.kickoff(inputs=inputs)
    print(result)
