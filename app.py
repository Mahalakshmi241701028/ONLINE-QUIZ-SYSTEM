import streamlit as st
import time

st.set_page_config(page_title="Quiz App", page_icon="🧠")

# ---------- FUNCTION ----------
def expand_to_15(questions):
    expanded = []
    count = 1
    while len(expanded) < 15:
        for q in questions:
            new_q = q.copy()
            new_q["question"] = f"{q['question']} (Q{count})"
            expanded.append(new_q)
            count += 1
            if len(expanded) == 15:
                break
    return expanded

# ---------- QUIZ BANK ----------
QUIZ_BANK = {
    "Environment": expand_to_15([
        {"question":"What is global warming?","options":["Increase in earth temperature","Decrease in rainfall","Cooling of earth","None"],"answer":1},
        {"question":"Which gas causes greenhouse effect?","options":["Oxygen","Nitrogen","Carbon dioxide","Hydrogen"],"answer":3},
        {"question":"What is recycling?","options":["Burning waste","Reusing materials","Throwing garbage","None"],"answer":2},
        {"question":"Deforestation leads to?","options":["More rain","Less pollution","Loss of biodiversity","None"],"answer":3},
        {"question":"Renewable energy source?","options":["Coal","Petrol","Solar","Diesel"],"answer":3}
    ]),
    "Computer Science": expand_to_15([
        {"question":"CPU stands for?","options":["Central Process Unit","Central Processing Unit","Computer Unit","Control Unit"],"answer":2},
        {"question":"RAM is?","options":["Permanent memory","Temporary memory","Storage disk","None"],"answer":2},
        {"question":"Binary system uses?","options":["0-9","0 and 1","1-10","None"],"answer":2},
        {"question":"OS means?","options":["Operating System","Open Software","Output System","None"],"answer":1},
        {"question":"Python is?","options":["Snake","Programming language","Game","OS"],"answer":2}
    ]),
    "Maths": expand_to_15([
        {"question":"2 + 2 = ?","options":["3","4","5","6"],"answer":2},
        {"question":"Square of 5?","options":["10","20","25","30"],"answer":3},
        {"question":"√16 = ?","options":["2","3","4","5"],"answer":3},
        {"question":"10/2 = ?","options":["2","3","5","6"],"answer":3},
        {"question":"7 x 6 = ?","options":["36","40","42","48"],"answer":3}
    ]),
    "English Grammar": expand_to_15([
        {"question":"Choose correct: She ___ going.","options":["is","are","am","be"],"answer":1},
        {"question":"Plural of child?","options":["childs","children","childes","None"],"answer":2},
        {"question":"He ___ a car.","options":["have","has","had","None"],"answer":2},
        {"question":"Synonym of fast?","options":["slow","quick","late","None"],"answer":2},
        {"question":"Opposite of hot?","options":["warm","cold","cool","None"],"answer":2}
    ]),
    "General Knowledge": expand_to_15([
        {"question":"Capital of India?","options":["Delhi","Mumbai","Chennai","Kolkata"],"answer":1},
        {"question":"National animal of India?","options":["Lion","Tiger","Elephant","Dog"],"answer":2},
        {"question":"Largest ocean?","options":["Atlantic","Indian","Pacific","Arctic"],"answer":3},
        {"question":"Sun is a?","options":["Planet","Star","Moon","Asteroid"],"answer":2},
        {"question":"Water formula?","options":["CO2","H2O","O2","NaCl"],"answer":2}
    ])
}

# ---------- USERS ----------
if "users" not in st.session_state:
    st.session_state.users = {
        "mahalakshmi.d.2024.csd@rajlakshmi.edu.in": {"password": "241701028","role": "admin"},
        "maahesh.s.2024.csd@rajalaksmi.edu.in": {"password": "025","role": "user"},
        "pradeepkumar.r.2024.csd@rajalakshmi.edu.in": {"password": "041","role": "user"},
        "samyuktha.su.2024.csd@rajalakshmi.edu.in": {"password": "047","role": "user"}
    }

