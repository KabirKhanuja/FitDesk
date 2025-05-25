import streamlit as st
from exercises import shoulder_shrugs, squats
import subprocess

st.set_page_config(page_title="FitDesk", layout="wide")

# Initialize session state
if 'category' not in st.session_state:
    st.session_state.category = None
if 'selected_exercise' not in st.session_state:
    st.session_state.selected_exercise = None
if 'start_exercise' not in st.session_state:
    st.session_state.start_exercise = False

# Header
st.title("👋 Welcome back, User!")
st.subheader("Your next workout")

# Next workout
st.markdown("### Full body strength")
st.caption("45 minutes - Intermediate")
# st.image("assets/images/strength_training.png", width=300)

if st.button("Start a new workout"):
    st.session_state['page'] = 'workout'

# Featured collections
st.markdown("### Featured collections")
cols = st.columns(4)

with cols[0]:
    st.image("assets/images/quick_workouts.png")
    if st.button("Quick Workouts"):
        st.session_state.category = "quick"
        st.session_state.selected_exercise = None
        st.session_state.start_exercise = False

with cols[1]:
    st.image("assets/images/yoga.png")
    if st.button("Yoga for Beginners"):
        st.session_state.category = "yoga"
        st.session_state.selected_exercise = None
        st.session_state.start_exercise = False

with cols[2]:
    st.image("assets/images/hiit.png")
    if st.button("High Intensity"):
        st.session_state.category = "hiit"
        st.session_state.selected_exercise = None
        st.session_state.start_exercise = False

with cols[3]:
    st.image("assets/images/stretching.png")
    if st.button("Stretching Routines"):
        st.session_state.category = "stretching"
        st.session_state.selected_exercise = None
        st.session_state.start_exercise = False

# -----------------------
# Sub-exercise selection
# -----------------------

if st.session_state.category == "quick":
    st.markdown("### Quick Workouts")
    if st.button("Shoulder Shrugs"):
        st.session_state.selected_exercise = "shoulder_shrugs"
        st.session_state.start_exercise = False

elif st.session_state.category == "hiit":
    st.markdown("### High Intensity Training")
    if st.button("Squats"):
        st.session_state.selected_exercise = "squats"
        st.session_state.start_exercise = False

elif st.session_state.category == "yoga":
    st.info("Yoga module coming soon!")

elif st.session_state.category == "stretching":
    st.info("Stretching module coming soon!")

# -----------------------
# Start Exercise
# -----------------------

if st.session_state.selected_exercise:
    st.markdown("### Ready to begin your exercise?")
    if st.button("Start Exercise"):
        st.session_state.start_exercise = True


    if st.session_state.start_exercise:
        if st.session_state.selected_exercise == "shoulder_shrugs":
            subprocess.Popen(["python3", "exercises/shoulder_shrugs.py"])
            st.success("Shoulder Shrugs started in a new window.")
        elif st.session_state.selected_exercise == "squats":
            subprocess.Popen(["python3", "exercises/squats.py"])
            st.success("Squats tracker started in a new window.")





