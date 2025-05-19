import streamlit as st
from camera import run_camera
from attendance import ensure_csv_exists

st.set_page_config(
    page_title="AttendAI",
    layout="wide",
    page_icon="📷"
)

st.markdown("<link rel='shortcut icon' href='favicon.png'>", unsafe_allow_html=True)

ensure_csv_exists()

if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False

# ---------- Sidebar Controls ----------
with st.sidebar:
    st.title("🎛️ Controls")
    st.markdown("Use the switch below to start or stop the face recognition camera.")
    st.session_state.camera_on = st.toggle("🎥 Toggle Camera", value=st.session_state.camera_on)

    st.markdown("---")
    st.markdown("💡 *Tip: Ensure good lighting and face visibility for best accuracy.*")

    st.markdown("---")
    st.markdown("📬 **Status:**")
    if st.session_state.camera_on:
        st.success("✅ Camera is ON")
    else:
        st.warning("🛑 Camera is OFF")

    st.markdown("---")
    st.caption("👨‍💻 Developed by Mudit Jain")

# ---------- Title ----------
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #1f77b4;'>📸 AttendAI: Face Attendance System</h1>
    </div>
""", unsafe_allow_html=True)

st.divider()
# ---------- Main Layout ----------
left_col, right_col = st.columns([2.5, 1.5], gap="medium")

# ---------- Left: Camera Feed ----------
with left_col:
    st.markdown("### 🎥 Live Camera Feed")
    camera_box = st.container()

    if st.session_state.camera_on:
        with camera_box:
            run_camera()
    else:
        with camera_box:
            st.info("🔌 Click the toggle in the sidebar to activate the camera.")

# ---------- Right: Info + Log ----------
with right_col:
    st.markdown("### 📊 Attendance Log")
    st.markdown("<p style='font-size: 0.9em; color: gray;'>Latest recognized students will appear below.</p>", unsafe_allow_html=True)
    st.session_state.attendance_log_placeholder = st.empty()

# ---------- Footer ----------
st.markdown(
    "<p style='text-align: center; color: #aaa;'>💻 Built using Streamlit, OpenCV & DeepFace | © 2025</p>",
    unsafe_allow_html=True
)
