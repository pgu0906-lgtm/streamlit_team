import base64

def encode_image_to_data_url(image_file):
    bytes_data = image_file.getvalue()
    b64 = base64.b64encode(bytes_data).decode("utf-8")
    return f"data:image/png;base64,{b64}"
import streamlit as st
from openai import OpenAI
import base64

if "OPENAI_KEY" not in st.session_state:
    st.error("먼저 메인 화면에서 OpenAI API Key를 입력해주세요!")
    st.stop()

client = OpenAI(api_key=st.session_state["OPENAI_KEY"])


def encode_image_to_data_url(image_file):
    bytes_data = image_file.getvalue()
    b64 = base64.b64encode(bytes_data).decode("utf-8")
    return f"data:image/png;base64,{b64}"

st.title("🧺 빨래 챗봇")
st.caption("니트, 이불, 털옷처럼 어떻게 빨아야 할지 모를 때 도와드려요!")

if "laundry_chat" not in st.session_state:
    st.session_state.laundry_chat = []

# 대화 기록 출력
for role, msg in st.session_state.laundry_chat:
    st.chat_message(role).write(msg)

# 입력
st.subheader("1) 사진 입력 (라벨/옷 상태 촬영)")
camera_image = st.camera_input("📷 사진 찍기")
uploaded_image = st.file_uploader("📁 사진 업로드", type=["jpg","jpeg","png"])

st.subheader("2) 고민 설명")
user_text = st.text_area("세탁이 고민되는 옷/이불을 알려주세요!")

if st.button("분석하기"):
    if not user_text and not (camera_image or uploaded_image):
        st.warning("사진 또는 텍스트가 필요해요.")
        st.stop()

    st.session_state.laundry_chat.append(("user", user_text or "(사진만 업로드됨)"))

    user_content = []
    if user_text:
        user_content.append({"type":"input_text","text":user_text})

    image_file = camera_image or uploaded_image
    if image_file:
        user_content.append({
            "type":"input_image",
            "image_url":{"url":encode_image_to_data_url(image_file)}
        })

    system_prompt = """
    너는 '세탁 전문가 AI'야.
    사용자가 보낸 사진(옷 라벨/재질/얼룩)과 설명을 읽고
    1) 재질 추정 + 라벨 의미 풀이
    2) 추천 세탁 코스/물 온도/세제 종류
    3) 건조 방법
    4) 절대 하면 안되는 주의사항
    5) 실수 방지 팁
    을 알려줘.
    """

    res = client.responses.create(
        model="gpt-5.1-mini",
        input=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_content},
        ]
    )

    answer = res.output_text
    st.chat_message("assistant").write(answer)
    st.session_state.laundry_chat.append(("assistant", answer))
