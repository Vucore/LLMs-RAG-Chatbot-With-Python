import os
import subprocess

def run_streamlit_app():
    """
    Chạy ứng dụng Streamlit
    """
    # Lấy đường dẫn thư mục hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Đường dẫn đến file streamlit_app.py
    app_path = os.path.join(current_dir, "streamlit_app.py")
    
    # Kiểm tra file tồn tại
    if not os.path.exists(app_path):
        print(f"Không tìm thấy file {app_path}!")
        return
    
    # Chạy ứng dụng streamlit
    print(f"Đang khởi động ứng dụng Streamlit từ {app_path}...")
    subprocess.call(["streamlit", "run", app_path])

if __name__ == "__main__":
    run_streamlit_app() 