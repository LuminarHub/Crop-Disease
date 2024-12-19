import tensorflow as tf
import numpy as np
from PIL import Image
import os

class_labels = [
    "Apple Scab",
    "Apple Black Rot",
    "Apple Cedar Apple Rust",
    "Apple Healthy",
    "Blueberry Healthy",
    "Cherry (Including Sour) Powdery Mildew",
    "Cherry (Including Sour) Healthy",
    "Corn (Maize) Cercospora Leaf Spot Gray Leaf Spot",
    "Corn (Maize) Common Rust",
    "Corn (Maize) Northern Leaf Blight",
    "Corn (Maize) Healthy",
    "Grape Black Rot",
    "Grape Esca (Black Measles)",
    "Grape Leaf Blight (Isariopsis Leaf Spot)",
    "Grape Healthy",
    "Orange Haunglongbing (Citrus Greening)",
    "Peach Bacterial Spot",
    "Peach Healthy",
    "Pepper Bell Bacterial Spot",
    "Pepper Bell Healthy",
    "Potato Early Blight",
    "Potato Late Blight",
    "Potato Healthy",
    "Raspberry Healthy",
    "Soybean Healthy",
    "Squash Powdery Mildew",
    "Strawberry Leaf Scorch",
    "Strawberry Healthy",
    "Tomato Bacterial Spot",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold",
    "Tomato Septoria Leaf Spot",
    "Tomato Spider Mites Two-Spotted Spider Mite",
    "Tomato Target Spot",
    "Tomato Yellow Leaf Curl Virus",
    "Tomato Tomato Mosaic Virus"
]


model_path = os.path.join(os.getcwd(), 'main','Crop_disease.h5')


filename='D:/Projects/Parkingson_s/Respiratory/Test Data/Bacterial Pneumonia.jpeg'

def load_and_prep_image(filename, img_shape=128):

    img = Image.open(filename)
    img = img.convert('RGB')
    # Resize the image
    img = img.resize((img_shape, img_shape))
    # Convert the image to a numpy array
    img = np.array(img) / 255.0  # Normalize to [0,1]
    # Add batch dimension (model expects shape (batch_size, height, width, channels))
    img = np.expand_dims(img, axis=0)
    return img



def predicted_class(class_labels,model_path,test_image):
    saved_model = tf.keras.models.load_model(model_path)
    # Make a prediction on our custom image
    prediction=saved_model.predict(test_image)
    predicted_class = np.argmax(prediction, axis=-1)
    # Map the predicted class index to the class label
    predicted_class_label = class_labels[predicted_class[0]]
    print(f"Predicted class: {predicted_class_label}")
    return predicted_class_label

# predicted_class(class_labels,model_path,test_image)