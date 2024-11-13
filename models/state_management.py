# models/state_management.py


class EmotionState:
    def __init__(self):
        self.current_state = "neutral"
        self.acknowledged_user_state = "not yet acknowledged"

    def update_state(self, model_new_emotion, user_new_emotion):
        self.current_state = model_new_emotion
        self.acknowledged_user_state = user_new_emotion
        print(f"[INFO] Internal emotional state updated to: {self.current_state}")
        print(f"[INFO] Acknowledged user state: {self.acknowledged_user_state}")

    def get_state(self):
        return self.current_state, self.acknowledged_user_state


class ConversationHistory:
    def __init__(self):
        self.history = ""

    def update_history(self, thread):
        self.history += thread

    def get_history(self):
        return self.history
