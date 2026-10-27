import streamlit as st
import utils_project
import threading
import queue
import os
import json
import uuid


# Folder for saving conversations
HISTORY_FOLDER = 'chat_history'

# Create the folder if it does not exist
os.makedirs(HISTORY_FOLDER, exist_ok=True)


def save_chat(chat_id, messages):
    file_path = os.path.join(HISTORY_FOLDER,f'{chat_id}.json')

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)


def load_chat(chat_id):
    file_path = os.path.join(HISTORY_FOLDER,f'{chat_id}.json')

    with open(file_path, 'r', encoding='utf-8') as file:
        messages = json.load(file)

    return messages


def get_saved_chats():
    chat_files = []

    for file_name in os.listdir(HISTORY_FOLDER):
        if file_name.endswith('.json'):
            chat_id = file_name.replace('.json', '')
            file_path = os.path.join(HISTORY_FOLDER,file_name)

            modified_time = os.path.getmtime(file_path)

            chat_files.append((chat_id, modified_time))

    chat_files.sort(key=lambda chat: chat[1], reverse=True)

    return [chat[0] for chat in chat_files]



with st.sidebar:
    st.title('My Chatbot')

    if st.button('➕ New Chat', use_container_width=True):
        st.session_state['chat_id'] = str(uuid.uuid4())
        st.session_state['messages'] = [{'role': 'ai', 'content': 'How Can I Help You?'}]
        st.session_state['generated_text'] = ''
        st.rerun()

    st.divider()
    st.subheader('Chat History')

    saved_chats = get_saved_chats()

    for chat_id in saved_chats:
        messages = load_chat(chat_id)

        title = 'New Chat'

        for msg in messages:
            if msg['role'] == 'user':
                title = msg['content'][:30]
                break

        if st.button(title, key=chat_id, use_container_width=True):
            st.session_state['chat_id'] = chat_id
            st.session_state['messages'] = messages
            st.session_state['generated_text'] = ''
            st.rerun()


st.title('STREAMLIT CAHTBOT')

model = 'gemma3:1b'

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'ai', 'content': 'How Can I Help You?'}
    ]
if 'chat_id' not in st.session_state:
    st.session_state['chat_id'] = str(uuid.uuid4())

if 'running' not in st.session_state:
    st.session_state['running'] = False

if 'stop_event' not in st.session_state:
    st.session_state['stop_event'] = None

if 'output_queue' not in st.session_state:
    st.session_state['output_queue'] = None

if 'response_holder' not in st.session_state:
    st.session_state['response_holder'] = None

if 'generated_text' not in st.session_state:
    st.session_state['generated_text'] = ''

if 'worker' not in st.session_state:
    st.session_state['worker'] = None

if st.button('Clear Chat', disabled=st.session_state['running']):
    st.session_state['messages'] = [
        {'role': 'ai', 'content': 'How Can I Help You?'}]
    st.rerun()

for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

if st.button('Save Chat'):
    with open('chat_history.txt', 'w', encoding='utf-8') as file:
        for msg in st.session_state['messages']:
            file.write(msg['role'] + ': ')
            file.write(msg['content'] + '\n\n')

    st.success('Chat saved successfully!')

if st.button('Summarize Chat'):

    with open('chat_history.txt', 'r', encoding='utf-8') as file:
        chat_text = file.read()

   
    summary_prompt = f"""
    You are a helpful assistant.

    Read the entire conversation carefully and summarize ALL questions
    and answers, not just the last question.

    Requirements:
    - Include every main topic discussed.
    - Explain the important information from each question and answer.
    - Include important details, explanations, and conclusions.
    - Organize the summary into separate sections when needed.
    - Write at least one paragraph for each main topic.
    - Do not skip earlier questions.
    - Do not invent information.

    Conversation:
    {chat_text}
    """

    st.write(chat_text)
    
    with st.spinner('Summarizing Chat...'):
        summary = utils_project.call_ollama_model(summary_prompt, model)

    with open('chat_summary.txt', 'w', encoding='utf-8') as file:
        file.write(summary)

    with open('chat_summary.txt', 'r', encoding='utf-8') as file:
        saved_summary = file.read()

    st.write('Text saved in file:')
    st.write(saved_summary)

    st.success('Chat summary saved successfully!')
    st.write(summary)

prompt = st.chat_input('Enter Your Question',disabled=st.session_state['running'])



def run_model(prompt, model, stop_event, output_queue, response_holder):
    utils_project.call_ollama_model_stream(prompt, model, stop_event, output_queue, response_holder)


if prompt and not st.session_state['running']:

    new_prompt = prompt + ' Describe your answer with detail and images'
   
    st.session_state['messages'].append({'role': 'user','content': prompt})
    save_chat(st.session_state['chat_id'],st.session_state['messages']) 

    st.session_state['running'] = True

    st.session_state['generated_text'] = ''
    st.session_state['stop_event'] = threading.Event()
    st.session_state['output_queue'] = queue.Queue()
    st.session_state['response_holder'] = {}

    worker = threading.Thread(
        target=run_model,
        args=(
            new_prompt,
            model,
            st.session_state['stop_event'],
            st.session_state['output_queue'],
            st.session_state['response_holder'])
         )

    st.session_state['worker'] = worker
    worker.start()

    st.rerun()


@st.fragment(run_every=0.2)
def show_response():

    if not st.session_state['running']:
        return

    stop_event = st.session_state['stop_event']
    output_queue = st.session_state['output_queue']
    response_holder = st.session_state['response_holder']

    if st.button('Stop', key='stop_model'):
        stop_event.set()

        response = response_holder.get('response')

        if response is not None:
            try:
                response.close()
            except Exception:
                pass

    finished = False

    while True:
        try:
            item = output_queue.get_nowait()
        except queue.Empty:
            break

        if item is None:
            finished = True
        else:
            st.session_state['generated_text'] += item

    st.chat_message('ai').write(st.session_state['generated_text'])

    if finished:
        st.session_state['messages'].append({'role': 'ai','content': st.session_state['generated_text']})
        
        save_chat(st.session_state['chat_id'],st.session_state['messages'])
        
        st.session_state['running'] = False
        st.rerun()

if st.session_state['running']:
    show_response()






















# import streamlit as st
# import utils_new
# import threading
# import queue

# st.title('STREAMLIT CAHTBOT')

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = [{'role' : 'ai', 'content' : 'How Can I Help You?'}]

# if st.button('Clear Chat'):
#     st.session_state['messages'] = [{'role': 'ai', 'content': 'How Can I Help You?'}]
#     st.rerun()

# for msg in st.session_state['messages']:
#     st.chat_message(msg['role']).write(msg['content'])

# prompt = st.chat_input('Enter Your Question')
# model = 'gemma3:1b'
# if prompt:

#     new_prompt = prompt +'Describe your answer with detail and images'

#     st.chat_message('user').write(prompt)
#     st.session_state['messages'].append({'role':'user', 'content':prompt})

#     with st.spinner('Genarating Response...'):
#         response = utils_new.call_ollama_model(new_prompt,model)

#     st.chat_message('ai').write(response)
#     st.session_state['messages'].append({'role':'ai', 'content':response})
