import speech_recognition as sr
import win32com.client
import time

speaker= win32com.client.Dispatch("SAPI.SpVoice")

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



if __name__ == '__main__':
    print("---- The AI Desktop Assistance starts here ----")
    time.sleep(1) # By this halt time the very next line of code executes smoothly.
    speaker.Speak("How can I help you") # This will give the audio output.
    while True:
        speech_input, speech_flag= takecommand()
        if speech_flag:
            # Repeat the speech input
            speaker.Speak(f"You said: {speech_input}")
        else:
            speaker.speak(speech_input)
