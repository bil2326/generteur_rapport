import os
import base64
from dotenv import load_dotenv
from mistralai import Mistral
from groq import Groq
import json
from prompt import * 
load_dotenv()



def get_text_from_vocal(vocal_path):
    client = Groq(api_key=os.environ["GROQ_KEY"])
    with open(vocal_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            prompt="Transcris ce fichier audio de manière intégralement fidèle...",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language="fr",
            temperature=0.0
        )
    return transcription.text

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erreur lors de l'encodage de l'image : {e}")
        return None

def build_content(image_path, vocal_path):
    base64_image = encode_image(image_path)
    transcription_text = get_text_from_vocal(vocal_path)
    api_key = os.environ["MISTRAL_KEY"]
    client = Mistral(api_key=api_key)

    messages = [
        {"role": "system", "content": CONTEXT},
        {"role": "user", "content": [
            {"type": "text", "text": get_constat_prompt(transcription_text)},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
        ]}
    ]

    response = client.chat.complete(
        model="pixtral-12b-2409",
        messages=messages,
        response_format={"type": "json_object"}
    )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)
