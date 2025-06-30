import os
# import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt):
    try:
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            response_format="b64_json",
            size="1024x1024",
            n=1
        )

        image_base64 = result.data[0].b64_json
        data_url = f"data:image/png;base64,{image_base64}"
        return data_url
    except Exception as e:
        print("Image generation error:", e)
        return None
