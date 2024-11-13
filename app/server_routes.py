from flask import request, jsonify
from app.session_manager import SessionManager
from typing import Optional

# Initialize the session manager
session_manager: SessionManager = SessionManager()

def create_session() -> tuple[dict, int]:
    """
    Create a new chat session.

    Args:
        - api_key (str): The API key to use for the session.
        - name (str): The name of the chatbot.
        - personality (str): The personality of the chatbot.
        - custom_instruction (str): The custom instruction to follow when generating responses.
        - client_maintains_history (bool): Whether the client should maintain the conversation history.
        - model (str): The model to use for generating responses.

    Returns:
        - A JSON response with the session ID if successful, or an error message if not.
        - An HTTP status code indicating success (200) or failure (400).
    """
    data = request.json
    api_key = data.get("api_key")
    name = data.get("name")
    personality = data.get("personality")
    custom_instruction = data.get("custom_instruction", "No custom instruction to follow")
    client_maintains_history = data.get("client_maintains_history", False)
    model = data.get("model")

    if not (api_key and name and personality and model):
        return jsonify({"error": "Missing required parameters"}), 400

    # Pass the model parameter to the session creation function
    session_id = session_manager.create_session(
        api_key, name, personality, custom_instruction, client_maintains_history, model
    )
    if session_id is None:
        return jsonify({"error": "Error creating session"}), 400
    return jsonify({"session_id": session_id}), 200

def send_message() -> tuple[dict, int]:
    """
    Send a message to the chatbot.

    Args:
        - session_id (str): The ID of the chat session.
        - user_input (str): The message to send to the chatbot.
        - user_history (Optional[list]): The conversation history to use when generating a response.

    Returns:
        - A JSON response with the chatbot's response if successful, or an error message if not.
        - An HTTP status code indicating success (200) or failure (400).
    """
    data = request.json
    session_id = data.get("session_id")
    user_input = data.get("message")
    user_history = data.get("history")  # Optional, used if client maintains history
    if not (session_id and user_input):
        return jsonify({"error": "Missing required parameters"}), 400

    response = session_manager.send_message(session_id, user_input, user_history)
    if response:
        return jsonify({"response": response}), 200
    else:
        return jsonify({"error": "Invalid session ID"}), 400

def end_session() -> tuple[dict, int]:
    """
    End a chat session.

    Args:
        - session_id (str): The ID of the chat session.

    Returns:
        - A JSON response with a success message if the session was ended successfully, or an error message if not.
        - An HTTP status code indicating success (200) or failure (400).
    """
    data = request.json
    session_id = data.get("session_id")

    success = session_manager.end_session(session_id)
    if success:
        return jsonify({"message": "Session ended successfully"}), 200
    else:
        return jsonify({"error": "Invalid session ID"}), 400

