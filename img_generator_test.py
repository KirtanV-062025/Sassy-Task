# from dotenv import load_dotenv
# from openai import OpenAI
# import base64
# import os
# # Load environment variables
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# prompt = """    
# A children's book drawing of a veterinarian using a stethoscope to 
# listen to the heartbeat of a baby otter.
# """

# result = client.images.generate(
#     model="gpt-image-1",
#     prompt=prompt
# )

# image_base64 = result.data[0].b64_json
# image_bytes = base64.b64decode(image_base64)

# # Save the image to a file
# with open("otter.png", "wb") as f:
#     f.write(image_bytes)


import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


user_prompt = input("Enter an image prompt: ")


try:
    result = client.images.generate(
        model="dall-e-3", 
        prompt=user_prompt,
        response_format="b64_json", 
        size="1024x1024",
        n=1
    )

    # Decode the base64 image and save it
    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    filename = "generated_image.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"Image saved as: {filename}")

except Exception as e:
    print("Error generating image:", str(e))
