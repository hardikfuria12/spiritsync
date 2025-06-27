from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace this with your actual ngrok public URL
NGROK_BACKEND_URL = 'https://xyz123.ngrok.io/upload'


@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@app.route('/submit', methods=['POST'])
def submit():
    file = request.files.get('file')
    if file:
        # Directly forward the file to the backend server without saving locally
        files = {
            'file': (file.filename, file.stream, file.mimetype)
        }
        try:
            response = requests.post(NGROK_BACKEND_URL, files=files)
            return f"File forwarded to backend. Response: {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Failed to reach backend: {e}", 500

    return "No file received", 400


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
