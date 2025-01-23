# AI Desktop Assistant Using OpenAI

This project implements an **AI Desktop Assistant** powered by **Azure OpenAI** and **Streamlit** that allows users to interact with their computer through voice-based and text-based commands, providing a user-friendly experience for performing various tasks. A **Streamlit-based UI** enhances accessibility and usability, allowing users to interact through an intuitive web interface. The assistant is designed to facilitate seamless user interaction, perform task-specific actions, and provide contextually relevant responses. Key features include voice recognition, integration with OpenAI for dynamic conversations, and efficient management of chat history, enabling an intuitive and intelligent experience.

> **Note**: This project has been further enhanced with additional features, including a **Streamlit application** for a graphical interface, enabling users to input text queries, view conversation history, and switch between text and voice interactions seamlessly. These updates aim to provide a more versatile and user-friendly experience.

## Example Screenshots

### 1. Streamlit Dashboard

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Streamlit-Dashboard.png" alt="Streamlit Dashboard" width="480">
      <p><em>An interactive dashboard for voice and text interactions</em></p>
    </td>
  </tr>
</table>

<p align="center">----</p>

### 2. Text Input Interaction

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-TextInput-Question.png" alt="Chat-Conversation-TextInput-Question" width="400">
      <p><em>TextInput Question</em></p>
    </td>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-TextInput-Live-Status.png" alt="Chat-Conversation-TextInput-Live-Status" width="400">
      <p><em>TextInput Live Status</em></p>
    </td>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-TextInput-Response.png" alt="Chat-Conversation-TextInput-Response" width="400">
      <p><em>TextInput Response</em></p>
    </td>
  </tr>
</table>

<p align="center">----</p>

### 3. Chat History Based Conversation

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-History-Question.png" alt="Chat-Conversation-History-Question" width="480">
      <p><em>Chat History Based Question</em></p>
    </td>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-History-Response.png" alt="Chat-Conversation-History-Response" width="480">
      <p><em>Chat History Based Response</em></p>
    </td>
  </tr>
</table>

<p align="center">----</p>

### 4. Voice Input Interaction

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-VoiceInput-Listening.png" alt="Chat-Conversation-VoiceInput-Listening" width="400">
      <p><em>VoiceInput Listening</em></p>
    </td>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-VoiceInput-Live-Status.png" alt="Chat-Conversation-VoiceInput-Live-Status" width="400">
      <p><em>VoiceInput Live Status</em></p>
    </td>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-VoiceInput-Response.png" alt="Chat-Conversation-VoiceInput-Response" width="400">
      <p><em>VoiceInput Response</em></p>
    </td>
  </tr>
</table>

<p align="center">----</p>

### 5. Chat History Clear Button

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-History-Clear-ButtonClick.png" alt="Chat-Conversation-History-Clear-ButtonClick" width="480">
      <p><em>Chat History Clear Button On Click</em></p>
    </td>
    <td align="center">
      <img src="https://github.com/SHETTY-DHIRAJ/AI-Desktop-Assistant-Using-OpenAI/blob/main/Dependent-Resources/Chat-Conversation-History-Clear-ButtonClick-Response.png" alt="Chat-Conversation-History-Clear-ButtonClick-Response" width="480">
      <p><em>Chat History Clear Button On Click Response</em></p>
    </td>
  </tr>
</table>

---

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

## Streamlit App Features

1. **Input Methods**:
   - **Voice Commands**: Users can interact through voice for hands-free operation.
   - **Text Commands**: A text-based interface allows precise control and input.

2. **Dynamic Chat History**:
   - View previous interactions in real time.
   - Clear chat history with a single button click.

3. **Realtime Conversation status**:
   - View the realtime conversation status as the assistant proceeds.

## Project Structure

| File/Directory             | Description                                                                |
|----------------------------|----------------------------------------------------------------------------|
| `main.py`                  | The Core research-based script for the AI desktop assistant functionality. |
| `streamlit_assistant.py`   | Streamlit-powered web application for user-friendly interactions.          |
| `requirements.txt`         | List of dependencies and libraries required for the project.               |
| `.env`                     | Environment file containing secrets such as API keys and endpoints.        |

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

1. **Run the Streamlit Web App**:
   - Start the Streamlit-based assistant:
     ```bash
     streamlit run streamlit_assistant.py
     ```
   - Open the provided URL (usually `http://localhost:8501`) in your browser to interact with the assistant.

2. **Run the Research Version**:
   - If you wish to use the original version without a UI:
     ```bash
     python main.py
     ```

3. **Interact with the Assistant**:
   - Speak or type commands such as:
      - "Open (application name)" to open applications or websites.
      - "What is the time?" to get the current system time.
      - "Reset chat" or "Clear history" to clear the assistant's memory.
      - "Exit chat" to quit the assistant.
   - The assistant will intelligently respond to other queries by interacting with Azure OpenAI.

## Future Enhancements
   - Add support for additional system utilities like file management and weather forecasting.
   - Enhance UI to include user settings for customizing the assistant.
   - Improve natural language understanding for more complex commands.
   - Enhance error handling and conversational flexibility.

## Acknowledgements
   - This project utilizes various libraries, including Azure OpenAI, speech_recognition and SAPI Speech API.
   - Special thanks to [Code with Harry](https://www.youtube.com/@CodeWithHarry) for his guidance on `main.py` research.
