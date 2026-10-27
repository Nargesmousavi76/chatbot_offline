# 🤖 Offline AI Chatbot with Ollama and Streamlit

## 📌 About the Project

This project is a local AI chatbot developed using Python, Streamlit, and Ollama.

It allows users to interact with a locally running language model through a simple and interactive web interface. The chatbot generates responses locally, without requiring a cloud-based AI API.

The project was developed as a Python programming practice project to explore local language models, API communication, Streamlit session state, real-time response streaming, and conversation management.

## ✨ Features

- 💬 **Interactive Chat Interface:** Chat with a local AI model through Streamlit.
- ⚡ **Streaming Responses:** Display AI responses gradually as they are generated.
- 🛑 **Stop Generation:** Stop the response generation when needed.
- 🆕 **New Chat:** Start a new conversation.
- 🧹 **Clear Chat:** Clear the current conversation.
- 💾 **Automatic Chat Saving:** Save user messages and completed AI responses automatically.
- 📂 **Chat History:** Store conversations separately as JSON files.
- 🕘 **Previous Conversations:** View and reopen saved conversations from the sidebar.
- 🔄 **Newest-First History:** Display recent conversations before older ones.
- 📝 **Chat Summarization:** Generate a summary of the conversation using the AI model.
- 📄 **Save Chat History:** Save conversation content to a text file.
- 📋 **Save Summaries:** Store generated summaries in a separate text file.

## 🛠️ Technologies Used

- **Python** – Main programming language
- **Streamlit** – Interactive web interface
- **Ollama** – Run large language models locally
- **Requests** – Communicate with the Ollama API
- **JSON** – Store individual conversations
- **Session State** – Maintain chat messages and application state

## 🧠 AI Model

This project uses the `gemma3:1b` model through Ollama.

You can use another locally available Ollama model by changing the model name in the application code.

## 📂 Project Structure

```text
chatbot_offline/
│
├── src/
│   ├── project_st.py       # Main Streamlit application
│   └── utils_new.py        # Ollama API communication
│
├── chat_history/           # Automatically saved conversations
│   └── chat_1.json
│
├── chat_history.txt        # Saved conversation text
├── chat_summary.txt        # Generated conversation summaries
│
└── README.md               # Project documentation
```

*Note: The directory and file structure may vary depending on your local project setup.*

## ⚙️ Requirements

Make sure Python and Ollama are installed on your computer.

Install the required Python packages:

```bash
pip install streamlit requests
```

## 🚀 Setup and Installation

### 1. Install Ollama

Download and install Ollama from its official website:

https://ollama.com/

### 2. Download the AI Model

Open your terminal and run:

```bash
ollama pull gemma3:1b
```

### 3. Start Ollama

Make sure Ollama is running on your computer.

The application communicates with the local Ollama API at:

```text
http://localhost:11434/api/generate
```

### 4. Run the Application

Navigate to the project directory and execute:

```bash
streamlit run src/project_st.py
```

If your main Python file is located elsewhere, update the command accordingly.

## 💡 How It Works

1. The user enters a question in the Streamlit chat interface.
2. The application sends the prompt to the local Ollama API.
3. Ollama generates a response using the selected language model.
4. The response is streamed to the interface as it is generated.
5. The conversation is automatically saved to a JSON file.
6. Users can revisit previous conversations from the sidebar.
7. Users can generate and save summaries of their conversations.

## 🎯 Learning Objectives

This project helped me practice:

- Building interactive applications with Streamlit.
- Integrating a locally running AI model.
- Sending HTTP requests to a REST API.
- Handling streamed responses.
- Managing application state with Streamlit session state.
- Reading and writing JSON and text files.
- Implementing automatic conversation persistence.
- Organizing Python code into separate modules.
- Building a chat interface with conversation history.

## 🔒 Privacy and Local Execution

The chatbot communicates with a locally running Ollama instance instead of relying on a cloud-based AI API.

Prompts and responses are processed by the local model. However, local execution alone does not guarantee that all application activity is private; privacy also depends on the model, software, and any additional services used.

## 👩‍💻 Author

Developed as a Python learning project focused on local AI, Streamlit, and chatbot development.
