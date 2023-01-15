import os
import openai
import ratelimit
import re

# extract the OpenAI API key and endpoint as environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

def read_file(file_path):
    """
    Reads the file located at file_path and returns its contents as a string
    """
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def process_text(text):
    """
    Processes the text by removing lines containing "-->" and splitting it into a list of strings,
    each string is a block of "block_size" sentences
    """
    text = re.sub(r'^.*-->.*$', '', text, flags=re.MULTILINE)
    text = text.split('.')
    text_list = []
    block_size = 30
    for i in range(0, len(text), block_size):
        temp = ''.join(text[i:i+block_size])
        text_list.append(temp)
    text_list.pop(0)
    return text_list

def summarize_text(text):
    """
    Sends a request to the OpenAI API to get a summary of the text
    """
    prompt = f"{text}\n\nTl;dr"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.1,
        max_tokens=800,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['text']

# rate limit API requests to 1 request per 3 seconds
@ratelimit.rate_limited(1, 3)
def get_summary(text_list):
    """
    For each element in text_list, calls the summarize_text function and writes the results to a file
    """
    output = []
    for elem in text_list:
        try:
            summary = summarize_text(elem)
            summary = summary.split('.')
            for item in summary:
                if ':' not in item:
                    if item.strip():
                        output.append(item + '.')
                        print("item: " + item)
        except Exception as e:
            print(f"Error: {e}")
    with open(f'output_file.txt', 'w') as f:
        for line in output:
            f.write(f"{line}")

if __name__ == '__main__':
    file_path = f'.\\path\\filename.txt'
    text = read_file(file_path)
    text_list = process_text(text)
    get_summary(text_list)
