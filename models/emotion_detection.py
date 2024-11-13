import json
from typing import Optional, Tuple
from app.llm_routes import LLMAPI


class EmotionDetection:
    def __init__(
        self, 
        api_key: str, 
        custom_instruction: Optional[str] = None, 
        personality: Optional[str] = None, 
        model: str = "gemini"
    ) -> None:
        """
        Initialize the EmotionDetection class.

        Args:
            api_key (str): The API key for accessing the Gemini LLM.
            custom_instruction (Optional[str]): Custom instruction for emotion detection.
            personality (Optional[str]): Personality of the model.
            model (str): Model to use for the LLM. Defaults to "gemini".
        """
        self.api_key = api_key
        self.history = ""
        self.custom_instruction = custom_instruction
        self.personality = personality
        try:
            self.call_gemini_api = LLMAPI(api_key, model).generate_response
        except Exception as e:
            raise RuntimeError(f"Error initializing LLMAPI: {e}")

    def detect_emotion(
        self, 
        text: str, 
        history: str = "", 
        custom_instruction: Optional[str] = None, 
        personality: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Detect the user's and model's emotional states.

        Args:
            text (str): The latest user input text.
            history (str): The conversation history.
            custom_instruction (Optional[str]): Custom instruction for analysis.
            personality (Optional[str]): Personality of the model.

        Returns:
            Tuple[Optional[str], Optional[str]]: Detected user and model emotions.
        """
        response = self.analyze_text(text, history, custom_instruction, personality)
        if response:
            try:
                response_json = json.loads(response)
                user_emotion = response_json.get("user_emotion")
                model_emotion = response_json.get("model_emotion")
                return user_emotion, model_emotion
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON response from Gemini LLM.")
                return None, None
        else:
            return None, None

    def analyze_text(
        self, 
        text: str, 
        history: str, 
        custom_instruction: Optional[str], 
        personality: Optional[str]
    ) -> Optional[str]:
        """
        Analyze the text to detect emotions.

        Args:
            text (str): The latest user input text.
            history (str): The conversation history.
            custom_instruction (Optional[str]): Custom instruction for analysis.
            personality (Optional[str]): Personality of the model.

        Returns:
            Optional[str]: JSON formatted string with detected emotions.
        """
        context = (
            f"IMPORTANT: You must follow these instructions exactly and return the output **only in JSON format**. "
            f'The JSON structure must be: {{"user_emotion": <detected_emotion>, "model_emotion": <model_response_emotion>}}. '
            f"No other text or formatting should be added outside this JSON structure. "
            f"Step-by-Step Instructions:"
            f"1. First, analyze the entire conversation history in the variable 'history'. Consider that 'history' contains all prior conversation exchanges. "
            f"   You must read through this complete history, understanding both explicit and implicit emotional cues provided by the user. "
            f"   Use this context to interpret shifts, consistencies, or nuances in user emotions. At every step, remember that the instruction must be adhered to precisely. "
            f"2. Detect the user's current emotional state by considering both the latest message and any overarching themes across the conversation history. "
            f"   The detected emotion should be as descriptive as possible, using more than one word if necessary (e.g., 'mild frustration with curiosity' or 'content but slightly skeptical'). "
            f"   This descriptive accuracy is preferred and essential for capturing complex emotional states. Follow this instruction at all costs. "
            f"3. Determine the appropriate emotional tone for the model's response (model_emotion) based on the user’s detected emotion while strictly adhering to the model's specified personality. "
            f"   The personality of the model, as defined in 'personality', must guide the emotional tone of each response. "
            f"   The model must consistently reflect this personality trait in its responses, without deviation. Following this personality is essential at all times, ensuring that the response aligns with both the detected user emotion and the model's personality. "
            f'4. Return the detected emotions in the JSON format: {{"user_emotion": <detected_emotion>, "model_emotion": <model_response_emotion>}}. '
            f"   Ensure absolute accuracy in following this structure without any additional text or formatting outside the JSON structure. The instruction must be followed precisely."
            f"Here is the most recent text sent by the user to analyze: '{text}'."
            f"Instruction for Analysis: '{custom_instruction if custom_instruction is not None else self.custom_instruction}'. "
            f"Analyze the following conversation history with absolute adherence to this instruction: '{history}'. "
            f"Maintain the specified personality consistently throughout the analysis: '{personality if personality is not None else self.personality}'."
        ).strip()

        output = None
        call_limit = 0
        while output is None and call_limit < 5:
            output = self.call_gemini_api(context)
            call_limit += 1
        return output

