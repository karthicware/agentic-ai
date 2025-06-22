# agent_builder.py
import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from app.agent_instructions import get_agent_instructions
from modules.flight_module import FlightModule
from modules.meal_order_module import MealOrderModule
from modules.stock_count_module import StockCountModule
from modules.erp_module import ERPModule
from modules.export_excel_module import ExportTextModule
from modules.knowledge_module import KnowledgeModule

load_dotenv()
MODAL_GEMINI_2_0_FLASH = os.environ["GOOGLE_GENAI_MODAL"]

def build_root_agent():
    flight_module = FlightModule()
    meal_order_module = MealOrderModule()
    stock_count_module = StockCountModule()
    erp_module = ERPModule()
    export_text_module = ExportTextModule()
    knowledge_module = KnowledgeModule()

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

    stock_count_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="stock_count_agent",
        instruction=get_agent_instructions("stock_count_agent"),
        description="Handles stock count queries",
        tools=[stock_count_module.get_stock_count_details]
    )

    erp_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="erp_agent",
        instruction=get_agent_instructions("erp_agent"),
        description="Handles ERP data queries",
        tools=[erp_module.get_erp_details]
    )

    export_text_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="export_text_agent",
        instruction=get_agent_instructions("export_text_agent"),
        description="Handles text file export functionality",
        tools=[export_text_module.export_to_text, export_text_module.export_stock_count_to_text, export_text_module.export_pre_approval_data]
    )

    stock_count_reconciliation_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="stock_count_reconciliation_agent",
        instruction=get_agent_instructions("stock_count_reconciliation_agent"),
        description="Handles stock count and ERP data comparison and reconciliation",
        tools=[]
    )

    post_approval_export_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="post_approval_export_agent",
        instruction=get_agent_instructions("post_approval_export_agent"),
        description="Exports ERP data to post-approval file if transaction is approved",
        tools=[export_text_module.export_post_approval_data]
    )

    knowledge_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="knowledge_agent",
        instruction=get_agent_instructions("knowledge_agent"),
        description="Handles detailed knowledge queries by searching the vector database and providing comprehensive answers",
        tools=[knowledge_module.get_knowledge_context, knowledge_module.search_specific_topic]
    )

    # --- Create the SequentialAgent ---
    # This agent orchestrates the pipeline by running the sub_agents in order.
    stock_count_approver_agent = SequentialAgent(
        name="stock_count_approver_agent",
        sub_agents=[stock_count_agent, export_text_agent, erp_agent, stock_count_reconciliation_agent, post_approval_export_agent],
        description="Executes a sequence of stock count data retrieval, export, ERP data retrieval, reconciliation, and conditional post-approval export.",
        # The agents will run in the order provided: Stock Count -> Export -> ERP -> Reconciliation -> Post-Approval Export
    )

    main_multi_tool_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="main_multi_tool_agent",
        instruction=get_agent_instructions("main_multi_tool_agent"),
        description="Handles catering modules",
        sub_agents=[flight_info_agent, meal_order_agent, meal_issue_agent, stock_count_approver_agent, knowledge_agent]
    )

    root_agent = Agent(
        model=MODAL_GEMINI_2_0_FLASH,
        name="catering_agent_v2",
        instruction=get_agent_instructions("catering_agent_v2", 
            user_name="Natarajan",
            user_preference_language="English",
            user_accessiblity_station="DXB",
            user_role="caterer",
            user_preference_currency="AED"
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
