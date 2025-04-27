import streamlit as st
import requests
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

PROCESS_DOCUMENTS_API_URL = "http://localhost:8000/api/process_documents"
UPLOAD_FILE_API_URL = "http://localhost:8000/api/upload/file"
GET_AGENT_EXECUTOR_API_URL = "http://localhost:8000/api/get_agent_executor"
RUN_AGENT_API_URL = "http://localhost:8000/api/run_agent"

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

def setup_chat_interface():
    st.title("💬 AI Assistant")
    st.caption("🚀 Trợ lý AI được hỗ trợ bởi LangChain và Llama3")

    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Tôi có thể giúp gì cho bạn?"}
        ]
        msgs.add_ai_message("Tôi có thể giúp gì cho bạn?")

        for msg in st.session_state.messages:
            role = "assistant" if msg["role"] == "assistant" else "human"
            st.chat_message(role).write(msg["content"])
    return msgs


def handle_file_upload():
    """Xử lý upload file lên backend và hiển thị danh sách file"""
    # Khởi tạo danh sách file trong session nếu chưa có
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = False
    
    # if "uploader_key" not in st.session_state:
    #     st.session_state["uploader_key"] = str(uuid.uuid4())
        
    uploaded_file = st.file_uploader(
        "Tải tài liệu PDF lên để truy vấn", 
        type=["pdf"],
        # key=st.session_state["uploader_key"]
    )
    
    if uploaded_file is not None and not st.session_state.file_uploaded:
        file_names = [f["original_name"] for f in st.session_state.uploaded_files]
        if uploaded_file.name not in file_names:
            # Gửi file lên backend qua API
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(UPLOAD_FILE_API_URL, files=files)

            if response.status_code == 200:
                result = response.json()
                st.session_state.uploaded_files.append({
                    "status": result.get("status", ""),
                    "original_name": result.get("original_name", ""),
                    "selected": True
                })
                st.success(f"Đã tải file lên backend thành công: {result.get('original_name', '')}")
            else:
                st.error(f"Lỗi upload: {response.text}")
            
            st.session_state.file_uploaded = True
            st.rerun()
    
    if uploaded_file is None:
        st.session_state.file_uploaded = False

    # Hiển thị danh sách file đã upload
    if st.session_state.uploaded_files:
        st.markdown("<div class='file-list'>", unsafe_allow_html=True)
        st.subheader("Tài liệu đã tải lên:")

        for index, file_info in enumerate(st.session_state.uploaded_files):
            is_selected = st.checkbox(
                f"{file_info['original_name']}", 
                value=file_info['selected'],
            )
            st.session_state.uploaded_files[index]['selected'] = is_selected

        st.markdown("</div>", unsafe_allow_html=True)
    
    # Xử lý nút truy xuất
    selected_files = [f["original_name"] for f in st.session_state.uploaded_files if f["selected"]]
    if selected_files and st.button("Truy xuất dữ liệu từ tài liệu đã chọn"):
        try:
            response = requests.post(
                PROCESS_DOCUMENTS_API_URL, 
                json={"original_names": selected_files}
            )
            if response.status_code == 200:
                st.success("Đã xử lý tài liệu thành công!")
            else:
                st.error(f"Lỗi xử lý tài liệu: {response.text}")
        except Exception as e:
            st.error(f"Lỗi khi kết nối server: {str(e)}")

def handle_user_input(msgs):
    if prompt := st.chat_input("Hãy hỏi tôi bất cứ điều gì!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("human").write(prompt)
        msgs.add_user_message(prompt)

        with st.chat_message("assistant"):
            chat_history = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages[:-1]
            ]
            response = requests.post(RUN_AGENT_API_URL, json={"message": prompt, "chat_history": chat_history})
            response_agent = response.json()
            output = response_agent["output"]
            st.session_state.messages.append({"role": "assistant", "content": output})
            msgs.add_ai_message(output)
            st.write(output)


# Sidebar
with st.sidebar:
    st.header("Cài đặt")
    
    # Thêm phần tải file và hiển thị danh sách file trong sidebar
    st.markdown("---")
    st.subheader("Quản lý tài liệu")
    handle_file_upload()
    
    st.markdown("---")
        
    st.markdown("### Hướng dẫn")
    st.info("""
    Chatbot này xây dựng bởi LangChain và Llama3:
    - Tải các tài liệu PDF (đã được làm sạch) lên để truy vấn
    """)


def main():
    msgs = setup_chat_interface()
    handle_user_input(msgs)


if __name__ == "__main__":
    main()

st.markdown("---")
st.markdown("Phát triển bởi Minh Vu")
