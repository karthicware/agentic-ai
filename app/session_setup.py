# session_setup.py
import uuid
from google.adk.sessions import InMemorySessionService

APP_NAME = "catering_management_system"
USER_ID_STATEFUL = "EMP123"
SESSION_ID_STATEFUL = str(uuid.uuid4())

state_context = {
    "user_name": "John Doe",
    "user_preference_language": "English",
    "user_preference_currency": "USD",
    "user_role": "caterer",
    "user_accessibility": {
        "station": "DXB, MAA"
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
    return session_service, session, APP_NAME, USER_ID_STATEFUL, SESSION_ID_STATEFUL
