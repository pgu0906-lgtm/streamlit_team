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

st.title("📃 고지서 챗봇")
st.caption("월세/보증금/관리비/전세사기 같은 사회초년생 경제 문제를 도와드려요!")

if "bill_chat" not in st.session_state:
    st.session_state.bill_chat = []

for role, msg in st.session_state.bill_chat:
    st.chat_message(role).write(msg)

st.subheader("1) 고지서/계약서 사진")
camera_image = st.camera_input("📷 찍기")
uploaded_image = st.file_uploader("📁 업로드", type=["jpg","jpeg","png"])

st.subheader("2) 상황 설명")
user_text = st.text_area("궁금한 내용을 적어주세요!")

if st.button("분석하기"):
    if not user_text and not (camera_image or uploaded_image):
        st.warning("사진 또는 텍스트가 필요합니다.")
        st.stop()

    st.session_state.bill_chat.append(("user", user_text or "(사진만 업로드됨)"))

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
    너는 '사회초년생 생활 금융 가이드 AI'야.
    고지서/계약서 사진과 텍스트를 보고
    1) 사진 내용 정리 (금액/항목)
    2) 상황 분석
    3) 체크해야 할 리스트
    4) 사기/이상 신호 판단 (일반적 기준)
    5) 다음 단계 조언
    을 알려줘.
    법률 자문이 아니라는 안내도 마지막에 추가해줘.
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
    st.session_state.bill_chat.append(("assistant", answer))
