import streamlit as st
import subprocess
import platform
import os

st.set_page_config(page_title="FitDesk", layout="wide")

if 'category' not in st.session_state:
    st.session_state.category = None
if 'selected_exercise' not in st.session_state:
    st.session_state.selected_exercise = None
if 'start_exercise' not in st.session_state:
    st.session_state.start_exercise = False

st.title("👋 Welcome back, User!")
st.subheader("Your next workout")

st.markdown("### Full body strength")
st.caption("45 minutes - Intermediate")

if st.button("Start a new workout"):
    st.session_state['page'] = 'workout'

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

#sub process of exercise 

if st.session_state.category == "quick":
    st.markdown("### Quick Workouts")
    if st.button("Shoulder Shrugs"):
        st.session_state.selected_exercise = "shoulder_shrugs"
        st.session_state.start_exercise = False
    if st.button("Wrist Curls"):
        st.session_state.selected_exercise = "wrist_curls"
        st.session_state.start_exercise = False
    if st.button("Bicep Curl Left"):
        st.session_state.selected_exercise = "bicep_curl_left"
        st.session_state.start_exercise = False
    if st.button("Bicep Curl Right"):
        st.session_state.selected_exercise = "bicep_curl_right"
        st.session_state.start_exercise = False

elif st.session_state.category == "hiit":
    st.markdown("### High Intensity Training")
    if st.button("Squats"):
        st.session_state.selected_exercise = "squats"
        st.session_state.start_exercise = False
    if st.button("Alternate Toe Touch"):
        st.session_state.selected_exercise = "alternate_toe_touch"
        st.session_state.start_exercise = False
    if st.button("High Knees"):
        st.session_state.selected_exercise = "high_knees"
        st.session_state.start_exercise = False

elif st.session_state.category == "yoga":
    st.markdown("### Yoga for Beginners")
    if st.button("Cobra Pose"):
        st.session_state.selected_exercise = "cobra_pose"
        st.session_state.start_exercise = False
    if st.button("Tree Pose Right"):
        st.session_state.selected_exercise = "tree_pose_right"
        st.session_state.start_exercise = False
    if st.button("Tree Pose Left"):
        st.session_state.selected_exercise = "tree_pose_left"
        st.session_state.start_exercise = False

elif st.session_state.category == "stretching":
    st.markdown("### Stretching Routines")
    if st.button("Neck Rotation"):
        st.session_state.selected_exercise = "neck_rotation"
        st.session_state.start_exercise = False
    if st.button("Arm Rotation Left"):
        st.session_state.selected_exercise = "arm_rotation_left"
        st.session_state.start_exercise = False
    if st.button("Arm Rotation Right"):
        st.session_state.selected_exercise = "arm_rotation_right"
        st.session_state.start_exercise = False


# Start of exercises


if st.session_state.selected_exercise:
    st.markdown("### Ready to begin your exercise?")
    if st.button("Start Exercise"):
        st.session_state.start_exercise = True

    if st.session_state.start_exercise:
        exercise_file_map = {
            "shoulder_shrugs": "shoulder_shrugs.py",
            "wrist_curls": "wrist_curls.py",
            "bicep_curl_left": "bicep_curl_left.py",
            "bicep_curl_right": "bicep_curl_right.py",
            "squats": "squats.py",
            "alternate_toe_touch": "alternate_toe_touch.py",
            "high_knees": "high_knees.py",
            "cobra_pose": "cobra_pose.py",
            "tree_pose_right": "tree_pose_right.py",
            "tree_pose_left": "tree_pose_left.py",
            "neck_rotation": "neck_rotation.py",
            "arm_rotation_left": "arm_rotation_left.py",
            "arm_rotation_right": "arm_rotation_right.py"
        }

        selected_file = exercise_file_map.get(st.session_state.selected_exercise)
        script_path = os.path.join("exercises", selected_file)

        if selected_file and os.path.exists(script_path):
            try:
                subprocess.Popen(["python3", script_path],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 start_new_session=True)
                st.success(f"{st.session_state.selected_exercise.replace('_', ' ').title()} started.")
            except Exception as e:
                st.error(f"Failed to launch script: {e}")
        else:
            st.error(f"Script not found at {script_path}")
