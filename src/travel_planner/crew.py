import os
from crewai import Agent, Task, Crew, LLM
from .tools.flight_search import FlightSearch
from .tools.stopover_evaluator import StopoverEvaluator
from .tools.local_guide_tools import SerperApiToolWrapper, ScrapeWebsiteToolWrapper

# Read your API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCAKt9P9yjOtTqQMJc2VIyu03GydCq3W2M")

# Use Gemini 1.5 Flash model (faster, different rate limits)
gemini_llm = LLM(
    model='gemini/gemini-1.5-flash',
    api_key=gemini_api_key,
    temperature=0.0  # Lower temperature for more consistent results
)

# Instantiate tools
flight_tool = FlightSearch()
evaluator_tool = StopoverEvaluator()
search_tool = SerperApiToolWrapper()
web_tool = ScrapeWebsiteToolWrapper()

# Create agents
flight_planner = Agent(
    role='Flight Planner',
    goal='Find direct and one‑stop flight offers using Amadeus',
    backstory='An expert flight planner with years of experience finding the best routes and deals.',
    tools=[flight_tool],
    llm=gemini_llm,
    verbose=True
)

route_evaluator = Agent(
    role='Route Evaluator',
    goal='Rank flight options by cost and stopover experience value',
    backstory='A travel expert who knows how to balance cost with experience quality.',
    tools=[evaluator_tool],
    llm=gemini_llm,
    verbose=True
)

local_guide = Agent(
    role='Local Guide',
    goal='Generate a 1–2 day itinerary in the stopover city using web search and scraping',
    backstory='A local travel guide who knows the best attractions and activities in cities worldwide.',
    tools=[search_tool, web_tool],
    llm=gemini_llm,
    verbose=True
)

# Define tasks
search_flights = Task(
    description='Given {origin}, {destination}, {date}, retrieve flight offers (direct & 1‑stop).',
    expected_output='A list of flight offers with prices and stopover information.',
    agent=flight_planner
)

evaluate_routes = Task(
    description='From search_flights output, rank routes by total price minus an experience bonus, then select the top two.',
    expected_output='The top two ranked flight routes with justification.',
    agent=route_evaluator
)

plan_itinerary = Task(
    description='For each chosen route with a stopover, produce a short 1–2 day itinerary in the stopover city, tailored to {interests}.',
    expected_output='Detailed itineraries for each stopover city.',
    agent=local_guide
)

# Assemble the crew
crew = Crew(
    agents=[flight_planner, route_evaluator, local_guide],
    tasks=[search_flights, evaluate_routes, plan_itinerary],
    verbose=True
)
