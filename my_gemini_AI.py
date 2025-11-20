import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as nd
st.set_page_config(page_title="Gemini",layout="centered")
tab1,tab2,tab3 = st.tabs(["Gemini","Đăng nhập","Đăng ký"])
with tab1:
    st.header("Gemini like clone")
    genai.configure(api_key="AIzaSyBGvb4xckZM3f51fDm2JQZeel1RG1M4GUY")
    if "gemini_model" not in st.session_state:
        st.session_state["gemini_model"] = genai.GenerativeModel("gemini-1.5-flash-latest")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        role = message["role"]
        with st.chat_message(role):
            for part in message["parts"]:
                st.markdown(part["text"])
    if prompt := st.chat_input("Bạn có câu hỏi gì không?"):
        user_message = {"role": "user", "parts": [{"text": prompt}]}
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = st.session_state["gemini_model"].generate_content(
                    st.session_state.messages,
                    stream=False
                )
                full_response = ""
                for part in response.parts:
                    full_response += part.text
                st.markdown(full_response)
                assistant_message = {"role": "model", "parts": [{"text": full_response}]}
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