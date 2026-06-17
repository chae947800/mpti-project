import streamlit as st
import json
import random
import re
from pathlib import Path
from pages.result_logic import mpti_results

# 1. 경로 및 데이터 저장 함수 (상단 정의)
DATA_FILE = Path(__file__).resolve().parents[1] / "users.json"

def save_result_to_user(mpti_key):
    if "username" in st.session_state and DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
        uid = st.session_state.username
        if uid in users:
            users[uid]["mpti"] = mpti_key
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)

# 2. 결과 처리 로직 (상단 정의)
def parse_stat_percentage(stat_text: str) -> float | None:
    match = re.search(r"(\d{1,3})%", stat_text)
    if match:
        value = float(match.group(1))
        return min(max(value, 0.0), 100.0)
    return None

def display_result(mpti_key: str) -> None:
    actual_key = next((k for k in mpti_results.keys() if k.startswith(mpti_key)), None)
    if not actual_key:
        st.error("유효하지 않은 MPTI 결과입니다.")
        return
    
    # 결과 고정 (세션에 저장)
    if "selected_result" not in st.session_state or st.session_state.get("selected_key") != actual_key:
        st.session_state.selected_result = random.choice(mpti_results[actual_key])
        st.session_state.selected_key = actual_key
        st.session_state.current_actual_key = actual_key

    result = st.session_state.selected_result
    st.subheader(f"결과 유형: {actual_key}")
    st.header(result["title"])
    st.write("---")
    st.subheader("📊 성격 능력치")
    for stat in result["stats"]:
        percentage = parse_stat_percentage(stat)
        if percentage is not None:
            cols = st.columns([4, 2])
            cols[0].info(stat)
            cols[1].progress(percentage / 100)
        else:
            st.info(stat)
    st.write("---")
    st.subheader("📝 성격 분석")
    st.write(result["description"])

# --- 여기서부터 기존 UI 유지 ---

st.set_page_config(page_title="MPTI 결과", page_icon="📊", layout="wide")
st.title("MPTI 성격 테스트 결과")
st.write("🎵 당신이 고른 음악 취향 속에 숨겨진 4가지 특징")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.caption("**H / L**")
    st.caption("🔊 Heavy (무거운)")
    st.caption("🌱 Light (가벼운)")
with col2:
    st.caption("**V / I**")
    st.caption("🎤 Vocal (목소리)")
    st.caption("🎸 Inst (악기)")
with col3:
    st.caption("**F / S**")
    st.caption("⚡ Fast (빠른)")
    st.caption("☕ Slow (느린)")
with col4:
    st.caption("**N / O**")
    st.caption("✨ New (최신)")
    st.caption("📻 Old (레트로)")
st.write("---")

user_mpti = st.session_state.get("selected_key", "HVFN")
display_result(user_mpti)

# 3. 홈화면 버튼 (기능 추가)
if st.button("🏠 홈화면으로 이동"):
    key_to_save = st.session_state.get("current_actual_key", "HVFN")
    save_result_to_user(key_to_save)
    st.switch_page("pages/dashboard.py")