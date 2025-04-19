import streamlit as st
import requests
import os
import uuid
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

FASTAPI_URL = "http://localhost:8000/api/chat"
UPLOAD_DIR = "uploads"

# Tạo thư mục uploads nếu chưa tồn tại
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

st.set_page_config(
    page_title="Chatbot Thông minh",
    page_icon="🌊",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main { background-color: #f5f7f9; }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        color: white;
        background-color: #4e8cff;
        padding: 0.5rem 1rem;
    }
    .file-list {
        margin-top: 10px;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


def get_response_from_api(message, use_rag=True, selected_files=None):
    payload = {
        "message": message,
        "rag": use_rag
    }
    
    # Thêm danh sách file được chọn vào payload nếu có
    if selected_files:
        payload["files"] = selected_files
        
    try:
        response = requests.post(FASTAPI_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("result", "Không có phản hồi từ chatbot.")
        else:
            return f"Lỗi {response.status_code}: {response.text}"
    except Exception as e:
        return f"Lỗi kết nối: {str(e)}"


def save_uploaded_file(uploaded_file):
    """Lưu file tải lên và trả về đường dẫn"""
    # Tạo tên file duy nhất để tránh trùng lặp
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    # Lưu file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path, uploaded_file.name


def setup_chat_interface():
    st.title("💬 AI Assistant")
    st.caption("🚀 Trợ lý AI được hỗ trợ bởi LangChain và Llama3")

    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    if len(msgs.messages) == 0:
        msgs.add_ai_message("Tôi có thể giúp gì cho bạn?")
    return msgs


def handle_file_upload():
    """Xử lý tải file lên và hiển thị danh sách file với checkbox"""
    # Khởi tạo danh sách file trong session state nếu chưa có
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    # Khởi tạo session state để theo dõi trạng thái tải lên
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = False
    
    # Widget tải file với key động để làm mới sau mỗi lần upload
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = str(uuid.uuid4())
        
    uploaded_file = st.file_uploader(
        "Tải tài liệu PDF lên để truy vấn", 
        type=["pdf"],
        key=st.session_state["uploader_key"]
    )
    
    # Xử lý file mới tải lên
    if uploaded_file is not None and not st.session_state.file_uploaded:
        # Kiểm tra xem file đã tồn tại chưa
        file_names = [f["original_name"] for f in st.session_state.uploaded_files]
        if uploaded_file.name not in file_names:
            # Lưu file và thêm vào danh sách
            file_path, original_name = save_uploaded_file(uploaded_file)
            st.session_state.uploaded_files.append({
                "path": file_path,
                "original_name": original_name,
                "selected": True  # Mặc định chọn file mới
            })
            st.success(f"Đã tải lên: {original_name}")
            
            # Đánh dấu đã tải file để tránh xử lý nhiều lần
            st.session_state.file_uploaded = True
            # Thiết lập key để buộc file uploader reset
            st.session_state["uploader_key"] = str(uuid.uuid4())
            # Chạy lại page để làm mới giao diện
            st.rerun()
    
    # Reset trạng thái file_uploaded khi không có file
    if uploaded_file is None:
        st.session_state.file_uploaded = False
    
    # Hiển thị danh sách file với checkbox
    if st.session_state.uploaded_files:
        st.markdown("<div class='file-list'>", unsafe_allow_html=True)
        st.subheader("Tài liệu đã tải lên:")
        
        for i, file_info in enumerate(st.session_state.uploaded_files):
            # Checkbox cho mỗi file
            is_selected = st.checkbox(
                f"{file_info['original_name']}", 
                value=file_info['selected'],
                key=f"file_{i}"
            )
            # Cập nhật trạng thái chọn
            st.session_state.uploaded_files[i]['selected'] = is_selected
        
        # Nút để xóa tất cả file
        if st.button("Xóa tất cả tài liệu"):
            # Xóa file khỏi hệ thống
            for file_info in st.session_state.uploaded_files:
                if os.path.exists(file_info["path"]):
                    try:
                        os.remove(file_info["path"])
                    except:
                        pass
            # Xóa danh sách
            st.session_state.uploaded_files = []
            st.success("Đã xóa tất cả tài liệu")
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Nút để kích hoạt truy xuất dữ liệu từ các file được chọn
    selected_files = [f["path"] for f in st.session_state.uploaded_files if f["selected"]]
    if selected_files and st.button("Truy xuất dữ liệu từ các tài liệu được chọn"):
        st.success(f"Đang truy xuất dữ liệu từ {len(selected_files)} tài liệu...")
        # Gọi API để truy xuất và xử lý dữ liệu từ các file được chọn
        try:
            response = requests.post(
                f"{FASTAPI_URL.replace('/chat', '/process_documents')}", 
                json={"file_paths": selected_files}
            )
            if response.status_code == 200:
                st.success("Đã xử lý tài liệu thành công!")
            else:
                st.error(f"Lỗi khi xử lý tài liệu: {response.text}")
        except Exception as e:
            st.error(f"Lỗi khi kết nối với server: {str(e)}")


def handle_user_input(msgs, use_rag):
    # Lấy danh sách file được chọn
    selected_files = [f["path"] for f in st.session_state.get("uploaded_files", []) if f["selected"]]
    
    if prompt := st.chat_input("Hãy hỏi tôi bất cứ điều gì!"):
        st.chat_message("human").write(prompt)
        msgs.add_user_message(prompt)

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            response = get_response_from_api(prompt, use_rag, selected_files)
            msgs.add_ai_message(response)
            st.write(response)


# Sidebar
with st.sidebar:
    st.header("Cài đặt")
    use_rag = st.checkbox("Sử dụng RAG (Retrieval Augmented Generation)", value=True)
    
    # Thêm phần tải file và hiển thị danh sách file trong sidebar
    st.markdown("---")
    st.subheader("Quản lý tài liệu")
    handle_file_upload()
    
    st.markdown("---")
    if st.button("Xóa lịch sử chat"):
        # Giữ lại danh sách file khi xóa lịch sử chat
        uploaded_files = st.session_state.get("uploaded_files", [])
        st.session_state.clear()
        st.session_state.uploaded_files = uploaded_files
        st.rerun()
        
    st.markdown("### Hướng dẫn")
    st.info("""
    Chatbot này cung cấp và trả lời theo thông tin:
    - Chọn RAG để ChatBot truy vấn theo thông tin file PDF
    - Bỏ chọn RAG để ChatBot trả lời dựa trên các kiến thức đã học
    """)


def main():
    msgs = setup_chat_interface()
    handle_user_input(msgs, use_rag)


if __name__ == "__main__":
    main()

st.markdown("---")
st.markdown("Phát triển bởi Minh Vu")
