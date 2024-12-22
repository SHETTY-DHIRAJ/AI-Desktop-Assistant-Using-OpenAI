# AI Desktop Assistant Using OpenAI

This project implements an **AI Desktop Assistant** powered by **Azure OpenAI** that allows users to interact with their computer through natural language and voice commands. The assistant is designed to facilitate seamless user interaction, perform task-specific actions, and provide contextually relevant responses. Key features include voice recognition, integration with OpenAI for dynamic conversations, and efficient management of chat history, enabling an intuitive and intelligent experience.

## Key Features

1. **Interactive Conversation with Azure OpenAI Integration**:
   - The assistant leverages **Azure OpenAI** to enable dynamic, intelligent, and multi-turn conversations. 
   - It remembers previous interactions and maintains **chat history** to ensure context-aware responses, making each conversation more meaningful and coherent.

2. **Voice Recognition & Audio Response**:
   - The assistant listens to user voice commands using the **speech_recognition** library and provides verbal feedback using the **SAPI Speech API**. 
   - This feature allows users to interact with the assistant hands-free, enhancing accessibility and user experience.

3. **Task-Specific Action Management**:
   - The assistant can launch installed applications directly from voice commands. If an application is not installed, it will open the relevant website in the browser.
   - It can also provide quick access to system-related queries, such as the current time and date, helping users stay organized and informed.

4. **Data Preprocessing**:
   - For improved voice command understanding, the assistant employs advanced **Azure OpenAI prompting** to clean and process voice inputs, extracting relevant keywords for accurate task execution. 
   - Previously, **NLTK librarie** was used for data preprocessing tasks (e.g., removing stop words), but this was later replaced with more sophisticated prompting methods to enhance processing efficiency.

5. **Chat History Management**:
   - The assistant allows users to manage their chat history, including options to reset or clear the history dynamically. This feature ensures privacy and gives users control over their data.

6. **Error Handling**:
   - The assistant is designed with robust **error handling** capabilities, providing fallback responses for unrecognized commands or errors related to speech recognition and OpenAI interactions.
   - This ensures a smooth user experience even when issues arise, preventing the assistant from malfunctioning and maintaining reliability.

## Project Structure

| File/Directory      | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `main.py`           | The core script containing the logic for the AI desktop assistant.         |
| `requirements.txt`  | List of dependencies and libraries required for the project.               |
| `.env`              | Environment file containing secrets such as API keys and endpoints.        |

---

## Getting Started

### Prerequisites

1. **Install Dependencies**:
   - Make sure you have Python 3.8 or higher installed.
   - Install the required packages using the following command:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the project directory with the following variables:
     ```plaintext
     azure_openai_api_key= <your_azure_openai_api_key>
     azure_api_version= <your_azure_api_version>
     azure_endpoint= <your_azure_openai_endpoint>
     azure_deployment_name= <your_azure_deployment_name>
     ```

## How to Run

1. **Start the Assistant**:
   Run the `main.py` script:
   ```bash
   python main.py

2. **Interact with the Assistant**:
   - Speak commands such as:
      - "Open (application name)" to open applications or websites.
      - "What is the time?" to get the current system time.
      - "Reset chat" or "Clear history" to clear the assistant's memory.
      - "Exit chat" to quit the assistant.
   - The assistant will intelligently respond to other queries by interacting with Azure OpenAI.

## Future Enhancements
   - Add support for additional system utilities like file management and weather forecasting.
   - Improve natural language understanding for more complex commands.
   - Enhance error handling and conversational flexibility.

## Acknowledgements
   - This project utilizes various libraries, including Azure OpenAI, speech_recognition and SAPI Speech API.
   - Special thanks to [Code with Harry](https://www.youtube.com/@CodeWithHarry) for his guidance. 
