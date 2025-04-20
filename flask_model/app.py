#flask_model/app.py
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array


import requests
from io import BytesIO
import cv2

app = Flask(__name__)

# Load the Siamese model with custom objects
try:
    model_path = "epoch-05-val_loss-0.0026.h5"
    model = tf.keras.models.load_model(model_path, compile=False)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


def load_image_from_url(image_url, target_size=(105, 105)):
    """
    Loads an image from a URL, preprocesses it for a Siamese network by resizing, 
    normalizing, converting to 3 channels, and adding a batch dimension.
    """
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Load image as grayscale and resize it
        img = load_img(BytesIO(response.content), color_mode="grayscale", target_size=target_size)
        
        # Convert image to array and normalize
        img_array = img_to_array(img) / 255.0
        
        # Convert to 3 channels (stack grayscale image 3 times)
        img_array = np.stack([img_array.squeeze()] * 3, axis=-1)  # Remove extra channel and stack
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        raise ValueError(f"Error loading or preprocessing image from URL {image_url}: {e}")


@app.route("/verify-signature", methods=["POST"])
def verify_signature():
    if model is None:
        return jsonify({"error": "Model not loaded. Cannot process requests."}), 500

    try:
        # print("Received verification request.")
        # Get JSON payload
        data = request.get_json()
        # print("Request data:", data)

        # Extract relative file paths
        original_path = data.get("original_signature_path")
        verification_path = data.get("uploaded_signature_path")

        # Validate paths
        if not original_path or not verification_path:
            return jsonify({"error": "Both file paths must be provided."}), 400

        # Read and preprocess images
        try:
            image1 = load_image_from_url(original_path)
            image2 = load_image_from_url(verification_path)
            # print("Images loaded and preprocessed successfully.")
        except ValueError as e:
            print(f"Image loading error: {e}")
            return jsonify({"error": str(e)}), 400

        # Predict similarity
        similarity_score = model.predict([image1, image2])[0][0]
        # print(f"Similarity score calculated: {similarity_score}")

        # Determine if the signature is real or forged
        result = "Real" if similarity_score >= 0.5 else "Forged"
        
        # Return similarity score and result
        return jsonify({
            "result": result,
            "similarity_score": float(similarity_score)
        })

    except Exception as e:
        print(f"Error during verification: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
