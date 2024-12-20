import speech_recognition as sr
import win32com.client
import time
import nltk
from nltk.corpus import stopwords
import sys
import subprocess
import os
import webbrowser
import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Note: For ease of work one can try mentioning all the respective values for below variables in string.
api_key= os.getenv("azure_openai_api_key") # Here you have to mention your azure openai api key.
api_version= os.getenv("azure_api_version") # Here you have to mention your azure openai api version
azure_endpoint= os.getenv("azure_endpoint") # Here you have to mention your azure openai endpoint
azure_deployment= os.getenv("azure_deployment_name") # Here you have to mention your azure openai deployment name

# Creating the client
client= AzureOpenAI(
    api_key= api_key,
    api_version= api_version,
    azure_endpoint= azure_endpoint
)

# Initialize the conversation history with a system message (e.g., setting assistant behavior)
messages = [
    {"role": "system", "content": "You are a helpful ai desktop assistant."}
]

# This function to trim message history to the last few messages
def trim_history():
    # Here we consider only last 28 message.
    max_history_length = 28
    if len(messages) > max_history_length:
        # Keep the system message intact, and trim the rest except the last 'max_history_length' messages
        messages[1:] = messages[-(max_history_length - 1):]

# This function is use for all the azure openai related tasks. (i.e., send a new user message and get a response)
def az_openai(prompt):

    # Append the user message to the conversation history
    messages.append({"role": "user", "content": prompt})

    # Trim the message history to keep only the last few messages. This will keep the token within the limit.
    trim_history()

    # Generate the assistant's response using the conversation history
    response= client.chat.completions.create(
        model= azure_deployment,
        messages= messages,
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
    messages.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

# Here we are creating an instance of the Speech API's (SpVoice) object, enabling text-to-speech functionality.
speaker= win32com.client.Dispatch("SAPI.SpVoice")

# This function is used to listen the users voice and then return the audio's text format with the respective flag if the audio is successfully converted then 1 else 0 if there is some exception.
def takecommand():

    print("Listining....")
    query= ""
    query_flag= 0
    rec= sr.Recognizer() # This will be further utilized to recognize the input.

    with sr.Microphone() as source: # Taking audio input
        rec.pause_threshold= 1
        audio= rec.listen(source) # Converting audio input to audio data.

        try:
            query= rec.recognize_google(audio, language= "en-in") # audio data is recognized here with the language selected.
            print(f"User said: {query}")
            print("Processing done.")
            query_flag= 1

        except sr.UnknownValueError:
            query= "Sorry, I did not understand that. Try again"
        except sr.RequestError:
            query= "Sorry, there was an error with the speech recognition service. Try again"
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

# This function is used to remove the stopwords like "the", "and", "is", etc.) which do not contribute much in the meaning of the sentence.
def remove_stopwords(input_string):

    # downloading stopwords. This will be later used to remove the stopwords in the sentence.
    nltk.download('stopwords')

    # Get the set of stopwords
    stop_words = set(stopwords.words('english'))

    # Split the input string into words
    words = input_string.split()
    
    # Remove stopwords
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Join the filtered words back into a string
    return " ".join(filtered_words)


if __name__ == '__main__':
    print("---- The AI Desktop Assistance starts here ----")
    time.sleep(1) # By this halt time the very next line of code executes smoothly.
    speaker.Speak("How can I help you") # This will give the audio output.
    while True:
        speech_input, speech_flag= takecommand()

        if speech_flag:

            # This is used to open any online websites.
            if "open" in speech_input.lower():

                speech_input_without_stopwords= remove_stopwords(speech_input)

                # Here in below code the very next word after the "open" is identified. In our case it is considered to be site/website the user want to open.
                app_site_name = next((speech_input_without_stopwords.split()[i+1] 
                                for i, word in enumerate(speech_input_without_stopwords.split()) 
                                if word.lower() == "open" 
                                and i+1 < len(speech_input_without_stopwords.split())), None).lower()
                
                if is_app_installed(app_site_name):
                    speaker.Speak(f"Opening {app_site_name}")
                    os.system(f"start {app_site_name}.exe")  # Windows command to open an app
                else:
                    speaker.Speak(f"Opening {app_site_name}")
                    webbrowser.open(f"https://{app_site_name}.com") # This will open the site in webbrowser

            # This is used to get the current system time.
            elif "what" in speech_input.lower() and "time" in speech_input.lower():

                strfTime= datetime.datetime.now().strftime("%H:%M:%S")
                speaker.Speak(f"The time is {strfTime}")
            
            # This is used to reset the chat history saved.
            elif "reset chat" in speech_input.lower() or "reset history" in speech_input.lower() or "clear chat" in speech_input.lower():
                messages.clear()
                messages = [{"role": "system", "content": "You are a helpful assistant."}]
                print("Message history has been reset.")
                speaker.Speak("Chat history has been reset.")

            # This is used to quit or exit the ai desktop assistant.
            elif "exit chat" in speech_input.lower() or "quit chat" in speech_input.lower():
                speaker.Speak(az_openai("Bye"))
                print("Exiting the AI Desktop Assistant")
                exit()

            # By default if the user input is not identified as any of the above predefined tasks then the flow will invoke the azure openai and start the conversation.
            else:
                assistant_reply= az_openai(speech_input[8:])
                if assistant_reply:
                    speaker.Speak(assistant_reply)
                else:
                    speaker.Speak("Sorry, Some error occured in openai functionality. Try again")

        else:
            speaker.speak(speech_input)
            print(f"System message: {speech_input}")
