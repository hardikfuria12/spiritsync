from flask import Flask, render_template, request, redirect, url_for
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
    username = request.form.get('username')
    password = request.form.get('password')

    if not file:
        print("🚫 No file received in request.files")
        return "No file received", 400

    print(f"📦 Received file: {file.filename}, type: {file.content_type}")

    files = {
        'file': (file.filename, file.stream, file.mimetype)
    }

    try:
        forward_url = f"{NGROK_BACKEND_URL}/receive_login"
        response = requests.post(
            forward_url,
            data={
                'username': username,
                'password': password
            },
            files=files
        )

        if response.status_code != 200:
            return f"Backend error: {response.text}", 500

        data = response.json()
        return render_template("result.html", user_id=data['user_id'], table_html=data['table_html'])

    except requests.exceptions.RequestException as e:
        print("❌ Failed to reach backend:", e)
        return f"Failed to reach backend: {e}", 500

@app.route('/review')
def review():
    user_id = request.args.get('user_id', 'unknown')
    return f"✅ Review page placeholder for user: {user_id}"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
