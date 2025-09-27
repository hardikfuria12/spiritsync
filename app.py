from flask import Flask, render_template, request, jsonify
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
        print("🚫 No file received")
        return "No file received", 400

    print(f"📦 Received file: {file.filename}, type: {file.content_type}")

    files = {
        'file': (file.filename, file.stream, file.mimetype)
    }

    try:
        response = requests.post(
            f"{NGROK_BACKEND_URL}/receive_login",
            data={'username': username, 'password': password},
            files=files
        )

        if response.status_code != 200:
            return f"Backend error: {response.text}", 500

        data = response.json()

        if data['type'] == "onboard":
            return render_template(
                "create_family.html",
                user_id=data['user_id'],
                session=data['session'],
                families=data['families'],
                pending_code_table=data['pending_code_table'],
            )

        elif data['type'] == "purchase_pending":
            return render_template(
                "accept_purchase.html",
                user_id=data['user_id'],
                # date = data['date'],
                # stats = data['stats'],
                session=data['session'],
                file_path=data['file_path'],
                pending_purchase_table=data['pending_purchase_data'],
            )

        elif data['type'] == "regular":
            return render_template(
                "result.html",
                user_id=data['user_id'],
                date = data['date'],
                stats = data['stats'],
                session=data['session'],
                table_html=data['table_html'],
                sales_clean_html=data['sales_clean_html'],
                sales_dirty_html=data.get('sales_dirty_html'),
            )

        else:
            return f"Unknown response type: {data['type']}", 500

    except requests.exceptions.RequestException as e:
        print("❌ Backend unreachable:", e)
        return f"Backend unreachable: {e}", 500

@app.route('/save_family', methods=['POST'])
def save_family():
    try:
        payload = request.get_json()
        print("📤 Forwarding family data to backend:", payload)

        response = requests.post(f"{NGROK_BACKEND_URL}/save_family", json=payload)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return f"Backend error: {response.text}", 500
    except Exception as e:
        print("❌ Error in save_family route:", e)
        return f"Server error: {e}", 500

@app.route('/upload_excise', methods=['POST'])
def upload_excise():
    try:
        payload = request.get_json()
        print("📤 Forwarding excise upload to backend:", payload)

        response = requests.post(f"{NGROK_BACKEND_URL}/upload_excise", json=payload)

        if response.status_code == 200:
            data = response.json()

            if data.get("type") == "success":
                # Successful upload — show upload.html with alert
                return render_template("upload.html", success=True)

            else:
                # Dirty data — return result.html again
                return render_template(
                    "result.html",
                    user_id=data['user_id'],
                    date=data['date'],
                    session=data['session'],
                    stats=data['stats'],
                    table_html=data['table_html'],
                    sales_clean_html=data['sales_clean_html'],
                    sales_dirty_html=data['sales_dirty_html'],
                )
        else:
            return f"Backend error: {response.text}", 500
    except Exception as e:
        print("❌ Error in /upload_excise:", e)
        return f"Server error: {e}", 500

@app.route("/accept_purchase", methods=["POST"])
def accept_purchase():
    data = request.get_json()

    # forward to backend
    try:
        resp = requests.post(f"{NGROK_BACKEND_URL}/accept_purchase", json=data)
        response_data = resp.json()
        success = response_data.get("success", False)
        res_type = response_data.get("type", "unknown")
        if success and res_type == "regular":
            return render_template(
                "result.html",
                user_id=data['user_id'],
                date = data['date'],
                stats = data['stats'],
                session=data['session'],
                table_html=data['table_html'],
                sales_clean_html=data['sales_clean_html'],
                sales_dirty_html=data.get('sales_dirty_html'),
            )
        else:
            error = response_data.get("error", "Unknown error")
            return jsonify({"error": f"Failed to accept purchases. {error}", }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
