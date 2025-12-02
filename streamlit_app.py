import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="1인 가구 AI 해결사", page_icon="🏠", layout="wide")

# ============================
# 🔐 1) 사용자에게 OpenAI API Key 입력받기
# ============================

st.sidebar.header("🔐 OpenAI API Key 입력")
openai_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-xxxx...",
)

if openai_key:
    st.session_state["OPENAI_KEY"] = openai_key

# 안내 문구
if "OPENAI_KEY" not in st.session_state:
    st.info("좌측 사이드바에 OpenAI API Key를 입력해주세요.")
else:
    st.success("OpenAI Key가 설정되었습니다!")

# ----------------------------

st.title("🏠 1인 가구 AI 해결사")
st.write("원룸 설계도를 보고, 고민되는 공간을 클릭하세요!")

img = Image.open("assets/oneroom.png")

canvas = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=0,
    background_image=img,
    update_streamlit=True,
    height=img.height,
    width=img.width,
    drawing_mode="transform",
    key="room_canvas",
)

if canvas.json_data is not None and len(canvas.json_data["objects"]) > 0:
    obj = canvas.json_data["objects"][-1]
    x, y = obj["left"], obj["top"]

    if 90 < x < 220 and 250 < y < 380:
        st.switch_page("pages/1_청소_챗봇.py")

    elif 220 < x < 350 and 250 < y < 380:
        st.switch_page("pages/2_빨래_챗봇.py")

    elif 350 < x < 480 and 150 < y < 280:
        st.switch_page("pages/3_고지서_챗봇.py")

    elif 350 < x < 520 and 300 < y < 430:
        st.switch_page("pages/4_부엌_챗봇.py")
