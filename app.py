from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    qr_type = request.form.get('type')

    # Gather data based on selection
    if qr_type == 'text':
        data = request.form.get('text')
    elif qr_type == 'url':
        data = request.form.get('url')
    elif qr_type == 'email':
        email = request.form.get('email')
        data = f"mailto:{email}"
    elif qr_type == 'wifi':
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        encryption = request.form.get('encryption')
        data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    else:
        return "Invalid type", 400

    # Generate QR
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)


def escape_wifi_text(text):
    return text.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:').replace('"', '\\"')

ssid = escape_wifi_text(ssid)
password = escape_wifi_text(password)
data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
