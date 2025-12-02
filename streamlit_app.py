import streamlit as st
from PIL import Image

st.set_page_config(page_title="1인 가구 AI 해결사", layout="wide")

st.title("🏠 1인 가구 AI 해결사")
st.write("원룸 설계도를 보고, 원하는 공간을 클릭하세요!")

# 원룸 이미지 로드
img = Image.open("assets/oneroom.png")

# 이미지 표시 + 클릭 이벤트 활성화
clicked = st.image(img, use_container_width=True)

# Streamlit click_event API
event = st.get_image_click("main_room")  # 고유 ID

if event:
    x, y = event["x"], event["y"]

    st.write(f"클릭 좌표: {x}, {y}")  # 디버깅용

    # --- 청소 영역 ---
    if 80 < x < 220 and 250 < y < 380:
        st.switch_page("pages/1_청소_챗봇.py")

    # --- 빨래 ---
    elif 220 < x < 350 and 250 < y < 380:
        st.switch_page("pages/2_빨래_챗봇.py")

    # --- 고지서 ---
    elif 350 < x < 480 and 150 < y < 280:
        st.switch_page("pages/3_고지서_챗봇.py")

    # --- 부엌 ---
    elif 350 < x < 520 and 300 < y < 430:
        st.switch_page("pages/4_부엌_챗봇.py")
