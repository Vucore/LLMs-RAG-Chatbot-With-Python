# Ứng dụng Chatbot + RAG + LangChain

Ứng dụng này cung cấp giao diện người dùng cho hệ thống chatbot thông minh, sử dụng công nghệ Streamlit và tích hợp với mô hình ngôn ngữ lớn.

## Tính năng

- 💬 Trò chuyện trực tiếp với chatbot thông minh
- 🔍 Tìm kiếm thông tin 
- 📊 Quản lý file PDF đã upload
- 📚 Sử dụng RAG (Retrieval Augmented Generation) để cải thiện chất lượng câu trả lời
- 🔄 Sử dụng Chroma làm vector database để lưu trữ và truy xuất tri thức
- 🇻🇳 Tích hợp mô hình `bkai-foundation-models/vietnamese-bi-encoder` từ Hugging Face cho embedding tiếng Việt

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.8+ và pip

2. Cài đặt các gói phụ thuộc (Có uv cài đặt nhanh hơn pip):
```bash
uv pip install -r requirements.txt  
```

3. Cài đặt Ollama (cho mô hình Llama3) theo hướng dẫn tại [Ollama.ai](https://ollama.ai/download)

## Cách sử dụng

### Chạy ứng dụng Streamlit

Chạy server:

```bash
uvicorn app.main:app --reload
```

Khởi động Client Streamlit:

```bash
streamlit run Client/streamlit_app.py
```

Ứng dụng sẽ khởi động và mở tự động trong trình duyệt web.

### Sử dụng chatbot

1. Nhập câu hỏi của bạn vào ô văn bản
2. Lựa chọn sử dụng RAG nếu muốn tìm kiếm thông tin từ tài liệu
3. Xem câu trả lời từ chatbot được hiển thị theo thời gian thực

## Cấu trúc dự án

```
chatbot_module/
├── base/                  # Mô-đun cơ sở của chatbot
│   ├── Agent/             # Agent thông minh xử lý truy vấn
│   ├── RAG/               # Hệ thống truy xuất và tăng cường thông tin
│   ├── ML/                # Chứa mô hình embedding
│   └── ...                #
│               
├── api/                   # API routes cho ứng dụng backend
├── services/              # Dịch vụ xử lý logic
└── streamlit_app.py       # Ứng dụng Streamlit
```

## Công nghệ sử dụng

- **Mô hình ngôn ngữ**: Llama3 thông qua Ollama
- **Vector Database**: Chroma để lưu trữ và truy xuất hiệu quả các embedding
- **Embedding Model**: `bkai-foundation-models/vietnamese-bi-encoder` từ Hugging Face cho embedding tiếng Việt
- **Framework**: LangChain cho xử lý chuỗi prompt và RAG
- **Frontend**: Streamlit cho giao diện người dùng thân thiện
- **Backend**: FastAPI

## Phát triển

Phát triển bởi Minh Vu