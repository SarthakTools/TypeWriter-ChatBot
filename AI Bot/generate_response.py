import numpy as np
import Levenshtein  # Import Levenshtein distance algorithm
import time, re
from textblob import TextBlob

# Define a dictionary of responses based on input keywords
responses = {
    # Basic Greetings
    "namaste": "Namaste to the god inside you, how can I help you today?",
    "hello": "Hi, how can I help you today?",
    "hi": "Namaste! How's it going?",
    "hey": "Hey there! How can I help you?",
    "good morning": "Good morning! How can I make your day better?",
    "good afternoon": "Good afternoon! What can I do for you?",
    "good evening": "Good evening! How can I help you tonight?",
    
    # Common Questions
    "who are you" : "I am Katyayini, a chatbot",
    "how are you": "I'm doing well, thank you! How can I help you?",
    "what's up": "Not much! Just here to help you. How can I help?",
    "how's it going": "It's going great! What can I do for you today?",
    "what's your name": "I am ChatBot Katyayini, your ai friend.",
    "what is your purpose": "My purpose is to help you with anything you need, whether it's information, advice, or just a conversation.",
    
    # Appreciation & Polite Interactions
    "thank you": "You're welcome! Let me know if you need anything else.",
    "thanks": "You're welcome! How else can I help you?",
    "no problem": "Glad I could help! What else is on your mind?",
    "sorry": "No worries, there's nothing to apologize for!",
    
    # Farewells
    "bye": "Goodbye, take care and have a great day!",
    "goodbye": "Goodbye! Wishing you all the best!",
    "see you later": "See you later! Have a great time!",
    "take care": "Take care! I hope to chat with you again soon!",
    
    # Questions about Time and Date
    "what is the time": "The current time is " + time.strftime('%H:%M:%S') + ".",
    "what time is it": "It's " + time.strftime('%H:%M:%S') + ".",
    "what day is it today": "Today's date is " + time.strftime('%D') + ".",
    "what's today's date": "Today's date is " + time.strftime('%D') + ".",
    
    # Questions about Weather
    "what's the weather like": "I'm afraid I can't check the weather, but you can easily find out on your phone or computer!",
    "how's the weather": "I don't have access to real-time weather data, but you can check any weather app or website for an update!",
    
    # Random Fun Responses
    "tell me a joke": "Why don't skeletons fight each other? They don't have the guts!",
    "make me laugh": "Why don’t oysters donate to charity? Because they’re shellfish!",
    "what is the meaning of life": "The meaning of life is a philosophical question, but many people say it's to live, learn, and be happy!",
    
    # Frustration or Negative Responses
    "i'm frustrated": "I'm sorry you're feeling frustrated. Would you like to talk about it?",
    "i'm angry": "I'm sorry you're feeling this way. Do you want to vent or talk it through?",
    "this is annoying": "I'm really sorry to hear that. How can I help make things better?",
    "this sucks": "I get it, things aren't always great. What can I do to help you feel better?",
    "i'm tired": "It sounds like you’ve had a long day. Maybe a break would help?",
    
    # Motivation
    "i need motivation": "You’ve got this! Keep pushing forward and don’t give up!",
    "encourage me": "Believe in yourself and keep moving forward. Every step is progress!",
    "cheer me up": "Everything will be okay! Keep your head up, you’re doing great!",
    
    # Self-Reflection
    "who am i": "You're an amazing person with so much potential!",
    "what am i doing with my life": "Life can be tough sometimes. But every step you take matters. You’re on the right path.",
    "what is my purpose": "Your purpose is what you decide it is. Whether it’s helping others, learning, or growing, you’re making an impact.",
    
    # Relationship Advice
    "how to deal with stress": "Try to take deep breaths and give yourself a break. Sometimes, a little rest helps clear your mind.",
    "how to make a friend": "Just be yourself, be kind, and show interest in others. Genuine connections happen naturally!",
    "how to be happy": "Find the things that make you feel good, and try to surround yourself with positive people and activities.",
    
    # Science and Knowledge
    "what is science": "Science is the pursuit of knowledge through observation, experimentation, and analysis.",
    "what is physics": "Physics is the branch of science concerned with the nature and properties of matter and energy.",
    "what is chemistry": "Chemistry is the science that deals with the properties, composition, and reactions of matter.",
    "what is biology": "Biology is the study of living organisms and their vital processes.",
    
    # Technology Questions
    "what is ai": "AI (Artificial Intelligence) refers to the simulation of human intelligence in machines.",
    "what is machine learning": "Machine Learning is a type of AI where machines can learn from data and improve over time.",
    "what is deep learning": "Deep learning is a subset of machine learning that uses neural networks with many layers to analyze large amounts of data.",
    "what is blockchain": "Blockchain is a decentralized digital ledger technology that records transactions across many computers securely.",
    
    # Personal Queries
    "how old are you": "I don’t have an age, but I’m always here to help you!",
    "where are you from": "I don’t have a physical location, but I’m here for you wherever you are.",
    "what do you look like": "I don’t have a body or a face, but I like to think of myself as a helpful presence!",
    
    # Philosophical Questions
    "what is the meaning of life": "The meaning of life is a deeply personal and philosophical question. What do *you* think the meaning of life is?",
    "is there life after death": "That's one of the biggest questions humanity has explored. Different cultures and philosophies offer various perspectives.",
    
    # Random Miscellaneous Questions
    "how do i make coffee": "To make coffee, you’ll need ground coffee, water, and a coffee maker. Just brew and enjoy!",
    "how to cook rice": "To cook rice, rinse it first, then use a 2:1 water-to-rice ratio. Boil, then simmer for 15-20 minutes.",
    "how do i start a blog": "To start a blog, choose a platform (like WordPress or Blogger), pick a domain name, and start writing!",
    
    # Health and Wellness
    "what is yoga": "Yoga is an ancient practice that combines physical postures, breathing exercises, and meditation for health and wellness.",
    "how can i lose weight": "A balanced diet and regular exercise are key. It's important to consult a healthcare professional for personalized advice.",
    "how to meditate": "To meditate, find a quiet space, close your eyes, and focus on your breath. Let thoughts come and go without judgment.",
    
    # Fun Facts
    "tell me something interesting": "Did you know? Octopuses have three hearts and blue blood!",
    "give me a fun fact": "Here's a fun fact: Honey never spoils! Archaeologists have found pots of honey in ancient tombs that are still good to eat!",
}


