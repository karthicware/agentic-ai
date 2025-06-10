# app.py
import asyncio
from app.session_setup import setup_session
from app.root_agent import root_agent


from google.adk.runners import Runner
from google.genai import types

async def main():
    session_service_stateful, _, APP_NAME, USER_ID, SESSION_ID = await setup_session()

    print(f"✅ Session '{SESSION_ID}' created for user '{USER_ID}'.")

    # Verify the initial state was set correctly
    retrieved_session = await session_service_stateful.get_session(app_name=APP_NAME,
                                                             user_id=USER_ID,
                                                             session_id = SESSION_ID)
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")

    runner = Runner(
        agent=root_agent,
        session_service=session_service_stateful,
        app_name=APP_NAME,
    )

    user_query = types.Content(
        role="user",
        parts=[types.Part(text="Hi there!")]
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_query
    ):
        if event.is_final_response():
            print("Final response:", event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
