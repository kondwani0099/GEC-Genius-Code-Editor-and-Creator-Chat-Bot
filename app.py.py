import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3

# Initialize session state
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# Set up your OpenAI API key
api_key = ''
openai.api_key = api_key

# Initialize PyAudio and speech recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Title of the web app
st.title("OpenAI Code Generation App")

# Input field for the prompt
st.sidebar.subheader("Enter your prompt:")
prompt = st.sidebar.text_area("")

# Button to start speech input
if st.sidebar.button("Start Speech Input"):
    with microphone as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        prompt = st.sidebar.text_area("Speech Input:", value=text, height=200, max_chars=None)
    except sr.UnknownValueError:
        st.sidebar.warning("Could not understand audio")
    except sr.RequestError:
        st.sidebar.error("Could not request results")

# If there's an error message, display it
if st.session_state.error_message:
    st.subheader("Error:")
    st.error(st.session_state.error_message)

# Button to generate code
if st.sidebar.button("Generate Code"):
    try:
        if not prompt:
            raise ValueError("Prompt is empty. Please provide a prompt.")

        # Create a chat completion
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the generated code from the completion response
        generated_code = completion.choices[0].message

        # Display the generated code
        st.subheader("Generated Code:")
        st.code(generated_code)

        # Warning about executing external code
        st.warning("Warning: Executing code generated from external sources can be unsafe.")

    except Exception as e:
        # Store the error message
        st.session_state.error_message = f"Error: {str(e)}"

        # Display the error message
        st.subheader("Error:")
        st.error(st.session_state.error_message)

# Button to start speech output
if st.sidebar.button("Start Speech Output"):
    engine.say(prompt)
    engine.runAndWait()

# Keep the Streamlit app running
# st.stop()