# Function to remove emojis from text
def remove_emoji_tag(text):
    """Removes emojis and other special characters from text."""
    return re.sub(r'[^\w\s,.]', '', text)

# Function to auto-correct user input
def auto_correct_sentence(text):
    """Auto-corrects sentences using TextBlob."""
    corrected_text = TextBlob(text).correct()
    return str(corrected_text)

# Function to generate chatbot responses
def generate_response(user_input):
    """Generates responses based on the user's input."""
    user_input = remove_emoji_tag(user_input)  # Remove emojis and special characters
    user_input = auto_correct_sentence(user_input)  # Auto-correct input
    user_input = user_input.lower()  # Convert input to lowercase
    response = "I'm sorry, I don't understand. Can you please rephrase your question?"  # Default response
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%D')

    # Dynamic responses for time and date
    responses.update({
        "what is the time": f"The current time is {current_time}.",
        "what day is it today": f"Today's date is {current_date}."
    })

    # Find the closest response using Levenshtein distance
    min_distance = np.inf
    for keyword in responses:
        distance = Levenshtein.distance(keyword, user_input)
        if distance < min_distance:
            min_distance = distance
            response = responses[keyword]

    return response

if __name__ == "__main__":
    print("ChatBot: Hello! Type 'bye' to end the conversation.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "bye":
            print("ChatBot: Goodbye, take care!")
            break
        else:
            response = generate_response(user_input)
            print("ChatBot: " + response)