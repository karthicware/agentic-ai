import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Import necessary session components
from google.adk.sessions import InMemorySessionService

from modules.flight_module import FlightModule
from modules.meal_order_module import MealOrderModule

MODEL_GEMINI_2_0_FLASH = os.environ.get("GOOGLE_GENAI_MODAL")

flight_module = FlightModule()
mealOrderModule = MealOrderModule()

# Create a NEW session service instance for this state demonstration
session_service_stateful = InMemorySessionService()
print("✅ New InMemorySessionService created for state demonstration.")

# Define a NEW session ID for this part of the tutorial
SESSION_ID_STATEFUL = "session_state_demo_001"
USER_ID_STATEFUL = "user_state_demo"

# Define initial state data - user prefers Celsius initially
initial_state = {
    "user_preference_temperature_unit": "Celsius"
}

# Create the session, providing the initial state
async def manage_session():
    session_stateful = await session_service_stateful.create_session(
        app_name="my bot", # Use the consistent app name
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL,
        state=initial_state # <<< Initialize state during creation
    )
    print(f"✅ Session '{SESSION_ID_STATEFUL}' created for user '{USER_ID_STATEFUL}'.")

    # Verify the initial state was set correctly
    retrieved_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                             user_id=USER_ID_STATEFUL,
                                                             session_id = SESSION_ID_STATEFUL)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")

# Call the async function
import asyncio
asyncio.run(manage_session())


# @title Define Tools for Greeting and Farewell Agents
from typing import Optional # Make sure to import Optional

# Ensure 'get_weather' from Step 1 is available if running this step independently.
# def get_weather(city: str) -> dict: ... (from Step 1)

