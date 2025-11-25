import streamlit as st
import base64
from openai import OpenAI

# 👉 Streamlit Cloud에서는 Settings → Secrets에 OPENAI_API_KEY 넣어두고 이렇게 불러오는 걸 추천
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📸 사물 인식 설명 봇")

st.write("카메라로 사진을 찍으면, 사진 속에 있는 사물들을 설명해줄게요!")

img_file = st.camera_input("사진을 찍어주세요")

if img_file is not None:
    st.image(img_file, caption="촬영한 사진", use_column_width=True)

    if st.button("사진 분석하기"):
        with st.spinner("사진 분석 중..."):
            # 1) 이미지 → base64 인코딩
            img_bytes = img_file.getvalue()
            b64_img = base64.b64encode(img_bytes).decode("utf-8")
            img_data_url = f"data:image/jpeg;base64,{b64_img}"

            # 2) OpenAI 비전 모델 호출 (Responses API 스타일)
            response = client.responses.create(
                model="gpt-4.1-mini",  # 또는 gpt-4o 등 비전 지원 모델
                input=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "이 사진에 보이는 주요 사물들을 한국어로 설명해줘. "
                                "각 사물이 무엇인지, 어떤 특징이 있는지도 간단히 말해줘."
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": img_data_url,
                            "detail": "auto",
                        },
                    ],
                }],
            )

            description = response.output_text
            st.subheader("설명 결과")
            st.write(description)
