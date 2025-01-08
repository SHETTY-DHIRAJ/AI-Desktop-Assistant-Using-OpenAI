import speech_recognition as sr
import pyttsx3
import subprocess
import os
import webbrowser
import requests
import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv
import streamlit as st

# load environment variables
load_dotenv()

# Note: For ease of work one can try mentioning all the respective values for below variables in string.
api_key= os.getenv("azure_openai_api_key") # Here you have to mention your azure openai api key.
api_version= os.getenv("azure_api_version") # Here you have to mention your azure openai api version.
azure_endpoint= os.getenv("azure_endpoint") # Here you have to mention your azure openai endpoint.
azure_deployment= os.getenv("azure_deployment_name") # Here you have to mention your azure openai deployment name.

# Function to handle text-to-speech
def speaker(text):
    # Reinitialize the engine to avoid run loop conflicts
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust the speech rate
    engine.say(text)
    engine.runAndWait()

# Creating the client
client= AzureOpenAI(
    api_key= api_key,
    api_version= api_version,
    azure_endpoint= azure_endpoint
)

# Streamlit App Layout
st.title("AI Desktop Assistant")
st.write("Interact with the assistant through voice or text.")

# Initialize the greeting status
if "greeted" not in st.session_state:
    st.session_state.greeted = False  # To track if the assistant greeted the user

# Conversation History
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Initialize the last user action
if "last_action" not in st.session_state:
    st.session_state.last_action = None  # Tracks the last user action (e.g., "speak", "text")

# Initialize the messages list
if "messages" not in st.session_state:
    # Initialize the conversation history with a system message (e.g., setting assistant behavior)
    st.session_state.messages = [
        {
            "role": "system", "content": """
            
            You are an AI desktop assistant designed to help the user with a variety of tasks on their machine. Your main role is to assist with tasks such as:

            1. Interactive Conversations: You will interact with the user in a conversational manner, understanding and responding to questions, clarifications, and requests.

            2. Task-Performed Messages: At times, tasks will be executed directly by the assistant's underlying code (e.g., opening a website or application, mentioning current time). These tasks might not need to be explicitly confirmed by the assistant but should be understood as performed actions.

            3. Context Handling: Your responses should maintain the context of previous interactions, understanding that certain actions like opening a website or app are being managed by the code behind you. Always be aware of the actions performed automatically and refer to them when relevant to the user.
            
            4. System-Related Tasks and History Check: If the user requests system-related tasks that may require specific permissions or access (e.g., modifying system settings, installing software, Set a timer for 30 minutes), you should check the previous conversation history to see if similar actions were previously performed.
        
                4.1. If a similar task has been performed before and is relevant, you should provide the user with the relevant information.
                
                4.2. If the task has not been performed before or is not currently possible, you should inform the user that the task cannot be performed at the moment.
            """
        }
    ]

if "text_input_buffer" not in st.session_state:
    st.session_state.text_input_buffer = ""  # Temporary buffer for input text

# Display the conversation dynamically using `st.container`
conversation_container = st.container()

# Display the conversation history inside the container
def conversation_display():
    with conversation_container:
        st.write("### Conversation History")
        if st.session_state.conversation:
            for sender, message in st.session_state.conversation:
                st.markdown(f"**{sender}:** {message}")
        else:
            st.write("No conversation history yet.")

# Greet the user when the app is first loaded
if not st.session_state.greeted:
    initial_message = "How can I help you?"
    st.session_state.conversation.append(("Assistant", initial_message))
    speaker(initial_message)  # Speak the greeting
    st.session_state.greeted = True

# Real-time Feedback
status_placeholder = st.empty()

# This function to trim message history to the last few messages
def trim_history():
    # Here we consider only last 28 message.
    max_history_length = 28
    if len(st.session_state.messages) > max_history_length:
        # Keep the system message intact, and trim the rest except the last 'max_history_length' messages
        st.session_state.messages[1:] = st.session_state.messages[-(max_history_length - 1):]

