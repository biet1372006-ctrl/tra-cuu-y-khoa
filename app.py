import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="Tra cứu Y Khoa", layout="wide")

st.title("🔍 Trợ lý Tra cứu Tài liệu Y Dược")
st.write("Dành cho sinh viên Cao đẳng Y tế Đồng Nai 🏥")

uploaded_file = st.sidebar.file_uploader("Tải file PDF hoặc Ảnh", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner('Đang đọc tài liệu...'):
        text_data = []
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for i, page in enumerate(pdf.pages):
                    text_data.append({"origin": f"Trang {i+1}", "text": page.extract_text() or ""})
        else:
            img = Image.open(uploaded_file)
            content = pytesseract.image_to_string(img, lang='vie')
            text_data.append({"origin": "Ảnh chụp", "text": content})

    keyword = st.text_input("Nhập từ khóa cần tìm (vđ: Paracetamol, kháng sinh...):")
    if keyword:
        found = False
        for item in text_data:
            if keyword.lower() in item['text'].lower():
                found = True
                with st.expander(f"📍 Tìm thấy tại: {item['origin']}", expanded=True):
                    highlighted = re.sub(f"({re.escape(keyword)})", r"**\1**", item['text'], flags=re.IGNORECASE)
                    st.markdown(highlighted)
        if not found:
            st.error("Không tìm thấy từ khóa này.")
