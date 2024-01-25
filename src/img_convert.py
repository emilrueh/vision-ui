import requests

from PIL import Image
from io import BytesIO
import base64


def image_to_base64str(image_source, file_type="JPEG"):
    if "http" in image_source or "https" in image_source:
        # Handle URL
        response = requests.get(image_source)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
        else:
            print("Failed to download image.")
            return None
    else:
        # Handle file path
        if "." in file_type:
            file_type = file_type.replace(".", "")
        if file_type == "jpg":
            file_type = "jpeg"
        image_data = image_source

    try:
        with Image.open(image_data) as image:
            buffered = BytesIO()
            # Convert to RGB if necessary
            if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
                image = image.convert("RGB")
            image.save(buffered, format=file_type.upper())
            image_bytes = buffered.getvalue()
            base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
            return f"data:image/{file_type.lower()};base64,{base64_encoded}"
    except Exception as e:
        print(f"{type(e).__name__} converting image: {e}")
        return None
