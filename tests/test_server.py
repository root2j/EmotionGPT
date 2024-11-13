import unittest
import json
from app.server import app  # Adjusting for Flask app in server.py


class TestServer(unittest.TestCase):

    def setUp(self,api_key=None):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.base_url = 'http://127.0.0.1:5000'
        self.api_key = api_key if api_key else "AIzaSyCsas4FZb-kFf8IIBVMtCbvEguClTP0ktw"

    def test_create_session_success(self):
        """Test creating a session with all required fields."""
        payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "personality": "Friendly, outgoing, etc.",
            "custom_instruction": "Your name is AadiManav",
            "model": "gemini",
            "client_maintains_history": True
        }
        response = self.client.post(f"{self.base_url}/create_session", json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('session_id', response_data)

    def test_create_session_missing_fields(self):
        """Test creating a session with missing fields."""
        payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "custom_instruction": "Your name is AadiManav",
            # Missing personality and model
        }
        response = self.client.post(f"{self.base_url}/create_session", json=payload)
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_create_session_invalid_model(self):
        """Test creating a session with an invalid model."""
        payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "personality": "Friendly, outgoing, etc.",
            "custom_instruction": "Your name is AadiManav",
            "model": "invalid_model",  # Invalid model
            "client_maintains_history": True
        }
        response = self.client.post(f"{self.base_url}/create_session", json=payload)
        self.assertEqual(response.status_code, 400)  # Should handle invalid model gracefully

    def test_send_message_with_server_history(self):
        """Test sending a message with server-maintained history."""
        create_payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "personality": "Friendly, outgoing, etc.",
            "custom_instruction": "Your name is AadiManav",
            "model": "gemini",
            "client_maintains_history": False
        }
        create_response = self.client.post(f"{self.base_url}/create_session", json=create_payload)
        session_id = json.loads(create_response.data)['session_id']

        message_payload = {
            "session_id": session_id,
            "message": "Hello, how are you?"
        }
        message_response = self.client.post(f"{self.base_url}/send_message", json=message_payload)
        self.assertEqual(message_response.status_code, 200)
        message_data = json.loads(message_response.data)
        self.assertIn('response', message_data)

    def test_send_message_with_client_history(self):
        """Test sending a message with client-maintained history."""
        create_payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "personality": "Friendly, outgoing, etc.",
            "custom_instruction": "Your name is AadiManav",
            "model": "gemini",
            "client_maintains_history": True
        }
        create_response = self.client.post(f"{self.base_url}/create_session", json=create_payload)
        session_id = json.loads(create_response.data)['session_id']

        message_payload = {
            "session_id": session_id,
            "message": "Hello, how are you?",
            "history": ""  # Client should provide history
        }
        message_response = self.client.post(f"{self.base_url}/send_message", json=message_payload)
        self.assertEqual(message_response.status_code, 200)
        message_data = json.loads(message_response.data)
        self.assertIn('response', message_data)

    def test_end_session(self):
        """Test ending a session."""
        create_payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "personality": "Friendly, outgoing, etc.",
            "custom_instruction": "Your name is AadiManav",
            "model": "gemini",
            "client_maintains_history": True
        }
        create_response = self.client.post(f"{self.base_url}/create_session", json=create_payload)
        session_id = json.loads(create_response.data)['session_id']

        end_payload = {
            "session_id": session_id
        }
        end_response = self.client.post(f"{self.base_url}/end_session", json=end_payload)
        self.assertEqual(end_response.status_code, 200)
        end_data = json.loads(end_response.data)
        self.assertEqual(end_data['message'], "Session ended successfully")

if __name__ == '__main__':
    unittest.main()
