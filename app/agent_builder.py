# agent_builder.py
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from app.agent_instructions import get_agent_instructions
from modules.flight_module import FlightModule
from modules.meal_order_module import MealOrderModule

load_dotenv()
MODAL_GEMINI_2_0_FLASH = os.environ["GOOGLE_GENAI_MODAL"]

def build_root_agent():
    flight_module = FlightModule()
    meal_order_module = MealOrderModule()

    greeting_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="greeting_agent",
        instruction=get_agent_instructions("greeting_agent"),
        description="Handles greetings",
        tools=[say_hello]
    )

    farewell_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="farewell_agent",
        instruction=get_agent_instructions("farewell_agent"),
        description="Handles farewells",
        tools=[say_goodbye]
    )

    flight_info_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="flight_info_agent",
        instruction=get_agent_instructions("flight_info_agent"),
        description="Handles flight queries",
        tools=[flight_module.get_flight_details]
    )

    meal_order_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="meal_order_info_agent",
        instruction=get_agent_instructions("meal_order_info_agent"),
        description="Handles meal order count queries",
        tools=[meal_order_module.get_meal_order_details]
    )

    meal_issue_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="meal_issue_agent",
        instruction=get_agent_instructions("meal_issue_agent"),
        description="This agent handles user queries related to meal ordering issues. It orchestrates responses by first retrieving flight information and then fetching meal order details, applying strict business rules to determine meal order eligibility.",
    )

    main_multi_tool_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="main_multi_tool_agent",
        instruction=get_agent_instructions("main_multi_tool_agent"),
        description="Handles catering modules",
        sub_agents=[flight_info_agent, meal_order_agent, meal_issue_agent]
    )

    root_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="catering_agent_v2",
        instruction=get_agent_instructions("catering_agent_v2", 
            user_name="John Doe",
            user_preference_language="English",
            user_accessiblity_station="DXB",
            user_role="caterer",
            user_preference_currency="USD"
        ),
        description="Root agent delegating to greeting/farewell/catering agents",
        sub_agents=[greeting_agent, farewell_agent, main_multi_tool_agent]
    )

    return root_agent

# Local tools
from typing import Optional

def say_hello(name: Optional[str] = None) -> str:
    return f"Hello, {name}!" if name else "Hello there!"

def say_goodbye() -> str:
    return "Goodbye! Have a great day."
