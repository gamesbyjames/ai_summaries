import os
import openai
import urllib.request
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
    Processes the input text by removing any unwanted characters and splitting it into lines
    """
    text = re.sub(r'[^\w\s\n]', '', text) # remove any non-alphanumeric characters
    lines = text.split('.')
    return lines

def create_images(lines, output_path):
    """
    Takes in a list of lines and creates an image for each one using the OpenAI API
    """
    image_count = 0
    for line in lines:
        try:
            result = openai.Image.create(
                prompt=line,
                n=1,
                size="1024x1024"
            )
            image_url = result['data'][0]['url']
            # download the image and save it to the output_path directory
            urllib.request.urlretrieve(image_url, os.path.join(output_path, "image_{}.jpg".format(image_count)))
            image_count += 1
            print(line)
            print(image_url)
        except Exception as e:
            print("An error occurred while creating image: {}".format(e))

if __name__ == '__main__':
    file_path = './path/input.txt'
    output_path = './path/images/'

    # read the file, process the text and create images
    text = read_file(file_path)
    lines = process_text(text)
    create_images(lines, output_path)
