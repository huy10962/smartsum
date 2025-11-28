from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# 1. Khởi tạo ứng dụng Flask
app = Flask(__name__)

# 2. Cấu hình kết nối Database PostgreSQL
# Công thức: postgresql://USER:PASSWORD@HOST:PORT/DB_NAME?options=...
# Mình đã thêm đoạn "?options=-c%20timezone=UTC" để tránh lỗi Timezone bạn gặp lúc nãy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/postgres?options=-c%20timezone=UTC'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Khởi tạo đối tượng Database
db = SQLAlchemy(app)

# 4. Tạo một đường dẫn (Route) để test kết nối
@app.route('/')
def check_connection():
    try:
        # Thử gửi một câu lệnh SQL đơn giản tới DB
        db.session.execute(text('SELECT 1'))
        return jsonify({
            "status": "success", 
            "message": "Kết nối Database THÀNH CÔNG! Flask và PostgreSQL đã bắt tay nhau."
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": "Kết nối THẤT BẠI", 
            "error_details": str(e)
        })

# 5. Chạy server
if __name__ == '__main__':
    print("Server đang khởi động...")
    app.run(debug=True, port=5000)