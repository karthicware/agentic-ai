# session_setup.py
import uuid
from google.adk.sessions import InMemorySessionService

APP_NAME = "icms" # Intelligent Catering Management System
USER_ID_STATEFUL = "EMP123"
SESSION_ID_STATEFUL = str(uuid.uuid4())

state_context = {
    "user_name": "Natarajan",
    "user_preference_language": "English",
    "user_preference_currency": "AED",
    "user_role": "caterer",
    "user_accessibility": {
        "station": "DXB, MAA, BOM"
    }
}

session_service = InMemorySessionService()

async def setup_session():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL,
        state=state_context
    )
    print(f"Session created: {session.id}")
    return session_service, session, APP_NAME, USER_ID_STATEFUL, SESSION_ID_STATEFUL
