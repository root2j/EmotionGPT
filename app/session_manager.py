import uuid
from models.emotion_detection import EmotionDetection
from models.state_management import EmotionState, ConversationHistory
from models.text_generation import TextGenerator
from typing import Optional, Dict

class SessionManager:
    def __init__(self) -> None:
        self.sessions: Dict[str, Dict[str, Optional[object]]] = {}

    def create_session(
        self, 
        api_key: str, 
        name: str, 
        personality: str, 
        custom_instruction: str, 
        client_maintains_history: bool, 
        model: str = "gemini"
    ) -> Optional[str]:
        """
        Create a new session.

        Args:
            api_key (str): The API key for authentication.
            name (str): The name of the session.
            personality (str): The personality to be used.
            custom_instruction (str): The custom instruction for the session.
            client_maintains_history (bool): Indicates if the client maintains history.
            model (str): The model to use (default is "gemini").

        Returns:
            Optional[str]: The session ID if successful, None otherwise.
        """
        session_id = str(uuid.uuid4())
        
        try:
            emotion_detector = EmotionDetection(
                api_key=api_key, 
                custom_instruction=custom_instruction, 
                personality=personality, 
                model=model
            )
            emotion_state = EmotionState()
            text_generator = TextGenerator(api_key=api_key, name=name, model=model, personality=personality)
            conversation_history = None if client_maintains_history else ConversationHistory()
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

        self.sessions[session_id] = {
            "name": name,
            "emotion_detector": emotion_detector,
            "emotion_state": emotion_state,
            "text_generator": text_generator,
            "conversation_history": conversation_history,
            "personality": personality,
            "client_maintains_history": client_maintains_history,
            "model": model
        }
        return session_id

    def send_message(
        self, 
        session_id: str, 
        user_input: str, 
        user_history: Optional[list] = None
    ) -> Optional[str]:
        """
        Send a message within an existing session.

        Args:
            session_id (str): The session ID.
            user_input (str): The user's input message.
            user_history (Optional[list]): The user's history, if maintained by the client.

        Returns:
            Optional[str]: The generated response, or None if session not found.
        """
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        name = session["name"]
        emotion_detector = session["emotion_detector"]
        emotion_state = session["emotion_state"]
        text_generator = session["text_generator"]
        conversation_history = session["conversation_history"]
        personality = session["personality"]
        client_maintains_history = session["client_maintains_history"]

        history = user_history if client_maintains_history else conversation_history.get_history()
        detected_emotion_user, detected_emotion_model = emotion_detector.detect_emotion(user_input, history)

        emotion_state.update_state(detected_emotion_model, detected_emotion_user)

        current_emotion_model_state, current_emotion_user_state = emotion_state.get_state()
        response = text_generator.generate_response(
            current_emotion_user_state,
            current_emotion_model_state,
            user_input,
            history,
            personality
        )

        if not client_maintains_history and conversation_history:
            conversation_history.update_history(f"\nUser: {user_input}\n{name}: {response}")

        return [response, detected_emotion_user, detected_emotion_model]
    
    def end_session(self, session_id: str) -> bool:
        """
        End a session.

        Args:
            session_id (str): The session ID to end.

        Returns:
            bool: True if the session was successfully ended, False otherwise.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
