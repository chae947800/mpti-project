import streamlit as st
import json
from pathlib import Path

# 프로젝트 최상위 폴더의 users.json을 참조
DATA_FILE = Path(__file__).resolve().parents[1] / "users.json"

def load_users():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def dashboard_page():
    # 1. 로그인 세션 확인
    if "username" not in st.session_state:
        st.warning("로그인이 필요합니다.")
        if st.button("로그인 페이지로", key="go_auth_btn"):
            st.switch_page("pages/auth.py")
        st.stop()

    users = load_users()
    my_id = st.session_state.username
    me = users.get(my_id, {"name": "게스트", "mpti": "미정", "playlist": [], "friends": []})

    # 2. UI 구성
    st.title(f"👋 {me['name']}님의 대시보드")
    
    # 내 정보 및 플레이리스트 영역
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("내 정보")
        st.metric("현재 MPTI", me.get('mpti', '미정'))
        if st.button("🎵 음악 MPTI 검사하기", key="go_test_btn"):
            st.switch_page("pages/test.py")
            
    with col2:
        st.subheader("내 플레이리스트")
        # 곡 추가 기능 (key 고유화)
        new_song = st.text_input("새 곡 추가하기", key="new_song_input")
        if st.button("추가", key="add_my_song_btn"):
            if new_song:
                me.setdefault("playlist", []).append(new_song)
                users[my_id] = me
                save_users(users)
                st.rerun()
        
        for i, song in enumerate(me.get('playlist', [])):
            st.write(f"▶️ {song}")

    st.write("---")

    # 3. 친구 관리 및 조회 영역
    st.subheader("👥 친구 목록")
    
    with st.expander("친구 추가하기"):
        friend_id = st.text_input("친구 아이디 입력", key="friend_id_input")
        if st.button("추가", key="add_friend_btn"):
            if friend_id in users and friend_id != my_id:
                if friend_id not in me.get("friends", []):
                    me.setdefault("friends", []).append(friend_id)
                    users[my_id] = me
                    save_users(users)
                    st.success("친구 추가 완료!")
                    st.rerun()
            else:
                st.error("존재하지 않는 유저이거나 본인입니다.")

    # 친구 상세 정보 출력
    for f_id in me.get("friends", []):
        if f_id in users:
            friend = users[f_id]
            # expander 키값도 고유하게 설정
            with st.expander(f"👤 {friend['name']} ({friend['mpti']})"):
                st.write(f"**MPTI**: {friend['mpti']}")
                st.write("**플레이리스트**:")
                for i, song in enumerate(friend.get('playlist', [])):
                    # 버튼 키에 인덱스를 포함하여 고유성 확보
                    if st.button(f"➕ {song}", key=f"add_{f_id}_{i}_{song}"):
                        if song not in me.get("playlist", []):
                            me.setdefault("playlist", []).append(song)
                            users[my_id] = me
                            save_users(users)
                            st.success(f"'{song}' 추가 완료!")
                            st.rerun()
        else:
            st.write(f"아이디 {f_id}: 존재하지 않는 유저입니다.")

    # 로그아웃
    if st.button("로그아웃", key="logout_btn"):
        st.session_state.clear()
        st.switch_page("pages/auth.py")

if __name__ == "__main__":
    dashboard_page()