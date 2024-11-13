import unittest
import json
import time
from app.server import app  # Adjusting for Flask app in server.py


class TestServerTimeComplexity(unittest.TestCase):

    def setUp(self, api_key=None):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.api_key = api_key if api_key else "AIzaSyCsas4FZb-kFf8IIBVMtCbvEguClTP0ktw"

    def _create_session(self):
        payload = {
            "api_key": self.api_key,
            "name": "AadiManav",
            "personality": "Friendly, outgoing, etc.",
            "custom_instruction": "Your name is AadiManav",
            "model": "gemini",
            "client_maintains_history": True,
        }
        response = self.client.post("/create_session", json=payload)
        return json.loads(response.data)["session_id"]

    def test_create_session_time_complexity(self):
        """Test create_session scalability with increasing session requests."""
        times = []
        for i in range(1, 31, 10):  # Increase number of sessions
            start_time = time.time()
            for _ in range(i):
                self._create_session()
            end_time = time.time()
            avg_time = (end_time - start_time) / i
            times.append((i, avg_time))
            print(
                f"Average time to create session for {i} sessions: {avg_time:.6f} seconds"
            )

        # Optional: analyze times list to check if time complexity appears linear, quadratic, etc.

    def test_send_message_time_complexity(self):
        """Test send_message scalability with increasing messages."""
        session_id = self._create_session()
        times = []
        message_payload = {"session_id": session_id, "message": "I am Very angry!"}
        for i in range(1, 31, 10):  # Increase number of messages
            start_time = time.time()
            for _ in range(i):
                # self.client.post("/send_message", json=message_payload)
                response = self.client.post("/send_message", json=message_payload)
                print(response.data)
            end_time = time.time()
            avg_time = (end_time - start_time) / i
            times.append((i, avg_time))
            print(f"Average time to send {i} messages: {avg_time:.6f} seconds")

        # Optional: analyze times list to check if time complexity appears linear, quadratic, etc.

    def test_end_session_time_complexity(self):
        """Test end_session scalability with increasing session terminations."""
        times = []
        session_ids = [self._create_session() for _ in range(10)]
        for i in range(1, 31, 10):  # Increase number of sessions to end
            start_time = time.time()
            for session_id in session_ids[:i]:
                end_payload = {"session_id": session_id}
                self.client.post("/end_session", json=end_payload)
            end_time = time.time()
            avg_time = (end_time - start_time) / i
            times.append((i, avg_time))
            print(f"Average time to end {i} sessions: {avg_time:.6f} seconds")

        # Optional: analyze times list to check if time complexity appears linear, quadratic, etc.


if __name__ == "__main__":
    unittest.main()
