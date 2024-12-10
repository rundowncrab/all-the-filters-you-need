import tensorflow as tf
import numpy as np
import cv2

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np
import io
import base64

# Initialize FastAPI
app = FastAPI()

app.mount("/basicsite", StaticFiles(directory="basicsite"), name="basicsite")

# HTML endpoint to upload images and show result
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Selector</title>
    <link rel="stylesheet" href="basicsite/body.css">
</head>
<body>
    <div class="container">
        <h1>Image Blend</h1>
        
        <!-- Image selection for Image 1 -->
        <div>
            <label for="image1">Choose Content Image:</label>
            <input type="file" id="image1" accept="image/*" onchange="loadImage(1)">
        </div>
        
        <!-- Image selection for Image 2 -->
        <div>
            <label for="image2">Choose Style Image:</label>
            <input type="file" id="image2" accept="image/*" onchange="loadImage(2)">
        </div>

        <!-- Displaying selected images -->
        <div id="imageDisplay1"></div>
        <div id="imageDisplay2"></div>
        
        <button onclick="submitImages()">Mix</button>
        
        <!-- Div to display the result -->
        <div id="result"></div>
    </div>

    <script src="basicsite/output.js"></script>
</body>
</html>

    """

# Endpoint to handle image mixing
@app.post("/mix-images/")
async def mix_images(image1: UploadFile = File(...), image2: UploadFile = File(...)):
    # Read the images as bytes
    image1_bytes = await image1.read()
    image2_bytes = await image2.read()
    image_array1 = np.frombuffer(image1_bytes, np.uint8)
    img1 = cv2.imdecode(image_array1, cv2.IMREAD_COLOR)

    image_array2 = np.frombuffer(image2_bytes, np.uint8)
    img2 = cv2.imdecode(image_array2, cv2.IMREAD_COLOR)

    mix_image = give_output(img1, img2)
    image = Image.fromarray(mix_image)
 
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    mix_image_64 = base64.b64encode(img_byte_arr.read()).decode('utf-8')

    # Return the mixed image as base64 and a success message
    return {"blended_image": mix_image_64, "message": "Images modified successfully!"}


def give_output(content_image, style_image):
    content_image = np.asarray(content_image, dtype=np.float32)[np.newaxis, ...] / 255.0
    style_image = np.asarray(style_image, dtype=np.float32)[np.newaxis, ...] / 255.0
    style_image = tf.image.resize(style_image, (256, 256))

    model= tf.keras.models.load_model("model")
    stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]*255.0
    out= np.asarray(stylized_image, dtype=np.uint8)[0]
    return out
