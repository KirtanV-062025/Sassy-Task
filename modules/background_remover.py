import io
from PIL import Image
from rembg import remove

def remove_background(file_stream, threshold=128):
    # Load image and convert to RGBA
    input_image = Image.open(file_stream).convert("RGBA")

    # Save image to buffer
    buffer = io.BytesIO()
    input_image.save(buffer, format="PNG")
    
    # Remove background
    output_data = remove(buffer.getvalue())

    # Post-process transparency based on threshold
    output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
    pixels = output_image.load()
    width, height = output_image.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            pixels[x, y] = (r, g, b, 0) if a < threshold else (r, g, b, 255)

    # Save to buffer and return
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return output_buffer
