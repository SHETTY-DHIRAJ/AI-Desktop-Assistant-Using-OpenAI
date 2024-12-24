import speech_recognition as sr
import win32com.client
import time
import subprocess
import os
import webbrowser
import requests
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

# Here we are creating an instance of the Speech API's (SpVoice) object, enabling text-to-speech functionality.
speaker= win32com.client.Dispatch("SAPI.SpVoice")

# Creating the client
client= AzureOpenAI(
    api_key= api_key,
    api_version= api_version,
    azure_endpoint= azure_endpoint
)

# Initialize the conversation history with a system message (e.g., setting assistant behavior)
messages = [
    # {"role": "system", "content": "You are a helpful ai desktop assistant."}

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

if __name__ == '__main__':
    print("---- The AI Desktop Assistance starts here ----")
    time.sleep(1) # By this halt time the very next line of code executes smoothly.
    speaker.Speak("How can I help you") # This will give the audio output.
    while True:
        speech_input, speech_flag= takecommand()

        if speech_flag:

            # This is used to open any online websites.
            if "open" in speech_input.lower():

                # Append the user message to the conversation history
                messages.append({"role": "user", "content": speech_input})

                # Below code identifies the app/website the user is requesting to open.
                app_site_name= az_openai_tasks_pecific(f"""Given the input "{speech_input}", extract the **primary keyword** or **main term** mentioned in the sentence. If no meaningful keyword can be identified, return an empty string. If the keyword consists of multiple words, return the full phrase. Do not include any additional text or explanations, just return the **keyword** or an empty string.

                                                            Input: "{speech_input}"

                                                            Response:""")
                                
                if app_site_name:
                    app_site_name= app_site_name.lower()
                
                    if is_app_installed(app_site_name):
                        speaker.Speak(f"Opening {app_site_name}")
                        os.system(f"start {app_site_name}.exe")  # Windows command to open an app

                        # Append the assistant's reply to the conversation history
                        messages.append({"role": "assistant", "content": f"The AI Desktop Assistant has opened {app_site_name} on users request"})

                    else:
                        browser_url= az_openai_tasks_pecific(f"""Given the input {app_site_name}, check if it corresponds to a valid website domain. Return the full URL (e.g., https://domain.com) if a valid domain exists for that keyword. If no valid URL exists, return an empty string. Do not include any explanations, just return the URL or an empty string.

                                                                Input: "{app_site_name}"

                                                                Response:""")
                        
                        print("browser_url: " + browser_url)
                        
                        # Checking if the azure openai returned a valid url and whether the url up and running.
                        if browser_url and check_url(browser_url):
                            
                            speaker.Speak(f"Opening {app_site_name} in browser")
                            webbrowser.open(browser_url) # This will open the site in webbrowser

                            # Append the assistant's reply to the conversation history
                            messages.append({"role": "assistant", "content": f"The AI Desktop Assistant has opened {browser_url} in browser on users request"})

                        else:
                            speaker.Speak(f"Sorry, Some error occured. Try again")

                            # Append the assistant's reply to the conversation history
                            messages.append({"role": "assistant", "content": f"Sorry, Some error occured. Try again"})
                
                else:
                    speaker.Speak(f"Sorry, Some error occured. Try again")

                    # Append the assistant's reply to the conversation history
                    messages.append({"role": "assistant", "content": f"Sorry, Some error occured. Try again"})


            # This is used to handle time and date related query.
            elif "time" in speech_input.lower() or "date" in speech_input.lower():

                # Getting the currnt time
                current_time= datetime.datetime.now().strftime("%H:%M:%S")

                # Getting the current date
                current_date = datetime.date.today().strftime("%d-%m-%Y")  # Day-Month-Year format

                assistant_reply= az_openai(f"The user has asked '{speech_input}'. current time is {current_time} and today's date is {current_date} this information is fetched from the underlying code. You can utilize the current time and date mentioned if the user asked question is relevent. Or provide an appropriate response if the request is unrelated.")

                if assistant_reply:
                    speaker.Speak(assistant_reply)
                else:
                    speaker.Speak("Sorry, Some error occured in openai functionality. Try again")
            
            # This is used to reset the chat history saved.
            elif "reset chat" in speech_input.lower() or "reset history" in speech_input.lower() or "clear chat" in speech_input.lower():
                messages.clear()
                messages = [{"role": "system", "content": "You are a helpful assistant."}]
                print("Message history has been reset.")
                speaker.Speak("Chat history has been reset. Is there anything else I can do for you.")

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
