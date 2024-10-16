import streamlit as st
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import io

def grade_answer(question_image, answer_image, similarity_threshold=0.8):
    # 이미지를 numpy 배열로 변환
    question_img = Image.open(question_image).convert('L')
    answer_img = Image.open(answer_image).convert('L')

    # 이미지 크기가 다른 경우 리사이즈
    if question_img.size != answer_img.size:
        answer_img = answer_img.resize(question_img.size)

    # numpy 배열로 변환
    question_array = np.array(question_img)
    answer_array = np.array(answer_img)

    try:
        # 구조적 유사성 지수(SSIM) 계산
        score = ssim(question_array, answer_array)
    except Exception as e:
        return f"이미지 비교 중 오류 발생: {str(e)}", 0

    # 유사도에 따라 결과 반환
    if score >= similarity_threshold:
        return "정답", score
    else:
        return "오답", score

st.title('이미지 채점 애플리케이션')

question_image = st.file_uploader("문제 이미지를 업로드하세요", type=['jpg', 'jpeg', 'png'])
answer_image = st.file_uploader("답안 이미지를 업로드하세요", type=['jpg', 'jpeg', 'png'])

if question_image and answer_image:
    if st.button('채점하기'):
        result, score = grade_answer(question_image, answer_image)
        st.write(f"채점 결과: {result}")
        st.write(f"유사도 점수: {score:.2f}")

        # 이미지 표시
        st.image(question_image, caption='문제 이미지', use_column_width=True)
        st.image(answer_image, caption='답안 이미지', use_column_width=True)

st.write("애플리케이션 버전: 1.0.2")
st.write(f"NumPy 버전: {np.__version__}")
st.write(f"Pillow 버전: {Image.__version__}")
st.write(f"scikit-image 버전: {skimage.__version__}")
st.write(f"Streamlit 버전: {st.__version__}")