# This function is use for all the azure openai related tasks. (i.e., send a new user message and get a response)
def az_openai(prompt):

    print(prompt)

    # Append the user message to the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Trim the message history to keep only the last few messages. This will keep the token within the limit.
    trim_history()

    # Generate the assistant's response using the conversation history
    response= client.chat.completions.create(
        model= azure_deployment,
        messages= st.session_state.messages,
        temperature= 0.7,
        max_tokens= 256,
        top_p= 0.9,
        frequency_penalty= 0.2,
        presence_penalty= 0.0
    )

    try:
        # Get the assistant's response from the API result
        assistant_reply = response.choices[0].message.content
        
    except Exception as e:
        print("az_openai function encountered an error: "+ str(e))
        assistant_reply= ""
    
    # Append the assistant's reply to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})    
    return assistant_reply

# This function is use when there is a need to perform task specific azure openai operations without updating the chat history.
def az_openai_tasks_pecific(prompt):

    # Generate the assistant's response using the conversation history
    response= client.chat.completions.create(
        model= azure_deployment,
        messages= [{"role": "user", "content": prompt}],
        temperature= 0.7,
        max_tokens= 256,
        top_p= 0.9,
        frequency_penalty= 0.2,
        presence_penalty= 0.0
    )

    try:
        # Get the assistant's response from the API result
        assistant_reply = response.choices[0].message.content
        
    except Exception as e:
        print("az_openai_tasks_pecific function encountered an error: "+ str(e))
        assistant_reply= ""
    
    return assistant_reply

