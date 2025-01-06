import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import spacy

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Training data for intent classification
X_train = [
    "hi", "hello", "hey",
    "workout schedule", "class timings", "fitness classes",
    "membership plans", "fees", "subscription cost",
    "diet tips", "nutrition advice", "healthy meal plan"
]

y_train = [
    "greeting", "greeting", "greeting",
    "workout", "workout", "workout",
    "membership", "membership", "membership",
    "diet", "diet", "diet"
]

# Vectorize the training data
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)

# Train a Naive Bayes model
model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

# Responses for intents
responses = {
    "greeting": "Hi there! How can I assist you today?",
    "workout": "We offer Yoga, Zumba, and Strength Training classes. Which one interests you?",
    "membership": "Our membership plans include monthly, quarterly, and yearly options. Would you like details?",
    "diet": "A balanced diet includes protein, carbs, and healthy fats. Need a personalized plan?",
    "default": "I'm sorry, I didn't quite get that. Could you please rephrase?"
}

# Function to predict intent
def predict_intent(user_input):
    user_vector = vectorizer.transform([user_input])
    return model.predict(user_vector)[0]

# Keyword extraction using spaCy
def extract_keywords(user_input):
    doc = nlp(user_input)
    return [token.text for token in doc if not token.is_stop and token.is_alpha]

# Streamlit app UI
st.title("Fitness Club Chatbot 🤖")
st.sidebar.header("Welcome to Your Fitness Assistant!")
st.sidebar.text("💪 Get workout plans\n🍎 Diet advice\n🗓️ Class schedules\n💬 Membership info")

# Personalization (Session state)
if "name" not in st.session_state:
    st.session_state['name'] = ""

if st.session_state['name'] == "":
    name = st.text_input("Please enter your name to get started:")
    if name:
        st.session_state['name'] = name
        st.success(f"Hello, {name}! How can I assist you today?")
else:
    # Display the user's name and accept their query
    st.write(f"Hello, {st.session_state['name']}! Ask me anything about fitness:")
    user_input = st.text_input("Your question:")
    
    if st.button("Submit"):
        if user_input:
            # Predict intent
            intent = predict_intent(user_input)

            # Extract keywords
            keywords = extract_keywords(user_input)

            # Generate response
            response = responses.get(intent, responses["default"])

            # Display the response
            st.write(f"Chatbot: {response}")
            
            # Display related keywords for workout intent
            if intent == "workout" and keywords:
                st.write(f"Related keywords: {', '.join(keywords)}")
        else:
            st.warning("Please type something to get a response.")

# Sidebar: Upcoming classes
st.sidebar.write("📅 Upcoming Classes:")
st.sidebar.text("1. Yoga - 7:00 AM\n2. Zumba - 6:00 PM\n3. Strength Training - 8:00 PM")
