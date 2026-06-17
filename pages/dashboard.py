import streamlit as st
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1]
USERS_FILE = DATA_DIR / "users.json"

def load_users():
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except:
            return {}
    return {}

def save_users(users):
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")

def init_state():
    st.session_state.setdefault("screen", "main")
    st.session_state.setdefault("me", {"name": "나", "mpti": "AMPX", "playlist": []})
    st.session_state.setdefault("selected_friend", None)
    st.session_state.setdefault("selected_friend_id", None)
    st.session_state.setdefault("users", load_users())

def main_screen():
    users = st.session_state.users
    left, right = st.columns([1, 2])

    with left:
        q = st.text_input("검색", key="search_left")
        st.write("친구 목록")
        
        for uid, uinfo in users.items():
            name = uinfo.get("name", uid)
            mpti = uinfo.get("mpti", "미정")
            
            if q and (q.lower() not in name.lower() and q.lower() not in mpti.lower()):
                continue
                
            if st.button(f"{name} ({mpti})", key=f"f_{uid}"):
                st.session_state.selected_friend = uinfo
                st.session_state.selected_friend_id = uid
                st.session_state.screen = "friend"
                st.rerun()

        if st.button("친구추가"):
            st.session_state.screen = "add_friend"
            st.rerun()

    with right:
        col1, col2 = st.columns([1, 3])
        with col1:
            # 에러 방지를 위해 st.image 주석 처리
            pass
        with col2:
            st.write(f"이름: {st.session_state.me['name']}")
        
        # ◀ 이 부분들의 들여쓰기를 일관되게 정렬했습니다.
        st.write(f"내 MPTI: {st.session_state.me['mpti']}")
        st.write("내 플레이리스트")
        for i, t in enumerate(st.session_state.me["playlist"]):
            st.write(f"{i+1}. {t}")

        if st.button("음악 추가"):
            st.session_state.screen = "add_music"
            st.rerun()

def friend_screen():
    u = st.session_state.selected_friend
    uid = st.session_state.selected_friend_id
    if not u:
        st.session_state.screen = "main"
        st.rerun()
        return
    left, right = st.columns([1, 2])
    with left:
        st.write(f"이름: {u.get('name')}")
        st.write(f"MPTI: {u.get('mpti', '미정')}")
        if st.button("메인으로"):
            st.session_state.screen = "main"
            st.rerun()
    with right:
        st.write(f"{u.get('name')}의 플레이리스트")
        for i, t in enumerate(u.get("playlist", [])):
            cols = st.columns([6,1])
            cols[0].write(f"{i+1}. {t}")
            if cols[1].button("+", key=f"add_{uid}_{i}"):
                st.session_state.me["playlist"].insert(0, t)
                st.success("내 플레이리스트에 추가되었습니다")
                st.rerun()

def add_friend_screen():
    st.write("친구 추가")
    uid = st.text_input("추가할 친구 아이디", key="add_friend_id")
    if st.button("추가"):
        users = st.session_state.users
        if uid in users:
            st.success(f"{users[uid].get('name')} 님이 친구로 확인되었습니다.")
            st.session_state.screen = "main"
            st.rerun()
        else:
            st.error("입력하신 아이디의 회원이 존재하지 않습니다")
            st.session_state.add_friend_id = ""

    if st.button("메인으로", key="back_from_add"):
        st.session_state.screen = "main"
        st.rerun()

SAMPLE_MUSIC = [
    {"id": "1", "title": "Song A", "artist": "Artist 1"},
    {"id": "2", "title": "Song B", "artist": "Artist 2"},
    {"id": "3", "title": "Song C", "artist": "Artist 1"},
]

def add_music_screen():
    q = st.text_input("음악 검색 (가수/곡)", key="music_search")
    results = [m for m in SAMPLE_MUSIC if not q or q.lower() in m['title'].lower() or q.lower() in m['artist'].lower()]
    picks = {}
    for m in results:
        picks[m['id']] = st.checkbox(f"{m['title']} - {m['artist']}", key=f"chk_{m['id']}")

    if st.button("+"):
        added = 0
        for m in results:
            if picks.get(m['id']):
                st.session_state.me['playlist'].insert(0, f"{m['title']} - {m['artist']}")
                added += 1
        st.success(f"{added}곡 추가됨")
        st.session_state.screen = "main"
        st.rerun()

    if st.button("메인으로", key="back_from_music"):
        st.session_state.screen = "main"
        st.rerun()

def app():
    init_state()
    st.title("mpti - 메인")
    screen = st.session_state.screen
    if screen == "main":
        main_screen()
    elif screen == "friend":
        friend_screen()
    elif screen == "add_friend":
        add_friend_screen()
    elif screen == "add_music":
        add_music_screen()

if __name__ == "__main__":
    app()