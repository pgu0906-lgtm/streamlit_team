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

st.title("🍽 부엌 챗봇")
st.caption("가스, 유통기한, 설거지·위생 같은 부엌 문제를 해결해드립니다!")

if "kitchen_chat" not in st.session_state:
    st.session_state.kitchen_chat = []

for role, msg in st.session_state.kitchen_chat:
    st.chat_message(role).write(msg)

st.subheader("1) 사진 입력")
camera_image = st.camera_input("📷 사진 찍기")
uploaded_image = st.file_uploader("📁 사진 업로드", type=["jpg","jpeg","png"])

st.subheader("2) 상황 설명")
user_text = st.text_area("부엌에서 어떤 상황인가요?")

if st.button("분석하기"):
    if not user_text and not (camera_image or uploaded_image):
        st.warning("사진 또는 설명을 입력해주세요!")
        st.stop()

    st.session_state.kitchen_chat.append(("user", user_text or "(사진만 업로드됨)"))

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
    너는 '부엌 안전/위생 전문가 AI'야.
    사진(가스 밸브, 음식, 싱크대)과 설명을 보고
    1) 사진 상황 설명
    2) 위험 요소(가스/불/상한 음식 등) 판단
    3) 즉시 해야 할 조치
    4) 해결 방법 단계별 안내
    5) 유통기한 관련 참고 조언
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
    st.session_state.kitchen_chat.append(("assistant", answer))
