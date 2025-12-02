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

st.title("🧹 청소 챗봇")
st.caption("에어컨, 화장실, 보일러처럼 처음 하면 어려운 집안일을 도와드릴게요!")

if "clean_chat" not in st.session_state:
    st.session_state.clean_chat = []

# 이전 대화 출력
for role, msg in st.session_state.clean_chat:
    st.chat_message(role).write(msg)

# 입력
st.subheader("1) 사진 입력 (선택)")
camera_image = st.camera_input("📷 지금 사진 찍기")
uploaded_image = st.file_uploader("📁 사진 업로드", type=["jpg","jpeg","png"])

st.subheader("2) 상황 설명")
user_text = st.text_area("어떤 청소가 막막한가요?")

if st.button("분석하기"):
    if not user_text and not (camera_image or uploaded_image):
        st.warning("사진 또는 설명을 입력해주세요!")
        st.stop()

    # 사용자 메시지 기록
    st.session_state.clean_chat.append(("user", user_text or "(사진만 업로드됨)"))

    # user_content 구성
    user_content = []
    if user_text:
        user_content.append({"type":"input_text","text":user_text})

    image_file = camera_image or uploaded_image
    if image_file:
        user_content.append({
            "type":"input_image",
            "image_url": { "url": encode_image_to_data_url(image_file) }
        })

    system_prompt = """
    너는 '청소 전문가 AI'야.
    사용자의 텍스트와 사진(에어컨 상태, 화장실, 보일러 등)을 보고
    1) 현재 상황 설명
    2) 준비물
    3) 단계별 청소 방법
    4) 안전 주의사항
    5) 전문가가 필요한 경우
    를 차분하게 설명해줘.
    """

    res = client.responses.create(
        model="gpt-5.1-mini",
        input=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_content}
        ],
    )

    answer = res.output_text
    st.chat_message("assistant").write(answer)
    st.session_state.clean_chat.append(("assistant", answer))
