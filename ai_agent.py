import base64
import requests
import os
import io
from mistralai import Mistral

from dotenv import load_dotenv
load_dotenv()

from prompt import *


def format_image_into_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")  # ou "PNG"
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_base64




def build_constat(image, user_input_2_section):
    base64_image = format_image_into_base64(image)

    model = "pixtral-12b-2409"
    load_dotenv()

    api_key = os.environ["MISTRAL_KEY"]
    client = Mistral(api_key=api_key)


    messages = [
        {
            "role": "system",
            "content": CONTEXT
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": get_constat_prompt(user_input_2_section)
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}" 
                }
            ]
        }
    ]

    # Get the chat response
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )


    return chat_response.choices[0].message.content








