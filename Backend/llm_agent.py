import os
import requests
import openai  # ✅ updated import
from dotenv import load_dotenv
from crewai import Crew, Agent, Task

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ updated API key setup

VEHICLE_API_URL = "https://98166d4a-3cec-482a-b286-63ad83cd2e19-00-ihgub8c2yv3k.riker.replit.dev/vehicles"


def fetch_vehicle_data():
    try:
        response = requests.get(VEHICLE_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error":
                f"Failed to fetch vehicle data. Status code: {response.status_code}"
            }
    except Exception as e:
        return {"error": str(e)}


def process_query_with_ai(user_query):
    vehicle_data = fetch_vehicle_data()
    if "error" in vehicle_data:
        return f"❌ Error fetching vehicle data: {vehicle_data['error']}"

    prompt = f"""You are VoltAI, a smart car assistant. Analyze the following vehicle telemetry data and respond to the user's query.

User query: {user_query}

Vehicle Data:
{vehicle_data}

Respond in a helpful and concise way, mentioning any alerts or advice based on the values."""

    try:
        chat_completion = openai.chat.completions.create(  # ✅ updated call
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }])
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI Error: {str(e)}"


def process_query_with_crewai(user_query):
    vehicle_data = fetch_vehicle_data()
    if "error" in vehicle_data:
        return f"❌ Error fetching vehicle data: {vehicle_data['error']}"

    data_str = str(vehicle_data)

    # Define CrewAI agents
    safety_agent = Agent(
        role="Vehicle Safety Analyst",
        goal=
        "Identify any critical safety issues from the vehicle telemetry data.",
        backstory=
        "An expert in automotive safety and diagnostics who ensures drivers stay safe on the road.",
        allow_delegation=False)

    maintenance_agent = Agent(
        role="Maintenance Advisor",
        goal=
        "Evaluate maintenance needs and offer preventive care suggestions.",
        backstory=
        "A seasoned auto maintenance specialist who keeps vehicles running in top condition.",
        allow_delegation=False)

    summary_agent = Agent(
        role="Technical Summary Writer",
        goal=
        "Summarize the overall health and highlight action points for the user.",
        backstory=
        "An AI assistant designed to present vehicle insights clearly and concisely for users.",
        allow_delegation=True)

    # Assign tasks to the agents
    task_safety = Task(
        description=
        f"Analyze this data for immediate safety concerns: {data_str}",
        expected_output=
        "A list of safety warnings with severity levels and reasons.",
        agent=safety_agent)

    task_maintenance = Task(
        description=
        f"Analyze this data for maintenance issues or early warnings: {data_str}",
        expected_output=
        "A list of suggested maintenance actions and recommendations.",
        agent=maintenance_agent)

    task_summary = Task(
        description=
        f"Based on this vehicle data and the agents' insights, write a structured report for the user query: '{user_query}'",
        expected_output=
        "A clear summary of vehicle condition, maintenance suggestions, and safety alerts in markdown-style formatting.",
        agent=summary_agent)

    # Crew execution
    crew = Crew(agents=[safety_agent, maintenance_agent, summary_agent],
                tasks=[task_safety, task_maintenance, task_summary],
                verbose=False)

    result = crew.kickoff()
    return result
