# EmotionGPT API Documentation

## Introduction

EmotionGPT offers a RESTful API that enables users to create, interact with, and end chat sessions. Each session supports customized chatbot configurations, including personality and instructions, and allows the bot to maintain conversation history.

---

## Base URL

The API is hosted at:  
**For Local Development:** `http://127.0.0.1:5000`

---

## Endpoints

### 1. **Create Session**

- **URL:** `/create_session`
- **Method:** `POST`
- **Description:** Initializes a new chat session with a chatbot configured to a specific personality and model.

#### Request Body Parameters

- `api_key` (string, required): The API key for authorization.
- `name` (string, required): The name assigned to the chatbot for this session.
- `personality` (string, required): The personality of the chatbot.
- `custom_instruction` (string, optional): Custom instruction the chatbot should follow for generating responses.
- `client_maintains_history` (boolean, optional): Whether the client will handle conversation history (default: `false`).
- `model` (string, required): The model ID to use for generating responses.

#### Example Request

```json
POST /create_session
{
  "api_key": "your_api_key",
  "name": "EmotionBot",
  "personality": "friendly",
  "custom_instruction": "Speak in a comforting tone",
  "client_maintains_history": true,
  "model": "gemini"
}
```

#### Example Response

```json
{
  "session_id": "unique_session_id"
}
```

- **Status Codes:**
  - `200 OK` - Session created successfully.
  - `400 Bad Request` - Missing required parameters or session creation error.

---

### 2. **Send Message**

- **URL:** `/send_message`
- **Method:** `POST`
- **Description:** Sends a user message to the chatbot and returns the chatbot's response with current user emotion state and model emotion state based on its current state and the provided history (if applicable).

#### Request Body Parameters

- `session_id` (string, required): The unique identifier of the chat session.
- `message` (string, required): The user’s message to send to the chatbot.
- `history` (array, optional): A string of previous messages in the conversation if the client maintains history.

#### Example Request

```json
POST /send_message
{
  "session_id": "unique_session_id",
  "message": "How are you feeling today?",
  "history": [
    {"user": "Hello!"},
    {"bot": "Hi there! How can I assist you?"}
  ]
}
```

#### Example Response

```json
{
  "response": ["I'm here to help you! Tell me more about how you're feeling.","user_emotion_state","model_emotion_state"]
}
```

- **Status Codes:**
  - `200 OK` - Response generated successfully.
  - `400 Bad Request` - Missing required parameters or invalid session ID.

---

### 3. **End Session**

- **URL:** `/end_session`
- **Method:** `POST`
- **Description:** Ends a chat session, clearing session data to prevent further interactions.

#### Request Body Parameters

- `session_id` (string, required): The unique identifier of the chat session to end.

#### Example Request

```json
POST /end_session
{
  "session_id": "unique_session_id"
}
```

#### Example Response

```json
{
  "message": "Session ended successfully"
}
```

- **Status Codes:**
  - `200 OK` - Session ended successfully.
  - `400 Bad Request` - Invalid session ID.

---

## Error Codes

- **400 Bad Request:** Indicates missing parameters or invalid data in the request.
- **200 OK:** Successful completion of the request.

---

## Additional Notes

- Ensure that each session starts with a `POST` request to `/create_session` to obtain a unique `session_id`.
- Store the `session_id` to maintain the session and interact with the chatbot using `/send_message`.
- When the conversation is over, end the session with a `POST` request to `/end_session` to release resources.
