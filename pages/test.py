import streamlit as st

st.set_page_config(page_title="MPTI 음악 성격 유형 검사", page_icon="🎵")

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "test_page" not in st.session_state:
    st.session_state.test_page = 1

st.title("🎵 MPTI 음악 성격 유형 검사")
st.write("모든 문항을 읽고 당신과 더 가까운 답변을 골라주세요.")
st.markdown("---")

def save_answers(page_questions):
    # 라디오 버튼 선택지 텍스트에서 (A)가 포함되어 있으면 "A", 아니면 "B"로 깔끔하게 저장
    for key, value in page_questions.items():
        if value is not None:
            st.session_state.answers[key] = "A" if "(A)" in str(value) else "B"

def compute_final_key():
    # 저장된 answers 딕셔너리에서 안전하게 값을 꺼내와 4글자 키 계산
    h_l = "H" if sum(1 for i in range(1, 6) if st.session_state.answers.get(f"q{i}") == "A") >= 3 else "L"
    v_i = "V" if sum(1 for i in range(6, 11) if st.session_state.answers.get(f"q{i}") == "A") >= 3 else "I"
    f_s = "F" if sum(1 for i in range(11, 16) if st.session_state.answers.get(f"q{i}") == "A") >= 3 else "S"
    n_o = "N" if sum(1 for i in range(16, 21) if st.session_state.answers.get(f"q{i}") == "A") >= 3 else "O"
    return h_l + v_i + f_s + n_o

# 기존 답변이 있으면 기억하고, 없으면 None(빈 상태)으로 설정하는 든든한 함수
def get_default_index(q_key):
    saved = st.session_state.answers.get(q_key)
    if saved == "A":
        return 0
    elif saved == "B":
        return 1
    return None

