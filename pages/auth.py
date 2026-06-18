import streamlit as st
import json
from pathlib import Path

# 프로젝트 루트의 users.json을 참조
DATA_DIR = Path(__file__).resolve().parents[1]
USERS_FILE = DATA_DIR / "users.json"

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def handle_login(username, password):
    users = load_users()
    if username in users and users[username].get("password") == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.switch_page("pages/dashboard.py")
    else:
        st.error("❌ 아이디 또는 비밀번호가 틀렸습니다.")

def main():
    st.set_page_config(page_title="로그인/회원가입", layout="centered")
    st.title("🔐 MPTI 인증 시스템")
    
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    
    with tab1:
        with st.form("login_form"):
            user_id = st.text_input("아이디")
            user_pw = st.text_input("비밀번호", type="password")
            if st.form_submit_button("🔓 로그인"):
                handle_login(user_id, user_pw)

    with tab2:
        with st.form("signup_form"):
            name = st.text_input("이름")
            uid = st.text_input("아이디")
            pw = st.text_input("비밀번호", type="password")
            if st.form_submit_button("✍️ 회원가입"):
                users = load_users()
                if uid in users:
                    st.error("이미 존재하는 아이디입니다.")
                elif not name or not uid or not pw:
                    st.error("모든 항목을 입력해주세요.")
                else:
                    # 데이터 구조를 초기화하여 저장
                    users[uid] = {
                        "name": name,
                        "password": pw,
                        "mpti": "미정",
                        "playlist": [],
                        "friends": []
                    }
                    save_users(users)
                    st.success("가입 완료! 로그인 탭에서 로그인하세요.")

if __name__ == "__main__":
    main()