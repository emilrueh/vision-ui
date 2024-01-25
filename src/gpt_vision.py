from openai import OpenAI
from dotenv import load_dotenv
import os


def init_openai_client(raw_api_key=None, dotenv_key=None):
    load_dotenv()

    api_key = os.getenv(dotenv_key) if dotenv_key and dotenv_key != "OPENAI_API_KEY" else raw_api_key

    return OpenAI(api_key=api_key)


client = init_openai_client()


def view_image(images_in_base64str: list, prompt, max_tokens=300):
    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        },
    ]

    for img in images_in_base64str:
        if img is None:
            continue
        messages[0]["content"].append(
            {
                "type": "image_url",
                "image_url": {"url": img},
            },
        )

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
