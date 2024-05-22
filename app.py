import pickle
import cv2
from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from img2vec_pytorch import Img2Vec # type: ignore
import tensorflow as tf

app = Flask(__name__)

# Load SVM model
with open("svm_model2.pkl", "rb") as f:
    svm_model = pickle.load(f)

# Load CNN model
try:
    cnn_model = tf.keras.models.load_model("cnn_cv8.keras")
except FileNotFoundError:
    print("CNN model file not found.")
    cnn_model = None

# Load Img2Vec model
img2vec = Img2Vec(model='resnet-18')

# Define potato classes
potato_classes = ['Potato_EarlyBlight', 'Potato_healthy', 'Potato_LateBlight', 'Not_Potato']

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/classify', methods=['POST'])
def classify():
    # Get the uploaded image file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Read the image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Resize the image
        image = cv2.resize(image, (264, 264))
        # Convert to PIL Image
        image_pil = Image.fromarray(image)
        # Extract features using Img2Vec
        features = img2vec.get_vec(image_pil).reshape(1, -1)
        # Predict the class label using SVM model
        predicted_class_index_svm = svm_model.predict(features)[0]
        predicted_class_svm = potato_classes[predicted_class_index_svm]
        # Predict the class label using CNN model if available
        predicted_class_cnn = None
        if cnn_model:
            # Assuming the CNN model expects images of size (64, 64, 3)
            image_for_cnn = cv2.resize(image, (64, 64)) / 255.0
            predicted_class_cnn_index = np.argmax(cnn_model.predict(np.expand_dims(image_for_cnn, axis=0)))
            predicted_class_cnn = potato_classes[predicted_class_cnn_index]
        # Pass the image path and prediction results to the result page
        image_path = request.form.get('image_path')
        return render_template('result.html', predicted_class_svm=predicted_class_svm, predicted_class_cnn=predicted_class_cnn, image_path=image_path)
    else:
        return render_template('upload23.html', error="No file selected.")

from io import BytesIO
import base64
@app.route('/classify_camera', methods=['POST'])
def classify_camera():
    image_data = request.form['image_data']
    if image_data:
        # Decode the image data
        image_data = image_data.split(",")[1]
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        # Convert to RGB
        image = image.convert("RGB")
        # Resize the image
        image = image.resize((264, 264))
        # Extract features using Img2Vec
        features = img2vec.get_vec(image).reshape(1, -1)
        # Predict the class label using SVM model
        predicted_class_index_svm = svm_model.predict(features)[0]
        predicted_class_svm1 = potato_classes[predicted_class_index_svm]
        # Predict the class label using CNN model if available
        predicted_class_cnn1 = None
        if cnn_model:
            # Assuming the CNN model expects images of size (128, 128, 3)
            image_for_cnn = image.resize((64, 64))
            image_for_cnn = np.array(image_for_cnn) / 255.0
            predicted_class_cnn_index = np.argmax(cnn_model.predict(np.expand_dims(image_for_cnn, axis=0)))
            predicted_class_cnn1 = potato_classes[predicted_class_cnn_index]
        # Pass the image data and prediction results to the camera result page
        return render_template('camera_result.html', predicted_class_svm1=predicted_class_svm1, predicted_class_cnn1=predicted_class_cnn1, image_path=image_data)
    else:
        return render_template('upload23.html', error="No file selected.")


@app.route('/upload23')
def upload():
    return render_template('upload23.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('aboutus.html')

@app.route('/treatment')
def treatment_page():
    return render_template('treatment.html')


@app.route('/treatment/earlyblight')
def earlyblight_treatment():
     return render_template('earlyblight.html')

@app.route('/treatment/lateblight')
def lateblight_treatment():
    return render_template('lateblight.html')

@app.route('/click')
def click():
    return render_template('imgCapture.html')


if __name__ == '__main__':
    app.run(debug=True)
