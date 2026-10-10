import random
import streamlit as st

# =========================================================
# LINGUAPLAY — игровой тренажёр иностранных языков
# =========================================================

st.set_page_config(
    page_title="LinguaPlay | Learn by Playing",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------- ДИЗАЙН ----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    color-scheme: dark;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #20204b 0%, transparent 35%),
        linear-gradient(145deg, #080d19, #0b1020 60%, #10132b);
    color: #f5f6ff;
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    letter-spacing: -0.7px;
}

[data-testid="stMetric"] {
    background: #111b30;
    border: 1px solid #293858;
    border-radius: 18px;
    padding: 17px;
}

[data-testid="stMetricValue"] {
    color: #a99aff;
}

div.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 13px;
    border: 1px solid #45427c;
    background: linear-gradient(120deg, #7048ff, #9a57ed);
    color: white;
    font-weight: 700;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    border-color: #c4b5fd;
    filter: brightness(1.12);
    transform: translateY(-1px);
}

div[data-testid="stRadio"] label {
    background: #111b30;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 5px;
    border: 1px solid #293858;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] input {
    background: #111b30;
    border-radius: 12px;
}

.hero {
    background: linear-gradient(120deg, #211b50, #151e37 65%, #123c42);
    border: 1px solid #494080;
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    line-height: 1.12;
    margin-bottom: 12px;
}

.muted {
    color: #a9b4cf;
}

.game-card {
    background: linear-gradient(145deg, #141e35, #101526);
    border: 1px solid #303c5d;
    padding: 22px;
    border-radius: 20px;
    margin-bottom: 12px;
}

.word {
    font-size: 32px;
    font-weight: 800;
    text-align: center;
    padding: 22px 0;
    color: #c4b5fd;
}

.pill {
    display: inline-block;
    border-radius: 20px;
    padding: 6px 12px;
    background: #29214d;
    color: #d7ccff;
    font-size: 12px;
    margin-right: 5px;
}

hr {
    border-color: #283450;
}

section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #222c45;
}
</style>
""", unsafe_allow_html=True)


# ---------------------- УЧЕБНАЯ БАЗА ----------------------

# Каждый элемент содержит слово на изучаемом языке,
# переводы для интерфейсов RU / UZ / EN,
# произношение китайского языка и сложность.

WORDS = {
    "en": [
        ("apple", "яблоко", "olma", "apple", 1, ""),
        ("water", "вода", "suv", "water", 1, ""),
        ("friend", "друг", "do'st", "friend", 1, ""),
        ("beautiful", "красивый", "chiroyli", "beautiful", 2, ""),
        ("journey", "путешествие", "sayohat", "journey", 2, ""),
        ("improve", "улучшать", "yaxshilamoq", "improve", 2, ""),
        ("opportunity", "возможность", "imkoniyat", "opportunity", 3, ""),
        ("achievement", "достижение", "yutuq", "achievement", 3, ""),
    ],
    "fr": [
        ("bonjour", "здравствуйте", "salom", "hello", 1, ""),
        ("merci", "спасибо", "rahmat", "thank you", 1, ""),
        ("maison", "дом", "uy", "house", 1, ""),
        ("magnifique", "великолепный", "ajoyib", "magnificent", 2, ""),
        ("voyage", "путешествие", "sayohat", "journey", 2, ""),
        ("apprendre", "учиться", "o'rganmoq", "to learn", 2, ""),
        ("épanouissement", "самореализация", "o'zini rivojlantirish",
         "personal growth", 3, ""),
        ("persévérance", "настойчивость", "qat'iyat",
         "perseverance", 3, ""),
    ],
    "de": [
        ("Hallo", "привет", "salom", "hello", 1, ""),
        ("Wasser", "вода", "suv", "water", 1, ""),
        ("Freund", "друг", "do'st", "friend", 1, ""),
        ("wunderschön", "прекрасный", "juda chiroyli", "beautiful", 2, ""),
        ("Erfahrung", "опыт", "tajriba", "experience", 2, ""),
        ("verbessern", "улучшать", "yaxshilamoq", "to improve", 2, ""),
        ("Herausforderung", "вызов", "qiyinchilik", "challenge", 3, ""),
        ("Zuverlässigkeit", "надёжность", "ishonchlilik", "reliability", 3, ""),
    ],
    "ru": [
        ("привет", "привет", "salom", "hello", 1, ""),
        ("вода", "вода", "suv", "water", 1, ""),
        ("друг", "друг", "do'st", "friend", 1, ""),
        ("путешествие", "путешествие", "sayohat", "journey", 2, ""),
        ("впечатление", "впечатление", "taassurot", "impression", 2, ""),
        ("развиваться", "развиваться", "rivojlanmoq", "to develop", 2, ""),
        ("целеустремлённость", "целеустремлённость",
         "maqsadga intilish", "determination", 3, ""),
        ("самостоятельность", "самостоятельность",
         "mustaqillik", "independence", 3, ""),
    ],
    "zh": [
        ("你好", "привет", "salom", "hello", 1, "nǐ hǎo"),
        ("水", "вода", "suv", "water", 1, "shuǐ"),
        ("朋友", "друг", "do'st", "friend", 1, "péngyou"),
        ("漂亮", "красивый", "chiroyli", "beautiful", 2, "piàoliang"),
        ("旅行", "путешествие", "sayohat", "journey", 2, "lǚxíng"),
        ("学习", "учиться", "o'rganmoq", "to learn", 2, "xuéxí"),
        ("坚持", "настойчивость", "qat'iyat", "perseverance", 3, "jiānchí"),
        ("机会", "возможность", "imkoniyat", "opportunity", 3, "jīhuì"),
    ],
}

LANGUAGES = {
    "en": "🇬🇧 English",
    "fr": "🇫🇷 Français",
    "de": "🇩🇪 Deutsch",
    "ru": "🇷🇺 Русский",
    "zh": "🇨🇳 中文",
}

INTERFACE = {
    "Русский": "ru",
    "O'zbekcha": "uz",
    "English": "en",
}

UI = {
    "ru": {
        "subtitle": "Учись играя. Говори свободно.",
        "start": "Начать обучение",
        "home": "Главная",
        "game": "Игры",
        "cards": "Карточки",
        "profile": "Мой прогресс",
        "target": "Какой язык изучаем?",
        "base": "Язык объяснений",
        "difficulty": "Сложность",
        "easy": "Начальный",
        "medium": "Средний",
        "hard": "Продвинутый",
        "all": "Все уровни",
        "quiz": "Викторина",
        "flash": "Карточки слов",
        "phrase": "Испытание перевода",
        "xp": "Опыт",
        "correct": "Правильные ответы",
        "attempts": "Всего ответов",
        "streak": "Серия правильных ответов",
        "question": "Как переводится это слово?",
        "check": "Проверить ответ",
        "next": "Следующее задание",
        "right": "Отлично! Верный ответ.",
        "wrong": "Пока неверно. Правильный ответ:",
        "reveal": "Показать перевод",
        "new_card": "Следующая карточка",
        "translate": "Переведите фразу",
        "write": "Введите перевод на изучаемом языке",
        "welcome": "Откройте для себя новый язык",
        "goal": "Ваша цель на сегодня",
        "tip": "Совет дня",
        "tip_text": "Лучше заниматься 5–10 минут каждый день, чем учить всё за один вечер.",
        "progress": "Ваш прогресс",
        "complete": "Вы прошли",
        "beginner": "Начните с простых слов",
        "no_data": "Прогресс появится после первых заданий.",
        "correct_answer": "Ответ",
    },
    "uz": {
        "subtitle": "O'ynab o'rganing. Erkin gapiring.",
        "start": "O'rganishni boshlash",
        "home": "Bosh sahifa",
        "game": "O'yinlar",
        "cards": "Kartochkalar",
        "profile": "Mening natijam",
        "target": "Qaysi tilni o'rganamiz?",
        "base": "Izohlar tili",
        "difficulty": "Qiyinlik darajasi",
        "easy": "Boshlang'ich",
        "medium": "O'rta",
        "hard": "Yuqori",
        "all": "Barcha darajalar",
        "quiz": "Viktorina",
        "flash": "So'z kartochkalari",
        "phrase": "Tarjima sinovi",
        "xp": "Tajriba",
        "correct": "To'g'ri javoblar",
        "attempts": "Jami javoblar",
        "streak": "Ketma-ket to'g'ri javoblar",
        "question": "Bu so'z qanday tarjima qilinadi?",
        "check": "Javobni tekshirish",
        "next": "Keyingi topshiriq",
        "right": "Ajoyib! To'g'ri javob.",
        "wrong": "Hozircha noto'g'ri. To'g'ri javob:",
        "reveal": "Tarjimani ko'rsatish",
        "new_card": "Keyingi kartochka",
        "translate": "Iborani tarjima qiling",
        "write": "O'rganayotgan tilingizda yozing",
        "welcome": "Yangi tilni kashf eting",
        "goal": "Bugungi maqsadingiz",
        "tip": "Kun maslahati",
        "tip_text": "Har kuni 5–10 daqiqa shug'ullanish samarali odat yaratadi.",
        "progress": "Sizning natijangiz",
        "complete": "Siz bajardingiz",
        "beginner": "Oddiy so'zlardan boshlang",
        "no_data": "Natijalar birinchi topshiriqlardan keyin ko'rinadi.",
        "correct_answer": "Javob",
    },
    "en": {
        "subtitle": "Learn through play. Speak with confidence.",
        "start": "Start learning",
        "home": "Home",
        "game": "Games",
        "cards": "Flashcards",
        "profile": "My progress",
        "target": "Which language do you want to learn?",
        "base": "Explanation language",
        "difficulty": "Difficulty",
        "easy": "Beginner",
        "medium": "Intermediate",
        "hard": "Advanced",
        "all": "All levels",
        "quiz": "Quiz",
        "flash": "Vocabulary cards",
        "phrase": "Translation challenge",
        "xp": "Experience",
        "correct": "Correct answers",
        "attempts": "Total answers",
        "streak": "Correct answer streak",
        "question": "What does this word mean?",
        "check": "Check answer",
        "next": "Next challenge",
        "right": "Excellent! Correct answer.",
        "wrong": "Not quite. The correct answer is:",
        "reveal": "Reveal translation",
        "new_card": "Next card",
        "translate": "Translate this phrase",
        "write": "Type in your target language",
        "welcome": "Discover a new language",
        "goal": "Your daily goal",
        "tip": "Daily tip",
        "tip_text": "Five to ten minutes every day can build a lasting habit.",
        "progress": "Your progress",
        "complete": "You completed",
        "beginner": "Start with simple words",
        "no_data": "Your progress will appear after your first exercises.",
        "correct_answer": "Answer",
    },
}

PHRASES = {
    "en": [
        ("Как дела?", "Qalaysiz?", "How are you?", "How are you?"),
        ("Я изучаю английский.", "Men ingliz tilini o'rganyapman.",
         "I am learning English.", "I am learning English."),
        ("Где находится станция?", "Bekat qayerda?",
         "Where is the station?", "Where is the station?"),
    ],
    "fr": [
        ("Доброе утро!", "Xayrli tong!", "Good morning!", "Bonjour !"),
        ("Я хочу кофе.", "Men qahva xohlayman.", "I want coffee.", "Je veux un café."),
        ("Где находится отель?", "Mehmonxona qayerda?",
         "Where is the hotel?", "Où est l'hôtel ?"),
    ],
    "de": [
        ("Доброе утро!", "Xayrli tong!", "Good morning!", "Guten Morgen!"),
        ("Я хочу воды.", "Men suv xohlayman.", "I want water.", "Ich möchte Wasser."),
        ("Где вокзал?", "Vokzal qayerda?", "Where is the station?", "Wo ist der Bahnhof?"),
    ],
    "ru": [
        ("Как вас зовут?", "Ismingiz nima?", "What is your name?", "Как вас зовут?"),
        ("Я не понимаю.", "Men tushunmayapman.", "I don't understand.", "Я не понимаю."),
        ("Сколько это стоит?", "Bu qancha turadi?", "How much is this?", "Сколько это стоит?"),
    ],
    "zh": [
        ("你好！", "Salom!", "Hello!", "你好！"),
        ("我想喝水。", "Men suv ichmoqchiman.", "I want to drink water.", "我想喝水。"),
        ("你叫什么名字？", "Ismingiz nima?", "What is your name?", "你叫什么名字？"),
    ],
}


# ---------------------- СОСТОЯНИЕ -------------------------

def init_state():
    defaults = {
        "xp": 0,
        "correct": 0,
        "attempts": 0,
        "streak": 0,
        "best_streak": 0,
        "answered": False,
        "question": None,
        "options": [],
        "card_index": 0,
        "card_revealed": False,
        "phrase_index": 0,
        "phrase_checked": False,
        "signature": None,
        "lesson_done": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def get_records(target, difficulty):
    records = WORDS[target]
    if difficulty != 0:
        records = [w for w in records if w[4] == difficulty]
    return records


def create_question(target, base, difficulty):
    records = get_records(target, difficulty)
    if len(records) < 2:
        records = WORDS[target]

    item = random.choice(records)
    correct_word = item[0]
    correct_translation = item[1] if base == "ru" else (
        item[2] if base == "uz" else item[3]
    )

    distractors = [
        w[0] for w in records
        if w[0] != correct_word
    ]
    distractors = random.sample(distractors, min(3, len(distractors)))

    options = distractors + [correct_word]
    random.shuffle(options)

    return {
        "item": item,
        "translation": correct_translation,
        "answer": correct_word,
    }, options


def normalize(text):
    return " ".join(text.lower().strip().split()).strip(" .!?。！，,")


# ---------------------- БОКОВАЯ ПАНЕЛЬ --------------------

with st.sidebar:
    st.markdown("## 🌍 LinguaPlay")
    st.caption("LANGUAGE ADVENTURE")

    interface_name = st.selectbox(
        "🌐 Interface / Интерфейс",
        ["Русский", "O'zbekcha", "English"],
        index=0,
    )
    base = INTERFACE[interface_name]
    t = UI[base]

    st.divider()

    target = st.selectbox(
        t["target"],
        list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
    )

    base = INTERFACE[interface_name]

    difficulty_label = st.selectbox(
        t["difficulty"],
        [t["all"], t["easy"], t["medium"], t["hard"]],
    )
    difficulty_map = {
        t["all"]: 0,
        t["easy"]: 1,
        t["medium"]: 2,
        t["hard"]: 3,
    }
    difficulty = difficulty_map[difficulty_label]

    st.divider()

    mode_label = st.radio(
        "🎮 Game mode",
        [t["quiz"], t["flash"], t["phrase"]],
    )

    st.markdown("---")
    st.caption("✨ Small steps. Big progress.")


# Reset active exercise when settings change.
signature = (target, base, difficulty, mode_label)

if st.session_state.signature != signature:
    st.session_state.signature = signature
    st.session_state.question, st.session_state.options = create_question(
        target, base, difficulty
    )
    st.session_state.answered = False
    st.session_state.card_index = 0
    st.session_state.card_revealed = False
    st.session_state.phrase_index = 0
    st.session_state.phrase_checked = False


# ---------------------- ШАПКА -----------------------------

st.markdown(f"""
<div class="hero">
    <div class="pill">✦ YOUR LANGUAGE JOURNEY</div>
    <div class="hero-title">Lingua<span style="color:#b49aff">Play</span> 🚀</div>
    <div style="font-size:18px;font-weight:600">{t["welcome"]}</div>
    <p class="muted">{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric(f"⚡ {t['xp']}", st.session_state.xp)
col2.metric(f"✅ {t['correct']}", st.session_state.correct)
col3.metric(f"🎯 {t['attempts']}", st.session_state.attempts)
col4.metric(f"🔥 {t['streak']}", st.session_state.streak)

st.divider()


# ---------------------- ВИКТОРИНА -------------------------

if mode_label == t["quiz"]:
    st.markdown(f"## 🎯 {t['quiz']}")
    st.caption(f"{LANGUAGES[target]} · {difficulty_label}")

    question = st.session_state.question

    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown(f"<div class='word'>{question['translation']}</div>",
                unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center;color:#a9b4cf'>{t['question']}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    selected = st.radio(
        "Choose an answer / Выберите ответ",
        st.session_state.options,
        key=f"answer_{st.session_state.signature}",
        disabled=st.session_state.answered,
    )

    if not st.session_state.answered:
        if st.button(t["check"], type="primary"):
            st.session_state.attempts += 1
            st.session_state.answered = True

            if selected == question["answer"]:
                st.session_state.correct += 1
                st.session_state.xp += 10
                st.session_state.streak += 1
                st.session_state.best_streak = max(
                    st.session_state.best_streak,
                    st.session_state.streak,
                )
                st.success(f"🎉 {t['right']} +10 XP")
            else:
                st.session_state.streak = 0
                st.error(
                    f"{t['wrong']} **{question['answer']}**"
                )

            st.rerun()

    else:
        if selected == question["answer"]:
            st.success(f"✨ {t['right']}")
        else:
            st.info(f"{t['correct_answer']}: {question['answer']}")

        if st.button(t["next"], type="primary"):
            st.session_state.question, st.session_state.options = create_question(
                target, base, difficulty
            )
            st.session_state.answered = False
            st.rerun()


# ---------------------- КАРТОЧКИ --------------------------

elif mode_label == t["flash"]:
    st.markdown(f"## 🃏 {t['flash']}")

    records = get_records(target, difficulty)
    if not records:
        records = WORDS[target]

    st.session_state.card_index %= len(records)
    item = records[st.session_state.card_index]

    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown(
        f"<div class='word'>{item[0]}</div>",
        unsafe_allow_html=True,
    )

    if target == "zh":
        st.markdown(
            f"<p style='text-align:center;color:#a9b4cf'>"
            f"Pinyin: {item[5]}</p>",
            unsafe_allow_html=True,
        )

    if st.session_state.card_revealed:
        translation = item[1] if base == "ru" else (
            item[2] if base == "uz" else item[3]
        )
        st.markdown(
            f"<h3 style='text-align:center;color:#6ee7b7'>{translation}</h3>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<p style='text-align:center;color:#a9b4cf'>"
            f"{t['reveal']}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button(t["reveal"], key="reveal_card"):
            st.session_state.card_revealed = True
            st.rerun()

    with c2:
        if st.button(t["new_card"], key="next_card"):
            st.session_state.card_index = (
                st.session_state.card_index + 1
            ) % len(records)
            st.session_state.card_revealed = False
            st.rerun()

    st.progress((st.session_state.card_index + 1) / len(records))
    st.caption(f"Card {st.session_state.card_index + 1} / {len(records)}")


# ---------------------- ПЕРЕВОД ФРАЗ ---------------------

elif mode_label == t["phrase"]:
    st.markdown(f"## 💬 {t['phrase']}")

    phrases = PHRASES[target]
    index = st.session_state.phrase_index % len(phrases)
    phrase = phrases[index]

    source_phrase = phrase[0] if base == "ru" else (
        phrase[1] if base == "uz" else phrase[2]
    )
    correct_phrase = phrase[3]

    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown(
        f"<div class='word'>{source_phrase}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    typed = st.text_input(
        t["write"],
        key=f"phrase_input_{st.session_state.signature}_{index}",
        disabled=st.session_state.phrase_checked,
    )

    if not st.session_state.phrase_checked:
        if st.button(t["check"], key="check_phrase"):
            st.session_state.phrase_checked = True
            st.session_state.attempts += 1

            if normalize(typed) == normalize(correct_phrase):
                st.session_state.correct += 1
                st.session_state.xp += 20
                st.session_state.streak += 1
                st.session_state.best_streak = max(
                    st.session_state.best_streak,
                    st.session_state.streak,
                )
                st.success(f"🎉 {t['right']} +20 XP")
            else:
                st.session_state.streak = 0
                st.info(f"{t['correct_answer']}: {correct_phrase}")

            st.rerun()

    else:
        st.info(f"{t['correct_answer']}: {correct_phrase}")

        if st.button(t["next"], key="next_phrase"):
            st.session_state.phrase_index += 1
            st.session_state.phrase_checked = False
            st.rerun()


# ---------------------- ПРОГРЕСС --------------------------

st.divider()
st.markdown(f"## 🏆 {t['progress']}")

total = st.session_state.attempts
accuracy = (
    round(st.session_state.correct / total * 100)
    if total else 0
)

progress_col1, progress_col2 = st.columns(2)

with progress_col1:
    st.markdown(f"### 🎯 {t['goal']}")
    st.progress(min(st.session_state.correct / 10, 1.0))
    st.caption(f"{st.session_state.correct} / 10 correct answers")

with progress_col2:
    st.markdown("### 📈 Accuracy")
    st.progress(accuracy / 100)
    st.caption(f"{accuracy}%")

if st.session_state.xp >= 200:
    level = 3
    level_name = "Language Explorer"
elif st.session_state.xp >= 70:
    level = 2
    level_name = "Word Adventurer"
else:
    level = 1
    level_name = "First Steps"

st.markdown(f"""
<div class="game-card">
    <div class="pill">LEVEL {level}</div>
    <h3>🌟 {level_name}</h3>
    <p class="muted">Keep playing to unlock your next milestone.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"### 💡 {t['tip']}")
st.info(t["tip_text"])

st.caption(
    "LinguaPlay MVP · Учебные примеры демонстрационные. "
    "Прогресс хранится в текущей сессии."
)
