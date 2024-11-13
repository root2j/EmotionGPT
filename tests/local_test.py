from models.emotion_detection import EmotionDetection
from models.state_management import EmotionState, ConversationHistory
from models.text_generation import TextGenerator

def main():
    key = "AIzaSyCsas4FZb-kFf8IIBVMtCbvEguClTP0ktw"
    Name = "EmotionGPT"
    # Initialize modules
    emotion_detector = EmotionDetection(
        api_key=key, custom_instruction="Your name is " + Name
    )
    emotion_state = EmotionState()
    text_generator = TextGenerator(api_key=key)
    conversation_history = ConversationHistory()

    # Loop to simulate interaction
    while True:
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() == "exit":
            print("Exiting conversation.")
            break

        # Step 1: Detect emotion
        detected_emotion_user,detected_emotion_model = emotion_detector.detect_emotion(user_input, history=conversation_history.get_history())

        # Step 2: Update emotion state
        emotion_state.update_state(detected_emotion_model, detected_emotion_user)

        # Step 3: Generate response based on updated state
        current_emotion_model_state, current_emotion_user_state = emotion_state.get_state()
        response = text_generator.generate_response(
            current_emotion_user_state,
            current_emotion_model_state,
            user_input,
            history=conversation_history.get_history(),
            personality="Energetic, enthusiastic, persuasive, confident, charming, relentless, upbeat, optimistic, convincing, outgoing, dynamic, talkative, engaging, witty, friendly, smooth-talking, assertive, spontaneous, charismatic, ambitious"
        )

        # Step 4: Update conversation history
        conversation_history.update_history(
            "\nUser:" + user_input + "\n" + Name + ":" + response[0] if response[0] else ""
        )

        print(f"{Name}: {response[0]}")
        # print(f"Conversation History: {conversation_history.get_history()}")


if __name__ == "__main__":
    main()
