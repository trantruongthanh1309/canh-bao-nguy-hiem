from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask import jsonify
app = Flask(__name__)
from flask import request
import os
from datetime import datetime
import random

# Tạm thời lưu cảnh báo trong bộ nhớ (chưa dùng DB)
alerts = []

@app.route('/')
def index():
    return render_template('index.html', alerts=alerts)

@app.route('/alert', methods=['POST'])
def alert():
    try:
        lat = float(request.form.get('lat'))
        lng = float(request.form.get('lng'))
        time = datetime.now().strftime('%H:%M:%S')

        alerts.append({
            'lat': lat,
            'lng': lng,
            'time': time
        })
    except:
        pass  # Có thể thêm xử lý lỗi nếu người dùng nhập sai

    return redirect('/')


@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts)

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

def detect_scream(path):
    """
    Hàm giả định nhận diện tiếng hét.
    Trả về True ngẫu nhiên (tạm thời).
    """
    # Sau này bạn có thể tích hợp model thật tại đây
    return random.choice([True, False])  # Giả lập: 50% cơ hội có tiếng hét

@app.route('/detect_audio', methods=['POST'])
def detect_audio():
    audio = request.files['audio']
    filename = f"audio_{datetime.now().strftime('%H%M%S')}.wav"
    path = os.path.join("static/audios", filename)
    audio.save(path)

    # Ở đây: chạy mô hình phát hiện tiếng hét (giả sử detect_scream(path) trả True)
    if detect_scream(path):
        # Gửi cảnh báo tự động từ toạ độ gần đây nhất (hoặc yêu cầu cập nhật GPS)
        alerts.append({
            'lat': 16.047079,
            'lng': 108.206230,
            'time': datetime.now().strftime('%H:%M:%S'),
            'note': 'Tự động gửi do phát hiện tiếng hét'
        })
    return '', 204

@app.route('/alert_audio', methods=['POST'])
def alert_audio():
    audio = request.files['audio']
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    time = datetime.now().strftime('%H:%M:%S')
    os.makedirs('static/audio', exist_ok=True)
    filename = f"audio_{time.replace(':', '-')}.webm"
    path = os.path.join('static/audio', filename)
    audio.save(path)
    alerts.append({
        'lat': float(lat),
        'lng': float(lng),
        'time': time,
        'audio': f'/static/audio/{filename}'  
    })

    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0')