# ------------------------------------------------------------------
# PAGE 1: H / L (무거운 vs 가벼운)
# ------------------------------------------------------------------
if st.session_state.test_page == 1:
    st.subheader("🔵 STEP 1. 사운드의 무게감 (1/4)")

    q1 = st.radio(
        "1. 음악을 들을 때 볼륨이나 사운드의 무게감에 대한 내 선호도는?",
        [
            " (A) 이어폰 볼륨을 크게 키우거나, 스피커의 베이스(우퍼)를 빵빵하게 켜서 가슴이 쿵쿵 울리는 타격감을 느껴야 제맛이다.",
            " (B) 귀가 피로한 건 딱 질색이다. 잔잔하고 편안한 볼륨으로, 귀에 부담 없이 부드럽게 스며드는 사운드를 좋아한다."
        ],
        key="q1_radio", index=get_default_index("q1")
    )
    q2 = st.radio(
        "2. 내가 스트레스를 격하게 받았을 때 찾게 되는 음악은?",
        [
            " (A) 귀가 얼얼할 정도로 강렬한 사운드나 웅장하고 꽉 찬 음악을 틀어놓고 감정을 확 분출시킨다.",
            " (B) 조용하고 맑은 뉴에이지, 어쿠스틱, 혹은 자연의 소리가 섞인 미니멀한 음악을 들으며 마음을 차분하게 가라앉힌다."
        ],
        key="q2_radio", index=get_default_index("q2")
    )
    q3 = st.radio(
        "3. 음악을 들으며 길을 걸을 때, 내 안의 '에너지' 상태는?",
        [
            " (A) 강력한 비트에 동화되어 나도 모르게 걸음걸이가 당당해지고, 마치 내가 영화 속 화끈한 주인공이 된 듯한 도파민을 즐긴다.",
            " (B) 맑고 산뜻한 멜로디를 들으며 발걸음이 가벼워지고, 일상의 소소한 풍경들을 여유롭게 눈에 담으며 평화로움을 느낀다."
        ],
        key="q3_radio", index=get_default_index("q3")
    )
    q4 = st.radio(
        "4. 영화나 드라마 OST 중 내가 더 깊게 매료되는 스타일은?",
        [
            " (A) 거대한 오케스트라, 화려한 액션 신에 어울리는 강렬한 록 사운드처럼 화면을 압도하는 스케일 큰 음악.",
            " (B) 일상적인 대화 뒤로 잔잔하게 깔리는 피아노 선율이나 청량한 인디 음악처럼 공간감 있고 담백한 음악."
        ],
        key="q4_radio", index=get_default_index("q4")
    )
    q5 = st.radio(
        "5. 지인이 나에게 플레이리스트를 추천해 주었을 때, 내가 더 선호하는 구성은?",
        [
            " (A) 사운드가 촘촘하고 악기나 소스가 꽉 차 있어서 지루할 틈 없이 귀를 사로잡는 화려하고 밀도 높은 리스트.",
            " (B) 악기 소리가 몇 개 없고 여백의 미가 느껴져서, 배경음악(BGM)처럼 편안하게 틀어놓기 좋은 미니멀한 리스트."
        ],
        key="q5_radio", index=get_default_index("q5")
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        pass 
    with col2:
        if st.button("다음 단계로 ➡️", key="btn_p1_next"):
            if None in [q1, q2, q3, q4, q5]:
                st.error("⚠️ 아직 답변하지 않은 문항이 있습니다. 모든 문항에 체크해 주세요!")
            else:
                save_answers({"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5})
                st.session_state.test_page = 2
                st.rerun()

# ------------------------------------------------------------------
# PAGE 2: V / I (보컬 vs 악기)
# ------------------------------------------------------------------
elif st.session_state.test_page == 2:
    st.subheader("🎤 STEP 2. 보컬과 세션 (2/4)")

    q6 = st.radio(
        "6. 새로운 노래를 들을 때 내 신경이 가장 먼저, 그리고 가장 강하게 꽂히는 곳은?",
        [
            " (A) 보컬의 음색, 가창력, 그리고 전달되는 고유의 감정과 감탄이 나오는 파트(킬링파트).",
            " (B) 베이스 라인, 드럼 비트, 신디사이저 사운드나 독특한 악기 세션의 전개 방식."
        ],
        key="q6_radio", index=get_default_index("q6")
    )
    q7 = st.radio(
        "7. 좋아하는 곡의 '가사'를 대하는 나의 태도는?",
        [
            " (A) 가사의 의미를 곱씹으며 내 상황에 대입해 보거나, 한 편의 시처럼 공감하며 감동을 받는다.",
            " (B) 가사는 그저 하나의 '소리(멜로디)'로 들릴 뿐, 가사의 구체적인 의미보다는 전체적인 사운드 구조에 집중한다."
        ],
        key="q7_radio", index=get_default_index("q7")
    )
    q8 = st.radio(
        "8. 노래방에 가거나 혼자 흥얼거릴 때, 내가 더 즐거움을 느끼는 순간은?",
        [
            " (A) 매력적인 보컬을 흉내 내며 내 목소리로 감정을 가득 담아 노래를 따라 부를 때.",
            " (B) 노래를 부르기보다 뒤에 깔리는 반주(MR)의 리듬을 타거나, 손가락으로 드럼 비트를 두드리고 악기 소리를 입으로 흉내 낼 때."
        ],
        key="q8_radio", index=get_default_index("q8")
    )
    q9 = st.radio(
        "9. 만약 내가 직접 음악을 만드는 아티스트가 된다면, 가장 공들여 작업하고 싶은 파트는?",
        [
            " (A) 사람들의 심금을 울리는 멜로디 라인을 짜고, 진정성 있는 메시지를 담은 가사를 쓰는 일.",
            " (B) 세련된 코드를 짜고, 완벽한 비트와 신선한 악기 소리들을 배치하여 곡의 완성도 높은 구조를 만드는 일."
        ],
        key="q9_radio", index=get_default_index("q9")
    )
    q10 = st.radio(
        "10. 내가 평소에 대화하거나 사람을 파악할 때의 성향과 더 가까운 것은?",
        [
            " (A) 상대방의 말투, 뉘앙스, 표정에서 느껴지는 '감정'에 깊게 공감하고 인간적인 연결감을 중요하게 생각한다.",
            " (B) 상대방이 말하는 내용의 '논리'와 상황의 전체적인 '구조'를 파악하며, 혼자 사색하는 시간을 더 편안하게 느낀다."
        ],
        key="q10_radio", index=get_default_index("q10")
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전 단계", key="btn_p2_prev"):
            # 이전으로 가기 전 현재 페이지 답변 중간 저장 (사라짐 방지)
            save_answers({"q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10})
            st.session_state.test_page = 1
            st.rerun()
    with col2:
        if st.button("다음 단계로 ➡️", key="btn_p2_next"):
            if None in [q6, q7, q8, q9, q10]:
                st.error("⚠️ 아직 답변하지 않은 문항이 있습니다. 모든 문항에 체크해 주세요!")
            else:
                save_answers({"q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10})
                st.session_state.test_page = 3
                st.rerun()

# ------------------------------------------------------------------
# PAGE 3: F / S (빠른 vs 느린)
# ------------------------------------------------------------------
elif st.session_state.test_page == 3:
    st.subheader("⚡ STEP 3. 템포와 에너지 (3/4)")

    q11 = st.radio(
        "11. 음악의 템포(박자)가 내 실제 행동이나 텐션에 미치는 영향은?",
        [
            " (A) 비트가 빨라지면 심장이 뛰고 텐션이 올라가며, 내적 댄스를 추거나 당장이라도 무언가 시작하고 싶어진다.",
            " (B) 음악은 나를 진정시켜 주는 도구다. 박자가 여유롭고 느릴 때 비로소 마음이 편안해지고 깊은 생각에 잠길 수 있다."
        ],
        key="q11_radio", index=get_default_index("q11")
    )
    q12 = st.radio(
        "12. 평소에 일을 하거나 공부를 할 때 작업용 음악(노동요)을 고르는 기준은?",
        [
            " (A) 신나고 빠른 비트의 음악을 틀어서 지루함을 날려버리고, 속도감 있게 효율을 높여 마무리를 지어야 한다.",
            " (B) 잔잔하고 느린 템포의 음악을 잔잔하게 깔아두고, 차분하고 집중력 있게 깊이 몰입하는 것을 선호한다."
        ],
        key="q12_radio", index=get_default_index("q12")
    )
    q13 = st.radio(
        "13. 주말이나 휴일에 집에서 휴식을 취할 때, 내 이상적인 분위기는?",
        [
            " (A) 힙하고 트렌디한 카페나 페스티벌에 온 것처럼 고조된 에너지를 주는 다이내믹한 분위기.",
            " (B) 비 오는 날 창밖을 바라보거나, 따뜻한 차 한 잔을 마시며 흘러가는 시간을 음미하는 여유롭고 정적인 분위기."
        ],
        key="q13_radio", index=get_default_index("q13")
    )
    q14 = st.radio(
        "14. 내가 일상에서 무언가 결정을 내릴 때(예: 여행 계획, 쇼핑 등)의 스타일은?",
        [
            " (A) \"이거다!\" 싶으면 지체 없이 바로 실행에 옮긴다. 지루하게 끄는 것보다 빠르게 결과를 보는 게 좋다.",
            " (B) 돌다리도 두들겨 보고 건넌다. 서두르지 않고 차근차근 계획을 세우며, 과정 자체에서 오는 여유를 즐긴다."
        ],
        key="q14_radio", index=get_default_index("q14")
    )
    q15 = st.radio(
        "15. 친구들과의 약속 시간에 늦을 것 같을 때, 혹은 급한 상황에서 내 머릿속에 흐르는 음악의 속도는?",
        [
            " (A) 심장을 쫄깃하게 만드는 쾌속 비트처럼 머릿속이 바쁘게 돌아가며 발걸음이 엄청나게 빨라진다.",
            " (B) '어쩔 수 없지' 하고 마인드 컨트롤을 하듯, 차분하고 의연한 호짐을 유지하려고 노력한다."
        ],
        key="q15_radio", index=get_default_index("q15")
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전 단계", key="btn_p3_prev"):
            # 이전으로 가기 전 현재 페이지 답변 중간 저장 (사라짐 방지)
            save_answers({"q11": q11, "q12": q12, "q13": q13, "q14": q14, "q15": q15})
            st.session_state.test_page = 2
            st.rerun()
    with col2:
        if st.button("다음 단계로 ➡️", key="btn_p3_next"):
            if None in [q11, q12, q13, q14, q15]:
                st.error("⚠️ 아직 답변하지 않은 문항이 있습니다. 모든 문항에 체크해 주세요!")
            else:
                save_answers({"q11": q11, "q12": q12, "q13": q13, "q14": q14, "q15": q15})
                st.session_state.test_page = 4
                st.rerun()

# ------------------------------------------------------------------
# PAGE 4: N / O (최신 vs 레트로)
# ------------------------------------------------------------------
elif st.session_state.test_page == 4:
    st.subheader("🟢 STEP 4. 당신의 트렌드 민감도 (4/4)")

    q16 = st.radio(
        "16. 친구들과의 대화나 SNS에서 최근 유행하는 챌린지 송이나 밈(Meme) 음악을 접했을 때 내 태도는?",
        [
            ' (A) "아, 이게 요즘 유행하는 거구나!" 하면서 흥미롭게 찾아보고, 귀에 맴돌아 한동안 찾아 듣는다.',
            " (B) 잠깐 신기해할 뿐, 자극적이고 가벼운 유행어 반복처럼 느껴져 금방 질리거나 내 취향이 아니라고 느낀다."
        ],
        key="q16_radio", index=get_default_index("q16")
    )
    q17 = st.radio(
        "17. 길을 걷거나 카페에 있을 때, 한 번도 들어본 적 없는 세련되고 독특한 노래가 흘러나온다면?",
        [
            "(A) 귀가 번쩍 뜨여서 음악 검색 앱(샤잠 등)을 켜서 제목이 무엇인지 반드시 찾아내고 저장한다.",
            "(B) '노래 좋네' 하고 잠깐 귀를 기울이지만, 굳이 찾아보진 않고 이내 내 생각에 집중하거나 넘긴다."
        ],
        key="q17_radio", index=get_default_index("q17")
    )
    q18 = st.radio(
        "18. 스트리밍 앱(멜론, 스포티파이 등)을 켰을 때 내가 가장 먼저 누르는 메뉴나 행동은?",
        [
            "(A) '실시간 차트', '이번 주 발매 신곡', 또는 AI가 추천해 주는 '새로운 취향 저격 플레이리스트'를 탐색한다.",
            "(B) 내가 직접 손으로 꾹꾹 눌러 담아둔 '나만의 오래된 재생목록'이나 익숙한 최애 앨범을 재생한다."
        ],
        key="q18_radio", index=get_default_index("q18")
    )
    q19 = st.radio(
        "19. 음악을 들을 때 사운드의 분위기나 질감 중 내가 더 매력을 느끼는 쪽은?",
        [
            "(A) 귀를 정밀하게 자극하는 세련된 컴퓨터 그래픽 같은 사운드나, 요즘 유행하는 미래지향적인 이색 효과음.",
            "(B) LP판의 지직거림, 통기타 줄 튕기는 소리, 실제 드럼 소리처럼 아날로그적이고 따뜨한 인간미가 느껴지는 사운드."
        ],
        key="q19_radio", index=get_default_index("q19")
    )
    q20 = st.radio(
        "20. 내가 생각하는 '완벽한 음악 플레이리스트'의 조건은 무엇인가?",
        [
            "(A) 끊임없이 업데이트되는 물과 같아야 한다. 새로운 곡이 계속 유입되고, 질린 곡은 빠르게 삭제되는 살아있는 리스트.",
            "(B) 시간이 흘러도 변치 않는 박물관 같아야 한다. 몇 년째 순서조차 바뀌지 않고 그대로 유지되어 언제 틀어도 편안한 리스트."
        ],
        key="q20_radio", index=get_default_index("q20")
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전 단계", key="btn_p4_prev"):
            save_answers({"q16": q16, "q17": q17, "q18": q18, "q19": q19, "q20": q20})
            st.session_state.test_page = 3
            st.rerun()
    with col2:
        if st.button("🏁 결과 제출하기", key="btn_p4_submit"):
            if None in [q16, q17, q18, q19, q20]:
                st.error("⚠️ 아직 답변하지 않은 문항이 있습니다. 모든 문항에 체크해 주세요!")
            else:
                save_answers({"q16": q16, "q17": q17, "q18": q18, "q19": q19, "q20": q20})
                # 💡 최종 키를 깨끗하게 계산해서 결과 세션에 저장합니다.
                st.session_state["selected_key"] = compute_final_key()
                st.switch_page("pages/test_result.py")