import cv2
import numpy as np
import streamlit as st

def grade_answer(question_image, answer_image, similarity_threshold=0.8):
    # 이미지를 numpy 배열로 변환
    question_img = cv2.imdecode(np.frombuffer(question_image.read(), np.uint8), 1)
    answer_img = cv2.imdecode(np.frombuffer(answer_image.read(), np.uint8), 1)

    # 이미지 크기가 다른 경우 리사이즈
    if question_img.shape != answer_img.shape:
        answer_img = cv2.resize(answer_img, (question_img.shape[1], question_img.shape[0]))

    # 그레이스케일로 변환
    question_gray = cv2.cvtColor(question_img, cv2.COLOR_BGR2GRAY)
    answer_gray = cv2.cvtColor(answer_img, cv2.COLOR_BGR2GRAY)

    # 구조적 유사성 지수(SSIM) 계산
    (score, diff) = cv2.compareSSIM(question_gray, answer_gray, full=True)

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
