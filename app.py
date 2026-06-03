import streamlit as st

st.set_page_config(page_title="MPTI", page_icon="🎧", layout="centered")

st.title("나의 음악 취향 성격 유형 MPTI 테스트")
st.markdown("#### Music Personality Type Indicator")

st.write("---")

if st.button("시작하기"):
    st.success("MPTI 테스트를 시작합니다.")
