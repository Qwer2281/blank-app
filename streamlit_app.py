import streamlit as st
import random
from PIL import Image
import os

# --- 게임 상태 초기화 ---
if "game_state" not in st.session_state:
    # 정답 카드 위치
    st.session_state.game_state = {
        "answer": random.randint(0, 4),
        "removed": [],  # 제거된 카드 인덱스
        "revealed": [False] * 5,  # 카드 뒤집힘 여부
        "wrong_images": {},  # 오답 카드별 이미지 저장
        "result": "",
        "game_over": False,
    }

st.title("🃏 카드 맞추기 게임")
st.write("5장의 카드 중 조커(정답)를 맞춰보세요!")

# --- 카드 이미지 불러오기 (로컬 파일 사용) ---
try:
    card_back = Image.open("static/images/CardB.png")
    card_joker = Image.open("static/images/CardJ.png")
    
    wrong_dir = "static/images"
    wrong_candidates = [f for f in os.listdir(wrong_dir) if f.startswith("wrong") and f.endswith(".png")]
    wrong_images = [Image.open(os.path.join(wrong_dir, f)) for f in wrong_candidates]

    # 이미지 크기 통일
    card_back = card_back.resize((150, 220))
    card_joker = card_joker.resize((150, 220))
    wrong_images = [img.resize((150, 220)) for img in wrong_images]

except FileNotFoundError:
    st.error("이미지 파일을 찾을 수 없습니다. 'static/images' 폴더에 이미지 파일을 넣어주세요.")
    st.stop()

# --- 카드 버튼 및 이미지 출력 ---
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        # 제거된 카드인 경우
        if i in st.session_state.game_state["removed"]:
            st.markdown("<div style='height:220px; width:150px; background-color:#e2e8f0; border-radius:10px;'></div>", unsafe_allow_html=True)
        # 이미 뒤집힌 카드인 경우
        elif st.session_state.game_state["revealed"][i]:
            if i == st.session_state.game_state["answer"]:
                st.image(card_joker, use_column_width=True)
            else:
                st.image(st.session_state.game_state["wrong_images"][i], use_column_width=True)
        # 아직 선택되지 않은 카드인 경우
        else:
            if st.button("", key=f"card_{i}", use_container_width=True):
                # 게임이 끝나지 않았을 때만 동작
                if not st.session_state.game_state["game_over"]:
                    st.session_state.game_state["revealed"][i] = True
                    if i == st.session_state.game_state["answer"]:
                        st.session_state.game_state["result"] = "🎉 정답! 조커를 찾았습니다!"
                        st.session_state.game_state["game_over"] = True
                        # 정답 맞추면 모든 카드 뒤집기
                        for j in range(5):
                            if j != i:
                                st.session_state.game_state["revealed"][j] = True
                                if j not in st.session_state.game_state["wrong_images"]:
                                     st.session_state.game_state["wrong_images"][j] = random.choice(wrong_images)
                    else:
                        st.session_state.game_state["result"] = "❌ 꽝! 오답 카드를 뒤집었습니다."
                        st.session_state.game_state["wrong_images"][i] = random.choice(wrong_images)
                    st.rerun()

            st.image(card_back, use_column_width=True)
            
# --- 오답 카드 제거 기능 ---
if st.button("오답 카드 하나 제거하기", disabled=st.session_state.game_state["game_over"]):
    choices = [i for i in range(5) if i != st.session_state.game_state["answer"] and i not in st.session_state.game_state["removed"] and not st.session_state.game_state["revealed"][i]]
    if choices:
        remove = random.choice(choices)
        st.session_state.game_state["removed"].append(remove)
        st.session_state.game_state["result"] = f"❌ {remove + 1}번 카드가 제거되었습니다."
    else:
        st.session_state.game_state["result"] = "더 이상 제거할 카드가 없습니다."

# --- 결과 출력 ---
st.write(st.session_state.game_state["result"])

# --- 새 게임 버튼 ---
if st.button("새 게임 시작"):
    st.session_state.game_state = {
        "answer": random.randint(0, 4),
        "removed": [],
        "revealed": [False] * 5,
        "wrong_images": {},
        "result": "",
        "game_over": False,
    }
    st.rerun()
