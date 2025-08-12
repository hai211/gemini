import streamlit as st
import google.generativeai as genai

st.title("Gemini-like clone")

# Thiết lập Gemini API key
genai.configure(api_key="AIzaSyBi43oTeMx0mCIpqrAH_8J7SqVkSnV1UHg")

# Khởi tạo mô hình
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = genai.GenerativeModel("gemini-1.5-flash-latest")

# Khởi tạo lịch sử chat
# Lịch sử chat được lưu trữ theo định dạng mà Gemini API yêu cầu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị tin nhắn từ lịch sử chat
for message in st.session_state.messages:
    # Lấy vai trò (role) của tin nhắn từ lịch sử chat
    role = message["role"]
    # Hiển thị tin nhắn
    with st.chat_message(role):
        # Duyệt qua các phần (parts) của tin nhắn và hiển thị nội dung
        for part in message["parts"]:
            st.markdown(part["text"])

# Xử lý input từ người dùng
if prompt := st.chat_input("Bạn có câu hỏi gì không?"):
    # Tạo tin nhắn người dùng theo định dạng của Gemini API
    user_message = {"role": "user", "parts": [{"text": prompt}]}

    # Thêm tin nhắn của người dùng vào lịch sử chat
    st.session_state.messages.append(user_message)

    # Hiển thị tin nhắn của người dùng
    with st.chat_message("user"):
        st.markdown(prompt)

    # Hiển thị phản hồi từ Gemini
    with st.chat_message("assistant"):
        try:
            # Gọi API với lịch sử chat đã được định dạng đúng
            response = st.session_state["gemini_model"].generate_content(
                st.session_state.messages,
                stream=False
            )

            # Lấy nội dung phản hồi từ đối tượng response của Gemini
            full_response = ""
            for part in response.parts:
                full_response += part.text

            st.markdown(full_response)

            # Tạo tin nhắn trợ lý theo định dạng của Gemini API
            assistant_message = {"role": "model", "parts": [{"text": full_response}]}

            # Thêm tin nhắn phản hồi của trợ lý vào lịch sử chat
            st.session_state.messages.append(assistant_message)

        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")