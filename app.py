from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)
model = load_model('vgg16_leukemia.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']  

    filepath = os.path.join('static/uploads', file.filename)
    os.makedirs('static/uploads', exist_ok=True)
    file.save(filepath)

    image = load_img(filepath, target_size=(224, 224)).convert('RGB')
    image = np.expand_dims(img_to_array(image) / 255.0, axis=0)

    prediction = model.predict(image)
    class_index = np.argmax(prediction)
    confidence = np.max(prediction)

    classes = ['Benign', 'Early', 'Pre', 'Pro']
    return jsonify({
        'result': {
            'class': classes[class_index],
            'confidence': f"{confidence * 100:.2f}%"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
