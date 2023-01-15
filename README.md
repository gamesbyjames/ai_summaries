# ai_summaries

text_summarizer.py: Reads a text file at ./path/input.txt and creates a summary using gpt-3 at ./path/output.txt. The "block_size" variable is used to specify how many lines to send to gpt-3 at a time.

image_creator.py: Reads a file at ./path/input.txt and for each line in the file, requests DALL-E 2 to create an image based on that line as a prompt. The output images are stored at ./path/images/image_x.jpg were x is the line number for that image.
