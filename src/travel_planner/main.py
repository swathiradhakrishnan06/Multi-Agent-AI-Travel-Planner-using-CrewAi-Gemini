# src/travel_planner/main.py
from dotenv import load_dotenv
load_dotenv()

# keep script mode for local ad-hoc runs
if __name__ == "__main__":
    from travel_planner.crew import crew
    inputs = {
        "origin": "MEL",
        "destination": "BLR",
        "date": "2025-08-01",
        "interests": ["food", "culture", "shopping"],
    }
    result = crew.kickoff(inputs=inputs)
    print(result)
