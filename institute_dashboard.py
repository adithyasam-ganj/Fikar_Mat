import os
from datetime import datetime, date, timedelta

import streamlit as st
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# --- IMPORT YOUR MODELS ---
# Easiest if you move your models (Base, User, Score) into a separate file, e.g. db_models.py
# and then:
from db_models import Base, User, Score, DB_PATH

# For this example, let's assume DB_PATH is set via env just like in your notebook.
# DB_PATH = os.getenv("FIKARMAT_DB", "D:/Data_Science/LangGraph/fikarmat.db")

engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

########################## Helper Functions ##############################################

def last_n_month_starts(n: int = 6) -> list[date]:
    """Return a list of month-start dates, oldest → newest."""
    today = date.today()
    year = today.year
    month = today.month

    months = []
    for i in range(n):
        m = month - (n - 1 - i)
        y = year
        while m <= 0:
            m += 12
            y -= 1
        months.append(date(y, m, 1))
    return months

######################################### Weekly Login Status ###############################################################

def show_weekly_login_status():
    st.header("📅 Weekly Login Status")

    with SessionLocal() as db:
        users = db.execute(select(User)).scalars().all()

    if not users:
        st.info("No users found in the database yet.")
        return

    # Compute start of current week (Monday 00:00)
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    start_of_week = datetime.combine(monday, datetime.min.time())

    rows = []
    for u in users:
        last_login = u.last_login_at
        logged_this_week = bool(last_login and last_login >= start_of_week)
        rows.append({
            "User ID": u.user_id,
            "Username": u.username,
            "Last login (UTC)": last_login,
            "Logged this week?": "✅ Yes" if logged_this_week else "❌ No",
        })

    st.dataframe(rows, use_container_width=True)

###################################################################################################################################################

def show_scores_section():
    st.header("📊 Monthly Scores (last 6 months)")

    with SessionLocal() as db:
        users = db.execute(select(User)).scalars().all()

    if not users:
        st.info("No users found.")
        return

    # Dropdown to pick a student
    user_options = {f"{u.user_id} - {u.username or 'no username'}": u for u in users}
    selected_label = st.selectbox("Select student", list(user_options.keys()))
    selected_user = user_options[selected_label]

    st.subheader(f"Scores for {selected_user.username or selected_user.user_id}")

    months = last_n_month_starts(6)
    month_labels = [m.strftime("%b %Y") for m in months]

    # Preload existing scores into a dict: {month: avg_score}
    with SessionLocal() as db:
        existing = db.execute(
            select(Score)
            .where(Score.user_id == selected_user.user_id, Score.month.in_(months))
        ).scalars().all()

        existing_map = {s.month: s for s in existing}

    score_inputs = {}
    for m, label in zip(months, month_labels):
        existing_score = existing_map.get(m).avg_score if m in existing_map else 0.0
        score_inputs[m] = st.number_input(
            f"{label} avg score",
            min_value=0.0,
            max_value=100.0,
            value=float(existing_score),
            step=1.0,
        )

    if st.button("Save scores"):
        with SessionLocal() as db:
            for m, score_val in score_inputs.items():
                s = db.execute(
                    select(Score).where(Score.user_id == selected_user.user_id, Score.month == m)
                ).scalar_one_or_none()
                if s:
                    s.avg_score = score_val
                else:
                    s = Score(
                        user_id=selected_user.user_id,
                        month=m,
                        avg_score=score_val,
                    )
                    db.add(s)
            db.commit()
        st.success("Scores saved/updated.")

############################################ Main App #################################################################################

def main():
    st.title("🏫 Institute Dashboard - Fikar Mat")

    tab1, tab2 = st.tabs(["Weekly Login Status", "Monthly Scores"])
    with tab1:
        show_weekly_login_status()
    with tab2:
        show_scores_section()


if __name__ == "__main__":
    main()