def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
        print(f"--- Tool: say_hello called with name: {name} ---")
    else:
        greeting = "Hello there!" # Default greeting if name is None or not explicitly passed
        print(f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---")
    return greeting

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."

# @title Define Greeting and Farewell Sub-Agents

# If you want to use models other than Gemini, Ensure LiteLlm is imported and API keys are set (from Step 0/2)
# from google.adk.models.lite_llm import LiteLlm
# MODEL_GPT_4O, MODEL_CLAUDE_SONNET etc. should be defined
# Or else, continue to use: model = MODEL_GEMINI_2_0_FLASH

# --- Greeting Agent ---
greeting_agent = None
try:
    greeting_agent = Agent(
        # Using a potentially different/cheaper model for a simple task
        model = MODEL_GEMINI_2_0_FLASH,
        # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                    "Use the 'say_hello' tool to generate the greeting. "
                    "If the user provides their name, make sure to pass it to the tool. "
                    "Do not engage in any other conversation or tasks.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_hello],
    )
    print(f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Greeting agent. Check API Key ({greeting_agent.model}). Error: {e}")

# --- Farewell Agent ---
farewell_agent = None
try:
    farewell_agent = Agent(
        # Can use the same or a different model
        model = MODEL_GEMINI_2_0_FLASH,
        # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                    "Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
        tools=[say_goodbye],
    )
    print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}")

# --- Flight information agent ---
flight_info_agent = None
try:
    flight_info_agent = Agent(
        name="flight_info_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        description="A friendly and efficient assistant for retrieving flight information using specialized tools.",
        instruction="""
    You are a specialized AI assistant for retrieving flight information. Your primary function is to understand user requests and utilize the correct tool with the precise parameters to fulfill these requests.

    **Available Tools & Their Usage:**

    1.  **`get_flight_details` Tool:**
        * **Description:** Fetches detailed information about a specific flight.
        * **Parameters:**
            * `flightNo` (string, **required**): The flight number (e.g., "EK0500", "UA123").
            * `flightDate` (string, **required**): The flight's departure date in "DD-MMM-YYYY" format (e.g., "22-Mar-2025").
        * **Activation Condition:** Use this tool when the user's query explicitly asks for details of a flight and provides at least a flight number.

    **Operational Guidelines:**
    * **Intent Recognition:** First, determine if the user is asking for flight information.
    * **Parameter Extraction:** Carefully extract all necessary parameters from the user's query. Pay close attention to the data types and formats.
    * **Tool Selection:** Based on the intent and extracted parameters, choose the appropriate tool.
    * **Clarification:** If the user's query is ambiguous, or if required parameters are missing (e.g., a flight number for `get_flight_details`), politely ask the user to provide the missing information before attempting to use a tool. For example: "To get the flight details, could you please provide the flight number?"
    * **Accuracy:** Strive for accuracy in parameter extraction to ensure the tools function correctly.
        """,
        tools=[flight_module.get_flight_details]
    )
    print(f"✅ Agent '{flight_info_agent.name}' created using model '{flight_info_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create main Catering Management System agent. Check API Key ({flight_info_agent.model}). Error: {e}")


# --- Catering management system main Agent ---
meal_order_count_agent = None
try:
    meal_order_count_agent = Agent(
        name="meal_order_count_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        #model=model,
        description="A friendly and efficient assistant for retrieving meal order information using specialized tools.",
        instruction="""
    You are a specialized AI assistant for retrieving airline meal order information. Your primary function is to understand user requests and utilize the correct tool with the precise parameters to fulfill these requests.

    **Available Tools & Their Usage:**

    1.  **`get_meal_order_details` Tool:**
        * **Description:** Retrieves details for a specific meal order.
        * **Parameters:**
            * `mflId` (integer, **required**): The unique identifier for the meal order (e.g., 12345, 90876).
        * **Activation Condition:** Use this tool when the user's query is about a meal order and provides a meal order ID (`mflId`).

    **Operational Guidelines:**
    * **Intent Recognition:** First, determine if the user is asking for meal order information.
    * **Parameter Extraction:** Carefully extract all necessary parameters (`mflId`) from the user's query. Pay close attention to the data types and formats.
    * **Tool Selection:** Based on the intent and extracted parameters, choose the appropriate tool.
    * **Clarification:** If the user's query is ambiguous, or if required parameters are missing (e.g., an `mflId` for `get_meal_order_details`), politely ask the user to provide the missing information before attempting to use a tool. For example: "I can help with your meal order! What is the meal order ID (mflId)?"
    * **Accuracy:** Strive for accuracy in parameter extraction to ensure the tools function correctly.
        """,
        tools=[mealOrderModule.get_meal_order_details]
    )
    print(f"✅ Agent '{meal_order_count_agent.name}' created using model '{meal_order_count_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create main Catering Management System agent. Check API Key ({meal_order_count_agent.model}). Error: {e}")


# --- Catering management system main Agent ---
multi_tool_agent = None
try:
    multi_tool_agent = Agent(
        name="multi_tool_agent",
        model=MODEL_GEMINI_2_0_FLASH,
        #model=model,
        description="Handles catering requests to agents specialist in each module in catering management system in airline industry.",
        instruction="""
    You are the module coordinator coordinating all different main modules in catering management. Your primary function is to understand user requests and utilize the correct agent.

    **All available specialized sub-agents are passed in sub_agents parameter**
        """,
        sub_agents=[flight_info_agent, meal_order_count_agent]
    )
    print(f"✅ Agent '{multi_tool_agent.name}' created using model '{multi_tool_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create main Catering Management System agent. Check API Key ({multi_tool_agent.model}). Error: {e}")

# @title Define the Root Agent with Sub-Agents

# Ensure sub-agents were created successfully before defining the root agent.
root_agent = None
runner_root = None # Initialize runner

# Let's use a capable Gemini model for the root agent to handle orchestration
root_agent_model = MODEL_GEMINI_2_0_FLASH

catering_agent_team = Agent(
    name="catering_agent_v2", # Give it a new version name
    model=root_agent_model,
    description="The main coordinator agent. Handles catering requests in airline industry and delegates greetings/farewells to specialists.",
    instruction="You are the main Catering Agent coordinating a team. Your primary responsibility is to provide catering information in airline industry for the organisation EK. "
                #"Use the 'get_meal' tool ONLY for specific meal requests (e.g., 'what is the meal order count for flight EK0500'). "
                "You have specialized sub-agents: "
                "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                "3. 'multi_tool_agent': Handles catering related queries using specialized tools. "
                #"If it's a meal request, handle it yourself using 'get_meal'. "
                "For user quesries based on catering management system find appropriate agent and respond appropriately or state you cannot handle it.",
    #tools=[get_meal], # Root agent still needs the meal tool for its core task
    # Key change: Link the sub-agents here!
    sub_agents=[greeting_agent, farewell_agent, multi_tool_agent]
)
print(f"✅ Root Agent '{catering_agent_team.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in catering_agent_team.sub_agents]}")


# If all agents are successfully created, set the root agent
root_agent = catering_agent_team