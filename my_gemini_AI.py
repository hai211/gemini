import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as nd

st.set_page_config(page_title="Gemini",layout="centered")

tab1,tab2,tab3 = st.tabs(["Gemini","Đăng nhập","Đăng ký"])


with tab1:
    st.header("Gemini like clone")
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


with tab2:
    st.header("Đăng nhập")
    container = st.container(border=True)
    container.header("Đăng nhập hệ thống học viên")
    container.write("Nhập tài khoản được cấp để đăng nhập vào hệ thống")
    container.write()
    container.write("**Tên đăng nhập**")
    user = container.text_input(label=" ",placeholder="Vui long nhap ten tai khoan")
    container.write("**Mật khẩu**")
    password1 = container.text_input(label=" ",type="password",placeholder="Vui long nhap mat khau")
    widget = container.button("Dang nhap")

    account = "admin"
    password = "nam20062011"

    if widget:
        if user == account and password == password1:
            st.success("success!!")
        else:
            st.error("error!!")

    else:
        user=""
        password1=""


with tab3:
    st.title("Tạo Tài Khoản Mới Của Bạn")
    container2 = st.container(border=True)
    container2.subheader("Vui lòng điền thông tin vào đây:")
    username = container2.text_input("Tên người dùng", placeholder="Nhập tên của bạn")
    password = container2.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
    confirm_password = container2.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")
    widget2 = container2.button("Đăng ký")
    container2.markdown("---")
    container2.write("Cảm ơn bạn đã ghé thăm ứng dụng đơn giản này!")
    
    if not username or not password or not confirm_password:
        st.warning("Vui lòng điền đầy đủ tất cả các trường.")
    elif password != confirm_password:
        st.error("Mật khẩu và xác nhận mật khẩu không khớp.")
    else:
        st.success("Đăng ký thành công! Chào mừng bạn.")
        st.info("Lưu ý: Thông tin này chỉ để hiển thị, không được lưu trữ.")

