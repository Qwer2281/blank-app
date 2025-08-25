import streamlit as st
import random
from PIL import Image
import os

st.title("카드 맞추기 게임")
st.write("5장의 카드 중 조커를 맞춰보세요!")

# --- 게임 상태 초기화 ---
if "answer" not in st.session_state:
    st.session_state.answer = random.randint(0, 4)  # 정답 카드 위치
    st.session_state.removed = []  # 제거된 카드 인덱스
    st.session_state.revealed = [False] * 5  # 카드 뒤집힘 여부
    st.session_state.wrong_images = {}  # 오답 카드별 이미지 저장
    st.session_state.result = ""

# --- 카드 이미지 불러오기 ---
card_back = Image.open("static/images/CardB.png")  # 여기
card_back = card_back.resize((120, 180))
card_joker = Image.open("static/images/CardD.png")  # 여기
card_joker = card_joker.resize((120, 180))

# 오답 이미지 후보 불러오기
# 오답 이미지 후보 불러오기
wrong_dir = "static/images"
wrong_candidates = sorted(
    [f for f in os.listdir(wrong_dir) if f.startswith("wrong") and f.endswith(".png")]
)
wrong_images = [Image.open(os.path.join(wrong_dir, f)).resize((120, 180)) for f in wrong_candidates]

# --- 카드 버튼 출력 ---
cols = st.columns(5)
for i in range(5):
    if i in st.session_state.removed:
        cols[i].image(Image.new("RGBA", (120, 180), (200, 200, 200, 255)))
    else:
        if st.session_state.revealed[i]:
            if i == st.session_state.answer:
                cols[i].image(card_joker)
            else:
                cols[i].image(st.session_state.wrong_images[i])
        else:
            if cols[i].button("", key=f"card_{i}"):
                if i == st.session_state.answer:
                    st.session_state.result = "🎉 정답! 조커를 찾았습니다!"
                    st.session_state.revealed[i] = True
                else:
                    st.session_state.result = "❌ 꽝! 오답 카드를 뒤집었습니다."
                    st.session_state.revealed[i] = True
                    st.session_state.wrong_images[i] = random.choice(wrong_images)
            cols[i].image(card_back)

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
    st.session_state.revealed = [False] * 5
    st.session_state.wrong_images = {}
    st.session_state.result = ""
