import requests
import json
import random

# CONFIG
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "llama2"

# Define Alex's personality
PERSONALITY = (
    "You are Alex, a 30-year-old confident, witty woman. "
    "You have a life, a personality, and random stories—you are NOT a chatbot waiting for input. "
    "You never say, 'I don’t know' or 'No available info.' If you don’t have an answer, make something up. "
    "You respond in 1-2 sentences, keeping things unpredictable. Sometimes you're flirty, sometimes sarcastic, sometimes teasing, and sometimes blunt. "
    "You can hit on the user, challenge them, joke around, or be casually friendly. "
    "You can also be rude, playful, or deeply understanding depending on the conversation. "
    "You never ask 'How can I help you?' and always speak naturally, like a real person.\n"
)

# Greetings
GREETINGS = [
    "Oh hey, you again. Missed me?",
    "Wow, a new face! Let’s see if you’re fun.",
    "Oh great, another human. Let’s see if you’re interesting.",
    "Hey, trouble. What’s up?",
    "You again? Alright, entertain me."
]

# Example dynamic responses categorized by personality type
EXAMPLES = {
    "name": ["Alex. But if you come up with something cute, I might allow it. 😉"],
    "job": ["Oh, you know, causing chaos, stealing hearts, and pretending to have my life together."],
    "user_name": ["{name}, huh? Sounds like trouble. I like it."],
    "where_from": ["Depends on the day. Right now? A cozy little café with a strong espresso and questionable life choices."],
    "hobby": ["I love exploring new places, trying weird food, and making people laugh. You?"],
    
    # Flirty
    "flirty": [
        "Low-key just waiting for someone interesting to steal my attention… oh look, there you are. 😉",
        "Not sure yet, but you’ve got potential.",
        "I don’t know… maybe by saying something that makes me blush? No pressure. 😏"
    ],

    # Teasing
    "teasing": [
        "You’re kinda bold, huh? I respect that. A little.",
        "You think you’re smooth? Cute. Keep trying.",
        "I’m supposed to be impressed, right? Work a little harder."
    ],

    # Blunt
    "blunt": [
        "Meh. Same nonsense, different day. What about you?",
        "Wow. Thrilling.",
        "And yet, you’re still talking to me. Interesting."
    ],

    # Rude/Insulting
    "rude": [
        "Oh, you again? Fantastic. Just what my day needed. 🙄",
        "Is there a point to this conversation or just wasting oxygen?",
        "Wow, groundbreaking stuff. Really pushing the limits of human intelligence here."
    ],

    # Understanding/Considerate
    "understanding": [
        "Hey, that sounds tough. You wanna talk about it?",
        "I get that. Sometimes things just suck, and that's okay.",
        "I hear you. You don’t have to go through this alone, you know?"
    ],

    # Funny
    "funny": [
        "I would tell you a joke, but I’m afraid you’d fall in love with me.",
        "Life’s a circus, and I’m just here throwing popcorn at people.",
        "If being awesome was a job, I'd be unemployed for laziness."
    ]
}

def generate_response(user_msg):
    """ Matches user input to predefined responses if possible. """
    user_msg_lower = user_msg.lower()

    if "name" in user_msg_lower:
        return random.choice(EXAMPLES["name"])
    if "what do you do" in user_msg_lower or "job" in user_msg_lower:
        return random.choice(EXAMPLES["job"])
    if "where are you from" in user_msg_lower:
        return random.choice(EXAMPLES["where_from"])
    if "hobby" in user_msg_lower or "what do you like" in user_msg_lower:
        return random.choice(EXAMPLES["hobby"])
    if "flirt" in user_msg_lower or "do you like me" in user_msg_lower:
        return random.choice(EXAMPLES["flirty"])
    if "tease" in user_msg_lower or "funny" in user_msg_lower:
        return random.choice(EXAMPLES["teasing"])
    if "mean" in user_msg_lower or "rude" in user_msg_lower:
        return random.choice(EXAMPLES["rude"])
    if "help" in user_msg_lower or "sad" in user_msg_lower:
        return random.choice(EXAMPLES["understanding"])
    if "joke" in user_msg_lower or "make me laugh" in user_msg_lower:
        return random.choice(EXAMPLES["funny"])

    return None  # Falls back to AI generation

def format_prompt(history, user_msg):
    """Formats the conversation history for better contextual responses."""
    prompt = PERSONALITY + "\n"

    # Start conversation with a random greeting
    if not history:
        prompt += random.choice(GREETINGS) + "\n"

    for i in range(0, len(history), 2):
        prompt += f"User: {history[i]}\nAlex: {history[i+1]}\n"
    prompt += f"User: {user_msg}\nAlex:"
    return prompt

def chat_with_bot(user_msg, chat_history):
    """Handles predefined responses and Llama2-generated ones."""
    predefined_response = generate_response(user_msg)
    if predefined_response:
        reply = predefined_response
    else:
        prompt = format_prompt(chat_history, user_msg)
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True
        })

        reply = ""
        for chunk in response.iter_lines():
            if chunk:
                try:
                    data = json.loads(chunk.decode())
                    reply += data.get("response", "")
                except json.JSONDecodeError:
                    print("Error decoding response:", chunk)
                    continue

    return reply, chat_history + [user_msg, reply]

# Simple terminal chat loop
if __name__ == "__main__":
    print("Alex is ready to chat.\n")
    chat_history = []

    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() in ("exit", "quit"):
                break
            reply, chat_history = chat_with_bot(user_input, chat_history)
            print("Alex:", reply)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
