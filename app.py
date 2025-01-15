import streamlit as st
from transformers import pipeline

# Load Hugging Face's pre-trained GPT-2 model for text generation
generator = pipeline('text-generation', model='gpt2')

# Function to generate response using GPT-2 with dynamic and interactive prompts
def get_gpt2_response(prompt, user_context):
    """Generates a response using GPT-2 with dynamic and interactive prompts."""
    try:
        # Crafting a personalized and detailed prompt based on user context
        personalized_prompt = f"""
        You are a highly experienced fitness coach with extensive knowledge of workout routines, diet plans, and fitness strategies.
        The user has the following preferences:

        - **Fitness goal**: {user_context['goal']}
        - **Fitness level**: {user_context['level']}
        - **Workout Preferences**: {user_context['preferences']}
        - **Fitness constraints**: {user_context['constraints']}
        - **Workout Duration**: {user_context['duration']}
        - **Preferred Workout Type**: {user_context['workout_type']}
        - **Diet Preferences**: {user_context['diet']}
        - **Workout Time**: {user_context['time']}
        - **Available Equipment**: {user_context['equipment']}

        The user has asked the following question: "{prompt}"

        Please provide a **detailed, engaging, and personalized response** that takes into account the user's preferences and fitness context. Include advice on exercises, diet recommendations, and workout strategies tailored to their goal. If the user’s goal is specific, provide a plan or workout schedule suggestion.
        """

        # Generate a response using the GPT-2 model with optimized settings
        response = generator(personalized_prompt, max_length=250, num_return_sequences=1, temperature=0.7, top_p=0.9)
        return response[0]['generated_text']
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI setup
st.title("AI Fitness Coach Chatbot")
st.write("Welcome to your personalized fitness coach chatbot. Ask any fitness-related questions!")

# Initialize session state for user context if not already set
if 'goal' not in st.session_state:
    st.session_state.goal = ''
    st.session_state.level = ''
    st.session_state.preferences = ''
    st.session_state.constraints = ''
    st.session_state.duration = ''
    st.session_state.workout_type = ''
    st.session_state.diet = ''
    st.session_state.time = ''
    st.session_state.equipment = ''

# Step 1: Get User Goal
if st.session_state.goal == '':
    st.session_state.goal = st.text_input("What's your fitness goal? (e.g., weight loss, muscle gain, flexibility, etc.)")
    if st.session_state.goal:
        st.session_state.level = ''

# Step 2: Get User Fitness Level
if st.session_state.goal and st.session_state.level == '':
    st.session_state.level = st.text_input("What's your fitness level? (e.g., beginner, intermediate, advanced)")
    if st.session_state.level:
        st.session_state.preferences = ''

# Step 3: Get User Workout Preferences
if st.session_state.level and st.session_state.preferences == '':
    st.session_state.preferences = st.text_input("What type of workout do you prefer? (e.g., strength training, cardio, yoga)")
    if st.session_state.preferences:
        st.session_state.constraints = ''

# Step 4: Get Fitness Constraints
if st.session_state.preferences and st.session_state.constraints == '':
    st.session_state.constraints = st.text_input("Do you have any fitness constraints? (e.g., injuries, time constraints, etc.)")
    if st.session_state.constraints:
        st.session_state.duration = ''

# Step 5: Get Preferred Workout Duration
if st.session_state.constraints and st.session_state.duration == '':
    st.session_state.duration = st.text_input("What's your preferred workout duration? (e.g., 30 minutes, 1 hour)")
    if st.session_state.duration:
        st.session_state.workout_type = ''

# Step 6: Get Preferred Workout Type
if st.session_state.duration and st.session_state.workout_type == '':
    st.session_state.workout_type = st.text_input("What's your preferred workout type? (e.g., strength training, yoga, cardio)")
    if st.session_state.workout_type:
        st.session_state.diet = ''

# Step 7: Get Diet Preferences
if st.session_state.workout_type and st.session_state.diet == '':
    st.session_state.diet = st.text_input("What's your preferred diet? (e.g., high-protein, vegetarian, keto)")
    if st.session_state.diet:
        st.session_state.time = ''

# Step 8: Get Preferred Workout Time
if st.session_state.diet and st.session_state.time == '':
    st.session_state.time = st.text_input("What time of day do you prefer to workout? (e.g., morning, evening)")
    if st.session_state.time:
        st.session_state.equipment = ''

# Step 9: Get Available Equipment
if st.session_state.time and st.session_state.equipment == '':
    st.session_state.equipment = st.text_input("What workout equipment do you have available? (e.g., dumbbells, treadmill, none)")

# Once all information is gathered, generate personalized response
if st.session_state.equipment:
    # Create user context
    user_context = {
        'goal': st.session_state.goal,
        'level': st.session_state.level,
        'preferences': st.session_state.preferences,
        'constraints': st.session_state.constraints,
        'duration': st.session_state.duration,
        'workout_type': st.session_state.workout_type,
        'diet': st.session_state.diet,
        'time': st.session_state.time,
        'equipment': st.session_state.equipment
    }

    # Ask user a fitness question
    user_input = st.text_input("You: What would you like to know about your fitness plan?", "")

    if user_input:
        # Get personalized response based on user input and context
        response = get_gpt2_response(user_input, user_context)

        # Display the conversation in WhatsApp-like chat format
        col1, col2 = st.columns([1, 6])  # 1 for user's input (right) and 6 for bot's response (left)
        
        # User's input on the right side
        with col2:
            st.markdown(f"""
            <div style="text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px;">
            <strong>You:</strong> {user_input}
            </div>
            """, unsafe_allow_html=True)

        # Bot's response on the left side
        with col1:
            st.markdown(f"""
            <div style="text-align: left; background-color: #E1F5FE; padding: 10px; border-radius: 10px; margin: 5px;">
            <strong>Fitness Coach:</strong> {response}
            </div>
            """, unsafe_allow_html=True)
