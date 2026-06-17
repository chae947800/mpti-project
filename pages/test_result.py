import random
import re
import streamlit as st
from pages.result_logic import mpti_results

# 1. 페이지 기본 설정
st.set_page_config(page_title="MPTI 결과", page_icon="📊", layout="wide")

st.title("MPTI 성격 테스트 결과")
st.write("🎵 당신이 고른 음악 취향 속에 숨겨진 4가지 특징")

# 2. 성향 지표 안내 UI
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


def parse_stat_percentage(stat_text: str) -> float | None:
    match = re.search(r"(\d{1,3})%", stat_text)
    if match:
        value = float(match.group(1))
        return min(max(value, 0.0), 100.0)
    return None


def display_result(mpti_key: str) -> None:
    # 검사 페이지에서 넘어온 4글자 키로 시작하는 실제 데이터 방 이름("HVFN (홉픈)")을 찾습니다.
    actual_key = next((k for k in mpti_results.keys() if k.startswith(mpti_key)), None)
    
    if not actual_key:
        st.error("유효하지 않은 MPTI 결과입니다. 검사를 다시 진행해 주세요.")
        return

    # 세션에 이미 저장된 결과가 있고 키가 같다면 그대로 쓰고, 없으면 새로 무작위(A/B타입 중) 추출하여 고정합니다.
    result = st.session_state.get("selected_result")
    if not result or st.session_state.get("selected_key") != actual_key:
        result = random.choice(mpti_results[actual_key])
        st.session_state.selected_result = result
        st.session_state.selected_key = actual_key

    # 3. 결과 화면 출력 (깔끔한 UI 정렬)
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


# 4. 검사 페이지(test.py)에서 넘겨준 결과 키를 받아서 화면에 그려줍니다.
# 만약 바로 결과페이지로 접속했다면 기본적으로 "HVFN"을 보여줍니다.
user_mpti = st.session_state.get("selected_key", "HVFN")
display_result(user_mpti)