from flask import Flask, render_template,request,jsonify,redirect,url_for,session
import base64
from datetime import datetime
import json
import os

import torch 
import re 

from transformers import AutoTokenizer, ViTFeatureExtractor, VisionEncoderDecoderModel 
from PIL import Image
  

device='cpu'
encoder_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
decoder_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
model_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
feature_extractor = ViTFeatureExtractor.from_pretrained(encoder_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(decoder_checkpoint)
model = VisionEncoderDecoderModel.from_pretrained(model_checkpoint).to(device)


def caption_this_image(image,max_length=64, num_beams=4):
  image=Image.open(image)
  image = image.convert('RGB')
  image = feature_extractor(image, return_tensors="pt").pixel_values.to(device)
  clean_text = lambda x: x.replace('<|endoftext|>','').split('\n')[0]
  caption_ids = model.generate(image, max_length = max_length)[0]
  caption_text = clean_text(tokenizer.decode(caption_ids))
  return caption_text 




app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template("home.html")
@app.route('/home')
def home():
    return render_template('home.html')
 
# File path to store user details
USER_DATA_FILE = 'user_data.json'

# Helper function to load user data from file
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Helper function to save user data to file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract user details from form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Load existing user data
        user_data = load_user_data()

        # Check if username or email already exists
        if username in user_data or email in (user['email'] for user in user_data.values()):
            return 'Username or email already exists. Please choose a different one.'

        # Add new user data
        user_data[username] = {'email': email, 'password': password}

        # Save updated user data
        save_user_data(user_data)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract user credentials from form
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Load user data
        user_data = load_user_data()

        # Check if username or email exists and password matches
        for username, user in user_data.items():
            if (user['email'] == username_or_email or username == username_or_email) and user['password'] == password:
                session['username'] = username  # Store username in session
                return redirect(url_for('home'))

        return render_template('login.html')

    return render_template('login.html')  


@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open('messages.txt', 'a') as file:
            file.write(f'{timestamp} - Name: {name}, Email: {email}, Message: {message}\n')

        return redirect(url_for('home'))
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    # Receive the image data as JSON
    data = request.json
    
    # Decode the Base64-encoded image data
    encoded_image = data['image']
    image_data = base64.b64decode(encoded_image.split(',')[1])
    
    # Save the decoded image data to the server
    filename = 'image.jpg'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)
    
    # Generate the caption for the image
    generated_caption =caption_this_image(filepath)
    
    # Delete the uploaded image file after generating the caption
    os.remove(filepath)
    
    return jsonify(caption=generated_caption)
if __name__ == '__main__':
    app.run(debug=True)
