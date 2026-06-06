import streamlit as st
import json
import os
from pathlib import Path


# ==================== 데이터 저장 경로 설정 ====================
DATA_DIR = Path(__file__).parent.parent
USERS_FILE = DATA_DIR / "users.json"


# ==================== 파일 초기화 함수 ====================
def initialize_users_file():
    """users.json 파일이 없을 경우 자동으로 생성"""
    if not USERS_FILE.exists():
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)


# ==================== 회원 정보 로드 및 저장 함수 ====================
def load_users():
    """users.json에서 회원 정보 로드"""
    initialize_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return users


def save_users(users):
    """회원 정보를 users.json에 저장"""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# ==================== 회원가입 함수 ====================
def handle_signup(name, username, password):
    """회원가입 처리 함수"""
    users = load_users()
    
    # 아이디 중복 확인
    if username in users:
        st.error("❌ 이미 존재하는 아이디는 이용할 수 없습니다.")
        return False
    
    # 새로운 사용자 추가
    users[username] = {
        "name": name,
        "password": password
    }
    save_users(users)
    st.success("✅ 회원가입이 완료되었습니다! 로그인해 주세요.")
    return True


# ==================== 로그인 함수 ====================
def handle_login(username, password):
    """로그인 처리 함수"""
    users = load_users()
    
    # 아이디 확인
    if username not in users:
        st.error("❌ 회원가입 먼저 진행해 주세요.")
        return False
    
    # 비밀번호 확인
    if users[username]["password"] != password:
        st.error("❌ 비밀번호가 일치하지 않습니다.")
        return False
    
    # 로그인 성공
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_name = users[username]["name"]
    st.success(f"✅ 환영합니다, {users[username]['name']}님!")
    return True


# ==================== Streamlit UI ====================
def main():
    st.set_page_config(page_title="인증", layout="centered")
    
    # 페이지 타이틀
    st.title("🔐 MPTI 인증 시스템")
    
    # 로그인/회원가입 모드 선택
    auth_mode = st.radio(
        "모드 선택",
        ["로그인", "회원가입"],
        horizontal=True
    )
    
    st.divider()
    
    if auth_mode == "로그인":
        st.subheader("🔑 로그인")
        with st.form("login_form"):
            username = st.text_input(
                "아이디",
                placeholder="아이디를 입력하세요"
            )
            password = st.text_input(
                "비밀번호",
                type="password",
                placeholder="비밀번호를 입력하세요"
            )
            
            submit_button = st.form_submit_button(
                "🔓 로그인",
                use_container_width=True
            )
            
            if submit_button:
                if not username or not password:
                    st.error("❌ 아이디와 비밀번호를 모두 입력해주세요.")
                else:
                    handle_login(username, password)
    
    else:  # 회원가입
        st.subheader("📝 회원가입")
        with st.form("signup_form"):
            name = st.text_input(
                "이름",
                placeholder="이름을 입력하세요"
            )
            username = st.text_input(
                "아이디",
                placeholder="아이디를 입력하세요"
            )
            password = st.text_input(
                "비밀번호",
                type="password",
                placeholder="비밀번호를 입력하세요"
            )
            
            submit_button = st.form_submit_button(
                "✍️ 회원가입",
                use_container_width=True
            )
            
            if submit_button:
                if not name or not username or not password:
                    st.error("❌ 이름, 아이디, 비밀번호를 모두 입력해주세요.")
                else:
                    handle_signup(name, username, password)


if __name__ == "__main__":
    main()
