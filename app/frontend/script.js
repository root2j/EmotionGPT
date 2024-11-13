const apiUrl = "http://127.0.0.1:5000";
let sessionId = "";
let apiKey = "API-KEY"; // Replace with a valid API key
let history = [];

// Emotion-to-emoji mapping
const emotionToEmoji = {
  happy: "😊",
sad: "😢",
angry: "😠",
neutral: "😐",
surprised: "😲",
confused: "😕",
excited: "😄",
bored: "😴",
relieved: "😌",
nervous: "😬",
scared: "😨",
disappointed: "😞",
hopeful: "🤞",
amused: "😆",
embarrassed: "😳",
ashamed: "😳",
proud: "😌",
grateful: "🙏",
determined: "💪",
frustrated: "😣",
guilty: "😔",
inspired: "🌟",
lonely: "😔",
jealous: "😒",
annoyed: "😤",
optimistic: "😁",
overwhelmed: "😩",
loved: "😍",
curious: "🤔",
content: "😌",
playful: "😜",
satisfied: "😋",
sympathetic: "🤗",
affectionate: "🥰",
fearful: "😱",
disgusted: "🤢",
confident: "😎",
embittered: "😖",
skeptical: "🤨",
thoughtful: "🤔",
shocked: "😱",
melancholic: "😔",
insecure: "😟",
stressed: "😫",
apologetic: "🙏",
peaceful: "😇",
apathetic: "😶",
nostalgic: "🥲",
exhausted: "😫",
motivated: "🔥",
mischievous: "😏",
regretful: "😔",
awed: "😮",
craving: "😋",
heartbroken: "💔",
sarcastic: "😜",
  // Additional emotions can be added dynamically
};

// Function to initialize a new session with user-defined parameters
async function createSession() {
  // Retrieve user-defined parameters
  const name = document.getElementById("botName").value || "EmotionBot";
  const personality =
    document.getElementById("personality").value || "friendly";
  // const emotionSet = document.getElementById('emotionSet').value.split(',').map(e => e.trim());
  const model = document.getElementById("model").value || "gemini";

  // Set custom instruction based on the selected emotions
  const customInstruction = `Please respond by expressing an emotion using only one of the options listed in ${Object.keys(emotionToEmoji)}. Avoid adding any additional words or explanations. Ensure your response is clear, unambiguous, and directly represents the intended emotion using a single emoji from the provided set.`;

  // Create session API call
  const response = await fetch(`${apiUrl}/create_session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      name,
      personality,
      client_maintains_history: true,
      custom_instruction: customInstruction,
      model,
    }),
  });

  const data = await response.json();
  sessionId = data.session_id;
  if (!sessionId) alert("Error creating session");

  document.querySelector(".config-form").style.display = "none";
  document.querySelector(".chat-interface").style.display = "flex";

  // // Dynamically update emotion-to-emoji mapping based on user-defined emotions
  // emotionSet.forEach(emotion => {
  //   if (!emotionToEmoji[emotion]) emotionToEmoji[emotion] = '😐';  // Default to neutral emoji if not defined
  // });
}

/// Function to send a message
async function sendMessage() {
  const message = document.getElementById("userMessage").value;
  if (!message || !sessionId) return;

  // Display user's message
  displayMessage(message, "user");
  document.getElementById("userMessage").value = "";

  // Send message to API
  history.push({ user: message });
  const response = await fetch(`${apiUrl}/send_message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message, history }),
  });

  const data = await response.json();
  const [botResponse, userEmotion, modelEmotion] = data.response;

  // Display bot's response
  displayMessage(botResponse, "bot");
  history.push({ bot: botResponse });

  // Update the emoji display for the bot's emotion
  updateEmojiDisplay(modelEmotion);
}

// Function to end session
async function endSession() {
  if (!sessionId) return;

  await fetch(`${apiUrl}/end_session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });

  sessionId = "";
  history = [];
  document.getElementById("chatWindow").innerHTML = "";
  document.getElementById("emojiDisplay").textContent = "😐"; // Reset emoji to neutral
  alert("Session ended");
}

// Utility function to display messages in the chat window
function displayMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.textContent = text;
  document.getElementById("chatWindow").appendChild(messageDiv);
  document.getElementById("chatWindow").scrollTop =
    document.getElementById("chatWindow").scrollHeight;
}

// Utility function to map emotion state to emoji
function getEmojiForEmotion(emotion) {
  return emotionToEmoji[emotion] || "😐"; // Default to neutral if no match
}

// Update the emoji display with the current emotion emoji
function updateEmojiDisplay(emotion) {
  const emoji = getEmojiForEmotion(emotion);
  document.getElementById("emojiDisplay").textContent = emoji;
}
