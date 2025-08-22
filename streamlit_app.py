import streamlit as st
import random
from PIL import Image

st.title("🃏 카드 맞추기 게임")
st.write("5장의 카드 중 조커(정답)를 맞춰보세요!")

# --- 게임 상태 초기화 ---
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(0, 4)  # 정답 카드 위치
    st.session_state.removed = []  # 제거된 카드 인덱스
    st.session_state.result = ""

# --- 카드 이미지 불러오기 ---
card_image = Image.open("images/CardB.png")  # 여기
# 실제 카드 크기처럼 비율 조절 (너비: 120px, 높이: 180px)
card_image = card_image.resize((120, 180))

# --- 카드 버튼 출력 ---
cols = st.columns(5)
for i in range(5):
    if i in st.session_state.removed:
        cols[i].image(Image.new("RGBA", (120, 180), (200, 200, 200, 255)))  # 제거된 카드 회색으로 표시
    else:
        if cols[i].button("", key=f"card_{i}"):  # 카드 선택
            if i == st.session_state.answer:
                st.session_state.result = "🎉 정답! 조커를 찾았습니다!"
            else:
                st.session_state.result = "❌ 꽝! 다시 시도해보세요."
        # 버튼 대신 카드 이미지 표시
        cols[i].image(card_image)

# --- 오답 카드 제거 기능 ---
if st.button("오답 카드 하나 제거하기"):
    choices = [i for i in range(5) if i != st.session_state.answer and i not in st.session_state.removed]
    if choices:
        remove = random.choice(choices)
        st.session_state.removed.append(remove)
    else:
        st.write("더 이상 제거할 카드가 없습니다.")

# --- 결과 출력 ---
st.write(st.session_state.result)

# --- 새 게임 버튼 ---
if st.button("새 게임 시작"):
    st.session_state.answer = random.randint(0, 4)
    st.session_state.removed = []
    st.session_state.result = ""
