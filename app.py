from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

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
