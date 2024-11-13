from models.emotion_detection import EmotionDetection

# Replace 'YOUR_API_KEY' with your actual Gemini API key
emotion_detector = EmotionDetection(api_key='AIzaSyCsas4FZb-kFf8IIBVMtCbvEguClTP0ktw')

# Basic emotion detection using keywords
emotion = emotion_detector.detect_emotion("I'm feeling joyful!")
print(f"Detected emotion: {emotion}")

# Advanced LLM-based emotion analysis with custom context and personality
# response = emotion_detector.analyze_text_with_gemini(
#     text="I had a fantastic day!",
#     history="",
#     custom_instruction="Detect the emotion expressed by the user from the text and what your emotion response should be according to your personality and the conversation history.",
#     personality="empathetic"
# )

# if response:
#     print("Gemini LLM Response:", response)
