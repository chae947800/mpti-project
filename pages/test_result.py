import random
import re

import streamlit as st
from result_logic import mpti_results

st.set_page_config(page_title="MPTI 결과", page_icon="📊", layout="wide")

st.title("MPTI 성격 테스트 결과")
st.write("개발자 테스트용: 사이드바에서 MPTI 키를 선택하고 결과 무작위 뽑기를 눌러주세요.")
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

MPTI_KEYS = sorted(mpti_results.keys())


def parse_stat_percentage(stat_text: str) -> float | None:
    match = re.search(r"(\d{1,3})%", stat_text)
    if match:
        value = float(match.group(1))
        return min(max(value, 0.0), 100.0)
    return None


def display_result(mpti_key: str) -> None:
    if mpti_key not in mpti_results:
        st.error("유효하지 않은 MPTI 키입니다. 사이드바에서 올바른 키를 선택하세요.")
        return

    result = st.session_state.get("selected_result")
    if not result or st.session_state.get("selected_key") != mpti_key:
        result = random.choice(mpti_results[mpti_key])
        st.session_state.selected_result = result
        st.session_state.selected_key = mpti_key

    st.subheader(f"결과 유형: {mpti_key}")
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

    st.write("---")
    with st.container():
        st.subheader("🎨 AI 이미지 생성 프롬프트")
        st.code(result["image_prompt"], language="text")


with st.sidebar:
    st.header("테스트 입력")
    selected_key = st.selectbox("MPTI 키 선택", MPTI_KEYS)
    if st.button("결과 무작위 뽑기"):
        st.session_state.selected_result = random.choice(mpti_results[selected_key])
        st.session_state.selected_key = selected_key

    st.write("---")
    st.write("현재 선택된 키:")
    st.markdown(f"**{selected_key}**")


display_result(st.session_state.get("selected_key", MPTI_KEYS[0]))
