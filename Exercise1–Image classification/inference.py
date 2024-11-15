import numpy as np
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.preprocessing import image
import joblib
import gradio as gr

base_model = VGG19(weights='imagenet', include_top=False)

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = base_model.predict(img_array)
    features_flattened = features.flatten()
    return features_flattened

svm_model = joblib.load("./svm_model.pkl")

def predict_animal(image_file):
    features = extract_features(image_file)
    prediction = svm_model.predict([features])[0]
    if prediction == 0:
        return "Cat 🐱"
    elif prediction == 1:
        return "Dog 🐶"

interface = gr.Interface(
    fn=predict_animal,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="Cat vs Dog Classifier",
    description="Upload an image of a cat or dog, and the model will predict whether it's a cat or a dog.",
)

interface.launch()