# make a main function with input arguments using the click library

import click
import whisper
from ollama import Client
import os
import json

@click.command()
@click.argument('filename')
def main(filename):
    print(f'Processing {filename}')

    transcript_filename = filename + '_transcript.json'

    if not os.path.exists(transcript_filename):
        print("Analysing audio file")
        text = speech_to_text(filename)
        # save the text to a file
        with open(transcript_filename, 'w') as f:
            json.dump(text, f, indent=4)
    else:
        print("Transcript found, loading existing transcript")
        with open(transcript_filename, 'r') as f:
            text = json.load(f)
    
    print("Summarizing text")
    response = make_summary(text)
    # save the summary to a file
    with open(filename + '_summary.md', 'w') as f:
        f.write(response['message']['content'])
    print("Done!")


def speech_to_text(filename, language=None):
    """
    Function to convert speech to text using openAI Whisper API

    Parameters
    ----------
    filename : str
        The filename of the audio file to convert
    language : str
        The language of the audio file
    
    Returns
    -------
    str
        The text of the audio file
    """
    model = whisper.load_model("turbo")
    if language is not None:
        model.set_language(language)
    result = model.transcribe(os.path.abspath(filename))
    # print(json.dumps(result, indent=4))
    return result

def make_summary(text):
    """
    Function to make a summary of the text

    Parameters
    ----------
    text : str
        The text to summarize
    
    Returns
    -------
    str
        The summary of the text
    """
    prompt = "The following text is a transcription of an audio fragment from a meeting. Summarize the text as formal minutes, including action points. Text: " + text["text"]
    if text['language'] == 'nl':
        prompt = "De volgende tekst is een transcriptie van een audiofragment van een vergadering. Maak een samenvatting van de tekst als formele notulen, inclusief actiepunten. Tekst: " + text["text"]


    client = Client(host='http://localhost:11434')
    response = client.chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': prompt
    },
    ])
    # print(json.dumps(response, indent=4))
    return response

if __name__ == '__main__':
    main()