# This function is used to send a GET request and check the response status code.
def check_url(url):
    url_flag= False
    try:
        response = requests.get(url, timeout=5)  # Set a timeout to avoid hanging
        if response.status_code in (200, 403):
            print(f"URL {url} is up and running!")
            url_flag= True
        else:
            print(f"URL {url} returned status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # This will catch most network-related exceptions
        print(f"Network-related error occurred with {url}. Error: {e}")
    except Exception as e:
        # This will catch all other exceptions, including unexpected ones
        print(f"An unexpected error occurred with {url}. Error: {e}")
    return url_flag

# This function is used to listen the users voice and then return the audio's text format with the respective flag if the audio is successfully converted then True else False if there is some exception.
def get_voice_input():
    query= ""
    query_flag= False
    recognizer= sr.Recognizer() # This will be further utilized to recognize the input.

    with sr.Microphone() as source: # Taking audio input from the microphone.
        print("Listining....")
        # st.info("Listening...")
        recognizer.pause_threshold= 1

        try:
            audio= recognizer.listen(source) # Converting audio input to audio data.
            query= recognizer.recognize_google(audio, language= "en-in") # audio data is recognized here with the language selected.
            print(f"User said: {query}")
            print("Processing done.")
            query_flag= True

        except sr.UnknownValueError:
            query= "Sorry, I did not understand that. Try again"
        except sr.RequestError:
            query= "Sorry, there was an error with the speech recognition service. Try again"
        except sr.WaitTimeoutError:
            return "No input detected. Please try again."
        except Exception as e:
            query= "Sorry, Some error occured. Try again"

        return query, query_flag

# This function Check if the application is installed on the system.
def is_app_installed(app_name):

    # For Windows, we can try searching the app in the PATH or using the `where` command
    try:
        subprocess.run(f"where {app_name}.exe", check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Application {app_name} was found as a installed application in your machine.")
        return True
    except subprocess.CalledProcessError:
        print(f"Application '{app_name}' not found as an installed application in your machine. Opening it in a web browser.")
        return False

# Function to process user input (text or voice)
def respond_to_input(speech_input):
    response_text= "" # This will contain the return text/response.
    response_flag= False # This flag will identify whether the response is success or not.

    # This is used to open any online websites.
    if "open" in speech_input.lower():

        # Append the user message to the conversation history
        st.session_state.messages.append({"role": "user", "content": speech_input})

        # Below code identifies the app/website the user is requesting to open.
        app_site_name= az_openai_tasks_pecific(f"""Given the input "{speech_input}", extract the **primary keyword** or **main term** mentioned in the sentence. If no meaningful keyword can be identified, return an empty string. If the keyword consists of multiple words, return the full phrase. Do not include any additional text or explanations, just return the **keyword** or an empty string.

                                                    Input: "{speech_input}"

                                                    Response:""")
                        
        if app_site_name:
            app_site_name= app_site_name.lower()
        
            if is_app_installed(app_site_name):
                response_text= f"Opening {app_site_name}"
                response_flag= True
                speaker(response_text)
                os.system(f"start {app_site_name}.exe")  # Windows command to open an app

                # Append the assistant's reply to the conversation history
                st.session_state.messages.append({"role": "assistant", "content": f"The AI Desktop Assistant has opened {app_site_name} on users request"})
            else:
                browser_url= az_openai_tasks_pecific(f"""Given the input {app_site_name}, check if it corresponds to a valid website domain. Return the full URL (e.g., https://domain.com) if a valid domain exists for that keyword. If no valid URL exists, return an empty string. Do not include any explanations, just return the URL or an empty string.

                                                        Input: "{app_site_name}"

                                                        Response:""")
                                
                # Checking if the azure openai returned a valid url and whether the url up and running.
                if browser_url and check_url(browser_url):

                    response_text= f"Opening {app_site_name} in browser"
                    response_flag= True                    
                    speaker(response_text)
                    webbrowser.open(browser_url) # This will open the site in webbrowser

                    # Append the assistant's reply to the conversation history
                    st.session_state.messages.append({"role": "assistant", "content": f"The AI Desktop Assistant has opened {browser_url} in browser on users request"})

                else:
                    response_text= f"Sorry, Some error occured. Try again"
                    speaker(response_text)

                    # Append the assistant's reply to the conversation history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
        
        else:
            response_text= f"Sorry, Some error occured. Try again"
            speaker(response_text)

            # Append the assistant's reply to the conversation history
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    # This is used to handle time and date related query.
    elif "time" in speech_input.lower() or "date" in speech_input.lower():

        # Getting the currnt time
        current_time= datetime.datetime.now().strftime("%H:%M:%S")

        # Getting the current date
        current_date= datetime.date.today().strftime("%d-%m-%Y")  # Day-Month-Year format

        assistant_reply= az_openai(f"The user has asked '{speech_input}'. current time is {current_time} and today's date is {current_date} this information is fetched from the underlying code. You can utilize the current time and date mentioned if the user asked question is relevent. Or provide an appropriate response if the request is unrelated.")

        if assistant_reply:
            response_text= assistant_reply
            response_flag= True
            speaker(response_text)
        else:
            response_text= "Sorry, Some error occured in openai functionality. Try again"
            speaker(response_text)
    
    # This is used to reset the chat history saved.
    elif "reset chat" in speech_input.lower() or "reset history" in speech_input.lower() or "clear chat" in speech_input.lower():
        st.session_state.messages.clear()
        st.session_state.messages = [
            {
                "role": "system", "content": """
                
                You are an AI desktop assistant designed to help the user with a variety of tasks on their machine. Your main role is to assist with tasks such as:

                1. Interactive Conversations: You will interact with the user in a conversational manner, understanding and responding to questions, clarifications, and requests.

                2. Task-Performed Messages: At times, tasks will be executed directly by the assistant's underlying code (e.g., opening a website or application, mentioning current time). These tasks might not need to be explicitly confirmed by the assistant but should be understood as performed actions.

                3. Context Handling: Your responses should maintain the context of previous interactions, understanding that certain actions like opening a website or app are being managed by the code behind you. Always be aware of the actions performed automatically and refer to them when relevant to the user.
                
                4. System-Related Tasks and History Check: If the user requests system-related tasks that may require specific permissions or access (e.g., modifying system settings, installing software, Set a timer for 30 minutes), you should check the previous conversation history to see if similar actions were previously performed.
            
                    4.1. If a similar task has been performed before and is relevant, you should provide the user with the relevant information.
                    
                    4.2. If the task has not been performed before or is not currently possible, you should inform the user that the task cannot be performed at the moment.
                """
            }
        ]
        print("Message history has been reset.")
        response_text= "Chat history has been reset. Is there anything else I can do for you."
        st.session_state.conversation = []
        response_flag= True
        speaker(response_text)

    # This is used to quit or exit the ai desktop assistant.
    elif "exit chat" in speech_input.lower() or "quit chat" in speech_input.lower() or "end chat" in speech_input.lower():
        assistant_reply= az_openai("Bye")
        if assistant_reply:
            response_text= "Exiting the AI Desktop Assistant"
            response_flag= True
            speaker(assistant_reply)
            print("Exiting the AI Desktop Assistant")
            exit()
        else:
            response_text= "Sorry, Some error occured in openai functionality. Try again"
            speaker(response_text)

    # By default if the user input is not identified as any of the above predefined tasks then the flow will invoke the azure openai and start the conversation.
    else:
        assistant_reply= az_openai(speech_input)
        if assistant_reply:
            response_text= assistant_reply
            response_flag= True
            speaker(response_text)
        else:
            response_text= "Sorry, Some error occured in openai functionality. Try again"
            speaker(response_text)
    
    return response_text, response_flag

# Text Input Field and Buttons
col1, col2 = st.columns([3, 1], vertical_alignment= "bottom", border= True)  # Split the input area into columns
with col1:
    # Allowing user for Text Input. Text input field bound to session state
    text_input = st.text_input(
        label= "Type your command here:",
        key= "text_input_field",
        on_change= lambda: st.session_state.update(
            text_input_buffer= st.session_state.text_input_field
        ),  # Sync the text field with the buffer
    )

with col2:
    # Submit Text Input
    if st.button("⌨️ Send Text", key="text_button", on_click= lambda: st.session_state.update(text_input_field= "")):  # Clear the text input field after submission
        st.session_state.last_action = "text"
        if st.session_state.text_input_buffer.strip():  # Process only non-empty input, preventing accidental submissions of blank commands.
            status_placeholder.info("Porcessing your text input...")
            st.session_state.conversation.append(("You (Text)", st.session_state.text_input_buffer))
            response_text, response_flag = respond_to_input(st.session_state.text_input_buffer)
            if response_flag:
                status_placeholder.success("Conversation successfully processed.")
                if response_text not in [ "Chat history has been reset. Is there anything else I can do for you.", "Exiting the AI Desktop Assistant"]:
                    st.session_state.conversation.append(("Assistant", response_text))
            else:
                status_placeholder.error("Error while processing conversations.")
                st.session_state.conversation.append(("Assistant", response_text))
            # Clear the text input buffer
            st.session_state.text_input_buffer = ""
        else:
            status_placeholder.error("Please enter a valid query.")

# Voice Input Button
if st.button("🎙️ Voice Input", key="speak_button"):
    st.session_state.last_action = "speak"
    status_placeholder.info("Listening for your voice input...")
    speech_input, success = get_voice_input()
    if success:
        status_placeholder.info("Captured voice input.")
        st.session_state.conversation.append(("You (Voice)", speech_input))
        response_text, response_flag = respond_to_input(speech_input)
        if response_flag:
            status_placeholder.success("Conversation successfully processed.")
            if response_text not in [ "Chat history has been reset. Is there anything else I can do for you.", "Exiting the AI Desktop Assistant"]:
                st.session_state.conversation.append(("Assistant", response_text))
        else:
            status_placeholder.error("Error while processing conversations.")
            st.session_state.conversation.append(("Assistant", response_text))
    else:
        status_placeholder.error(speech_input)

# Clear Conversation History Button
if st.button("🧹 Clear Conversation", key="clear_button"):
    st.session_state.last_action = "clear"
    status_placeholder.info("Clearing conversation history...")
    response_text, response_flag = respond_to_input("reset chat")
    if response_flag:
        status_placeholder.success("Conversation history is cleared!")
    else:
        status_placeholder.error("Conversation history was not cleared. Try again.")

# Refresh the conversation container to display the updated conversation
conversation_display()