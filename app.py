from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

app = Flask(__name__)

# Load the trained model
model = load_model('vgg16_leukemia.h5')

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess the image
        try:
            image = load_img(filepath, target_size=(224, 224))  # Adjust as per model input
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0) / 255.0

            # Predict
            predictions = model.predict(image)
            class_index = np.argmax(predictions)
            confidence = np.max(predictions)

            # Map class indices to stage names
            classes = ['Benign', 'Early', 'Pre', 'Pro']
            result = {
                'class': classes[class_index],
                'confidence': f"{confidence * 100:.2f}%"
            }
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': f"Error processing image: {str(e)}"})
    else:
        return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True)
