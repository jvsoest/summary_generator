# make a main function with input arguments using the click library

import click
import whisper
import os

@click.command()
@click.argument('filename')
def main(filename):
    print(f'Processing {filename}')
    speech_to_text(filename)

def speech_to_text(filename):
    """
    Function to convert speech to text using openAI Whisper API

    Parameters
    ----------
    filename : str
        The filename of the audio file to convert

    Returns
    -------
    str
        The text of the audio file
    """
    model = whisper.load_model("turbo")
    result = model.transcribe(os.path.abspath(filename))
    print(result["text"])

if __name__ == '__main__':
    main()