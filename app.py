from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)\


@app.route('/upload',methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return f"File uploaded successfully: {file.filename}"
    return render_template('upload.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    image = request.files['photo']
    image.save('static/temp.jpg')

    # Stub for OCR result
    extracted_data = {
        'distributor': 'Stub Distilleries',
        'invoice_number': 'INV1234',
        'brand': 'Royal Stag',
        'qty': '12',
        'rate': '180'
    }

    return render_template('review.html', data=extracted_data)




if __name__ == '__main__':
    app.run(debug=True)
