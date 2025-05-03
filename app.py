from flask import Flask, render_template, request, url_for
from PIL import Image, ImageOps, ImageFilter
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder 'uploads' ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def deteksi_wajah(input_path, output_path):
    # Pastikan path ke file haarcascade_frontalface_default.xml benar
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        raise Exception("File haarcascade_frontalface_default.xml tidak ditemukan.")
    
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imwrite(output_path, img)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_path = None
    processed_path = None

    if request.method == 'POST':
        file = request.files['image']
        effect = request.form.get('effect')

        if file and allowed_file(file.filename):
            filename = file.filename
            original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(original_file_path)

            processed_filename = 'processed_' + filename
            processed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

            if effect == 'grayscale':
                img = Image.open(original_file_path)
                processed_img = ImageOps.grayscale(img)
                processed_img.save(processed_file_path)

            elif effect == 'blur':
                img = Image.open(original_file_path)
                processed_img = img.filter(ImageFilter.GaussianBlur(4))
                processed_img.save(processed_file_path)

            elif effect == 'rotate':
                img = Image.open(original_file_path)
                processed_img = img.rotate(90)
                processed_img.save(processed_file_path)

            elif effect == 'mirror':
                img = Image.open(original_file_path)
                processed_img = ImageOps.mirror(img)
                processed_img.save(processed_file_path)

            elif effect == 'face_detect':
                deteksi_wajah(original_file_path, processed_file_path)

            original_path = url_for('static', filename=f'uploads/{filename}')
            processed_path = url_for('static', filename=f'uploads/{processed_filename}')

    return render_template('index.html', original_path=original_path, processed_path=processed_path)

# Jangan jalankan app.run di PythonAnywhere
# Hapus atau komentari baris ini jika sudah di PythonAnywhere
# if __name__ == '__main__':
#     app.run(debug=True)
