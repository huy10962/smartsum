from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from sqlalchemy import inspect

# 1. Khởi tạo ứng dụng Flask
app = Flask(__name__)

# 2. Cấu hình kết nối Database PostgreSQL
# (Giữ nguyên cấu hình chuẩn của bạn)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/postgres?options=-c%20timezone=UTC'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Khởi tạo đối tượng Database
db = SQLAlchemy(app)

# --- PHẦN 4: ĐỊNH NGHĨA BẢNG (MODELS) ---
# Phần này thay thế cho việc gõ lệnh CREATE TABLE trong DBeaver

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Tạo mối quan hệ để dễ truy vấn sau này
    summaries = db.relationship('Summary', backref='owner', lazy=True)

class Summary(db.Model):
    __tablename__ = 'summaries'
    id = db.Column(db.Integer, primary_key=True)
    # Khóa ngoại nối sang bảng users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text)
    action_type = db.Column(db.String(20), default='SUMMARIZE')
    model_name = db.Column(db.String(50), default='facebook/bart-large-cnn')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- PHẦN 5: TỰ ĐỘNG TẠO BẢNG & CHẠY SERVER ---

# Hàm này chạy 1 lần khi server bật lên để kiểm tra DB
with app.app_context():
    try:
        db.create_all()
        print("✅ Đã khởi tạo các bảng thành công!")
        
        # --- ĐOẠN CODE MỚI THÊM ĐỂ SOI BẢNG ---
        inspector = inspect(db.engine)
        cac_bang = inspector.get_table_names()
        print(f"👀 Danh sách bảng hiện có trong Database: {cac_bang}")
        # --------------------------------------
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

@app.route('/')
def check_connection():
    return jsonify({
        "status": "success", 
        "message": "Server SmartSum đang chạy! Các bảng dữ liệu đã sẵn sàng."
    })

if __name__ == '__main__':
    print("Server đang khởi động...")
    app.run(debug=True, port=5000)