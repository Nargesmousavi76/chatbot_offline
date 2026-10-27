import requests
import json
import threading
import time
import queue

def call_ollama_model(prompt, model, stream=False):
    url = 'http://localhost:11434/api/generate'

    params = {
        'prompt' : prompt,
        'model' : model,
        'stream' : stream
        }

    payload = json.dumps(params)

    response = requests.post(url, data=payload,
                             headers={'content_Type' : 'application/json'})

    if response.status_code != 200:
        return 'ERROR'

    else:
        response = response.json()['response']
        return response

def call_ollama_model_stream(
    prompt, model, stop_event, output_queue, response_holder):
    url = 'http://localhost:11434/api/generate'

    params = {
        'prompt': prompt,
        'model': model,
        'stream': True
    }

    response = None

    try:
        response = requests.post(
            url,
            json=params,
            stream=True,
            timeout=(30, 120)
        )

        response_holder['response'] = response

        if stop_event.is_set():
            response.close()
            return

        response.raise_for_status()

        for line in response.iter_lines():
            if stop_event.is_set():
                break

            if line:
                data = json.loads(line)
                text = data.get('response', '')

                if text:
                    output_queue.put(text)

                if data.get('done'):
                    break

    except requests.RequestException as error:
        if not stop_event.is_set():
            output_queue.put(f'\nError: {error}')

    except json.JSONDecodeError:
        output_queue.put('\nError: Invalid response from Ollama')

    finally:
        if response is not None:
            response.close()

        output_queue.put(None)
####################################################
if __name__ == '__main__':
    model = 'gemma3:1b'
    prompt = input('Enter Your Question: ')
    response = call_ollama_model(prompt, model)
    print(f'result : {response}')