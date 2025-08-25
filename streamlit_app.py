import streamlit as st
import random

# --- 게임 상태 초기화 ---
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "answer": random.randint(0, 4),  # 정답 카드 위치
        "removed": [],  # 제거된 카드 인덱스
        "revealed": [False] * 5,  # 카드 뒤집힘 여부
        "result": "",
        "game_over": False,  # 게임 종료 상태 추가
    }

st.title("🃏 카드 맞추기 게임")
st.write("5장의 카드 중 조커(정답)를 맞춰보세요!")

# --- 카드 이미지 (이모지로 대체) ---
card_back_symbol = "❓"
card_joker_symbol = "🃏"
wrong_card_symbols = ["💀", "👻", "🤡", "�"]

# --- 카드 버튼 및 이미지 출력 ---
cols = st.columns(5)
for i in range(5):
    # 제거된 카드인 경우
    if i in st.session_state.game_state["removed"]:
        with cols[i]:
            st.markdown(
                f"<div style='height:180px; width:120px; border-radius:10px; background-color:#e2e8f0; border:2px solid #cbd5e0;'></div>",
                unsafe_allow_html=True
            )
    # 뒤집힌 카드인 경우
    elif st.session_state.game_state["revealed"][i]:
        with cols[i]:
            if i == st.session_state.game_state["answer"]:
                st.markdown(f"<p style='font-size: 5rem; text-align: center; margin: 0; padding-top: 20px;'>{card_joker_symbol}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='font-size: 5rem; text-align: center; margin: 0; padding-top: 20px;'>{random.choice(wrong_card_symbols)}</p>", unsafe_allow_html=True)
    # 아직 선택되지 않은 카드인 경우
    else:
        with cols[i]:
            if st.button(f"**{card_back_symbol}**", key=f"card_{i}", use_container_width=True):
                # 게임이 끝나지 않았을 때만 동작
                if not st.session_state.game_state["game_over"]:
                    st.session_state.game_state["revealed"][i] = True
                    if i == st.session_state.game_state["answer"]:
                        st.session_state.game_state["result"] = "🎉 정답! 조커를 찾았습니다!"
                        st.session_state.game_state["game_over"] = True
                    else:
                        st.session_state.game_state["result"] = "❌ 꽝! 오답 카드를 뒤집었습니다."
            # 버튼 아래에 뒷면 심볼을 표시하여 버튼이 보이지 않게 함
            st.markdown(f"<p style='position:relative; top: -180px; font-size: 6rem; text-align: center; margin: 0; padding-top: 20px; color: transparent;'>{card_back_symbol}</p>", unsafe_allow_html=True)

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
        "result": "",
        "game_over": False,
    }
    st.rerun() # 변경사항 즉시 적용
