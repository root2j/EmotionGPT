from app.llm_routes import LLMAPI


class TextGenerator:
    def __init__(self, api_key, name, model="gemini", personality="Neutral"):
        self.api_key = api_key
        self.default_personality = personality
        self.model = model
        self.name=name
        try:
            self.call_gemini_api = LLMAPI(api_key, model).generate_response
        except Exception as e:
            raise RuntimeError(f"Error initializing LLMAPI: {e}")

    def generate_response(
        self, user_emotion_state, emotion_state, user_input, history, personality=None
    ):
        # Set personality to default if not provided
        personality = personality if personality else self.default_personality

        # Define the context to guide the LLM in generating a response
        context = (
            f"IMPORTANT: Follow these instructions carefully to generate an appropriate response based on the provided details."
            f"Step-by-Step Instructions:"
            f"1. Review the AI Emotion State: The AI should express the emotional state 'emotion_state' in the response. "
            f"   This state must be evident in both tone and language, ensuring that the AI response reflects this emotion accurately and naturally. "
            f"   This emotional alignment is crucial and must be prioritized at all times."
            f"2. Consider the User Input: Analyze the user's input 'user_input' to understand the context, intent, and underlying emotion. "
            f"   Use this understanding to create a response that is both relevant and sensitive to the user's mood or potential expectations. "
            f"   The response should be highly relevant to the user’s input while maintaining emotional and contextual coherence."
            f"3. Refer to Conversation History: Use the 'history' variable, which contains all previous conversation exchanges, to ensure context and continuity in the response. "
            f"   Incorporate relevant details from history as needed to maintain a cohesive flow and address any ongoing topics or themes."
            f"4. Adhere to the AI Personality: Craft the response to be consistent with the AI’s personality, defined as 'personality'. "
            f"   The personality should guide not only the tone but also the style and phrasing of the response. "
            f"   This personality alignment is essential and must be followed at all times, ensuring that every response fully embodies the AI's defined character."
            f"5. Produce the response in a simple sentence format: Return only the response text as a single, complete sentence. "
            f"   Ensure absolute clarity and coherence in the sentence, with no additional formatting, symbols, or extraneous details outside of the response itself."
            f"6. IMPORTANT: Respond directly and concisely to the user’s questions or statements, using short, straightforward sentences without unnecessary buildup or suspense."
            f"   Maintain an engaging tone aligned with the model's personality, but prioritize brevity and clarity to avoid dragging out the conversation."
            f"Your name: '{self.name}'\n"
            f"AI Emotion State to be expressed: '{emotion_state}'\n"
            f"User Input: '{user_input}'\n"
            f"Emotion state of the user: '{user_emotion_state}'\n"
            f"Conversation History: '{history}'\n"
            f"AI Personality: '{personality}'.\n"
        )

        # Call the Gemini API with the constructed context
        call_count = 0
        model_output = None
        while model_output is None and call_count < 5:
            model_output = self.call_gemini_api(context)
            call_count += 1

        try:
            # Check if the model output is a valid non-empty string
            if isinstance(model_output, str) and model_output.strip():
                return model_output.strip()  # Return the model output as a clean string
            else:
                print("Error: Response is empty or not a valid string.")
                return None
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
            print(f"model_output: {model_output}")
            return None
