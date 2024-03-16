from openai import OpenAI
from dotenv import load_dotenv
import os


def init_openai_client(raw_api_key=None, dotenv_key=None):
    load_dotenv()

    api_key = os.getenv(dotenv_key) if dotenv_key and dotenv_key != "OPENAI_API_KEY" else raw_api_key

    return OpenAI(api_key=api_key)


# auth openai
client = init_openai_client()


def view_image(images_in_base64str: list, user_prompt, system_prompt=None, max_tokens=300):
    messages = []
    if system_prompt:
        messages.append(
            {"role": "system", "content": system_prompt},
        )
    messages.append(
        {
            "role": "user",
            "content": [{"type": "text", "text": user_prompt}],
        },
    )

    for img in images_in_base64str:
        if img is None:
            continue
        messages[1]["content"].append(
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