# ---------- SESSION ----------
defaults = {
    "logged_in": False,
    "role": None,
    "username": "",
    "assigned_quiz": None,
    "results": [],
    "attempted": {}
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- LOGIN + REGISTER ----------
if not st.session_state.logged_in:
    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN
    with tab1:
        u = st.text_input("Email")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u in st.session_state.users and st.session_state.users[u]["password"] == p:
                st.session_state.logged_in = True
                st.session_state.role = st.session_state.users[u]["role"]
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid login")

    # REGISTER
    with tab2:
        new_user = st.text_input("New Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if new_user in st.session_state.users:
                st.warning("User already exists")
            elif new_user == "" or new_pass == "":
                st.warning("Fill all fields")
            else:
                st.session_state.users[new_user] = {
                    "password": new_pass,
                    "role": "user"
                }
                st.success("Registered successfully! Please login")

    st.stop()

# ---------- LOGOUT ----------
st.sidebar.write(st.session_state.username)
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ================= ADMIN =================
if st.session_state.role == "admin":
    st.title("👨‍💼 Admin Panel")

    topic = st.selectbox("Select Quiz Topic", list(QUIZ_BANK.keys()))

    if st.button("Assign Quiz"):
        st.session_state.assigned_quiz = topic
        st.success(f"{topic} quiz assigned!")

    st.subheader("👥 Registered Students")
    students = [u for u,info in st.session_state.users.items() if info["role"]=="user"]
    for s in students:
        st.write(s)

    st.subheader("📊 Results")
    for r in st.session_state.results:
        st.write(f"{r['user']} | {r['quiz']} | {r['score']}/15")

    st.subheader("❌ Not Attended")
    quiz = st.session_state.assigned_quiz
    if quiz:
        attended = [r["user"] for r in st.session_state.results if r["quiz"] == quiz]
        not_attended = [s for s in students if s not in attended]

        for s in not_attended:
            st.write(s)

# ================= USER =================
elif st.session_state.role == "user":
    st.title("🎮 User Panel")

    user = st.session_state.username
    quiz = st.session_state.assigned_quiz

    st.subheader("📊 Dashboard")
    user_results = [r for r in st.session_state.results if r["user"] == user]

    if user_results:
        total = len(user_results)
        avg = sum(r["score"] for r in user_results) / total
        best = max(r["score"] for r in user_results)

        st.write(f"Total Attempts: {total}")
        st.write(f"Average Score: {avg:.2f}")
        st.write(f"Best Score: {best}")

    st.subheader("🏆 Leaderboard")
    sorted_results = sorted(st.session_state.results, key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(sorted_results[:5], 1):
        st.write(f"{i}. {r['user']} - {r['score']}")

    st.subheader("📜 History")
    for r in user_results:
        st.write(f"{r['quiz']} → {r['score']}")

    if not quiz:
        st.warning("No quiz assigned")
        st.stop()

    if user in st.session_state.attempted and quiz in st.session_state.attempted[user]:
        st.error("Already attempted")
        st.stop()

    if st.button("Start Quiz"):
        st.session_state.current = quiz
        st.session_state.i = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.start_time = time.time()
        st.rerun()

# ================= QUIZ =================
if "current" in st.session_state:
    qs = QUIZ_BANK[st.session_state.current]
    i = st.session_state.i

    remaining = int(600 - (time.time() - st.session_state.start_time))
    st.warning(f"⏱ {remaining//60:02d}:{remaining%60:02d}")
    st.progress(i / len(qs))

    if i < len(qs):
        q = qs[i]
        st.subheader(f"Q{i+1}: {q['question']}")
        ans = st.radio("Choose", q["options"], key=i)

        if st.button("Next"):
            idx = q["options"].index(ans) + 1
            st.session_state.answers.append(idx)

            if idx == q["answer"]:
                st.session_state.score += 1

            st.session_state.i += 1
            st.rerun()
    else:
        st.success(f"Score: {st.session_state.score}/{len(qs)}")

        acc = (st.session_state.score/len(qs))*100
        st.write(f"Accuracy: {acc:.2f}%")

        st.session_state.results.append({
            "user": st.session_state.username,
            "quiz": st.session_state.current,
            "score": st.session_state.score
        })

        st.session_state.attempted.setdefault(st.session_state.username, []).append(st.session_state.current)

        st.subheader("📊 Review")
        for idx,q in enumerate(qs):
            ua = st.session_state.answers[idx]
            ca = q["answer"]

            st.write(q["question"])
            for i,opt in enumerate(q["options"],1):
                if i == ca:
                    st.success(f"✔ {opt}")
                elif i == ua:
                    st.error(f"✘ {opt}")
                else:
                    st.write(opt)

        del st.session_state["current"]
